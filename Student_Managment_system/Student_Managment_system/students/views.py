from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models  # Add this import
from .models import StudentProfile, Marks, Subject, notice, Assignment, StudentSubmission
from .serializers import (NoticeSerializer, StudentProfileSerializer, MarksSerializer, 
                        SubjectSerializer, AssignmentSerializer, StudentSubmissionSerializer)
from users.permissions import IsTeacher, IsAdmin, IsTeacherOrAdmin

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Only admins can create or delete subjects
            return [IsAdmin()]
        if self.action in ['update', 'partial_update']:
            # Only teachers or admins can update subjects
            return [permissions.IsAuthenticated() & (IsTeacher() | IsAdmin())]
        # Anyone authenticated can view subjects
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'], url_path='unassigned')
    def unassigned_subjects(self, request):
        # Get all subjects without a teacher or with null teacher
        unassigned = Subject.objects.filter(teacher__isnull=True)
        serializer = self.get_serializer(unassigned, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-subjects')
    def my_subjects(self, request):
        """Get subjects assigned to the current teacher"""
        user = request.user
        if user.role != 'teacher':
            return Response(
                {"error": "Only teachers can access their subjects"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        subjects = Subject.objects.filter(teacher=user)
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Don't assign a teacher when creating a subject through the API
        serializer.save(teacher=None)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Subject.objects.none()
            
        if user.role == 'teacher':
            return Subject.objects.filter(teacher=user)
        # Admin can see all subjects
        return Subject.objects.all()


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'assign_subjects']:
            # Use the combined permission class instead of OR operator
            return [IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = StudentProfile.objects.all()
        user = self.request.user
        subject_id = self.request.query_params.get('subject', None)
        user_id = self.request.query_params.get('user', None)
        
        # Log for debugging
        print(f"Filtering student profiles - User: {user.username}, Role: {user.role}, Subject ID: {subject_id}, User ID: {user_id}")
        
        if not user.is_authenticated:
            return StudentProfile.objects.none()
            
        # Filter by specific user if requested (for finding a student's profile)
        if user_id:
            # Admin can see any student profile
            if user.role == 'admin':
                return queryset.filter(user_id=user_id)
            
            # Teachers can see profiles of students in their subjects
            elif user.role == 'teacher':
                return queryset.filter(
                    user_id=user_id,
                    subjects__teacher=user
                ).distinct()
            
            # Students can only see their own profile
            elif user.role == 'student' and str(user.id) == str(user_id):
                return queryset.filter(user=user)
                
            return StudentProfile.objects.none()
        
        # Filter by role
        if user.role == 'teacher':
            if subject_id:
                try:
                    # Get students enrolled in a specific subject
                    return queryset.filter(subjects__id=subject_id, subjects__teacher=user)
                except Exception as e:
                    print(f"Error filtering by subject: {e}")
                    return StudentProfile.objects.none()
            # Get all students (optional: limit to only students associated with this teacher's subjects)
            return queryset.filter(subjects__teacher=user).distinct()
        elif user.role == 'student':
            # Students can only see their own profile
            return queryset.filter(user=user)
        
        # Admin can see all
        return queryset

    @action(detail=True, methods=['post'], url_path='assign-subjects')
    def assign_subjects(self, request, pk=None):
        """Assign subjects to a student"""
        try:
            # Get the profile
            try:
                profile = StudentProfile.objects.get(pk=pk)
            except StudentProfile.DoesNotExist:
                return Response(
                    {"error": f"Student profile with ID {pk} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            subject_ids = request.data.get('subject_ids', [])
            
            if not subject_ids:
                return Response({"error": "No subjects provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Ensure subject_ids is a list of integers
            if isinstance(subject_ids, list):
                subject_ids = [int(sid) for sid in subject_ids if sid]
            else:
                return Response(
                    {"error": "subject_ids must be a list"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate that all subject IDs exist
            subjects = Subject.objects.filter(id__in=subject_ids)
            if len(subjects) != len(subject_ids):
                missing_ids = set(subject_ids) - set(subjects.values_list('id', flat=True))
                return Response(
                    {"error": f"One or more subject IDs are invalid: {missing_ids}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check teacher's permissions - teachers can only assign subjects they teach
            user = request.user
            if user.role == 'teacher':
                teacher_subjects = Subject.objects.filter(teacher=user)
                teacher_subject_ids = set(teacher_subjects.values_list('id', flat=True))
                invalid_subject_ids = set(subject_ids) - teacher_subject_ids
                
                if invalid_subject_ids:
                    return Response(
                        {"error": f"You can only assign subjects that you teach. Invalid IDs: {invalid_subject_ids}"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Assign the subjects to the student
            profile.subjects.clear()
            profile.subjects.add(*subjects)
            
            # Return updated profile
            serializer = self.get_serializer(profile)
            return Response({
                "message": f"Successfully assigned {len(subjects)} subjects to {profile.user.username}",
                "profile": serializer.data
            })
        except Exception as e:
            return Response(
                {"error": f"Server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'], url_path='list-students')
    def list_students(self, request):
        """List all students for subject assignment"""
        from users.models import User
        from users.serializers import UserSerializer
        
        # If teacher, only return students assigned to their subjects
        user = request.user
        if user.role == 'teacher':
            student_users = User.objects.filter(
                role='student',
                studentprofile__subjects__teacher=user
            ).distinct()
        else:
            student_users = User.objects.filter(role='student')
        
        serializer = UserSerializer(student_users, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a student profile with better error handling"""
        try:
            # Check if a profile already exists for this user
            user_id = request.data.get('user')
            if StudentProfile.objects.filter(user_id=user_id).exists():
                return Response(
                    {"error": "A profile already exists for this user"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Proceed with creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to create profile: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish_results', 'bulk_create']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            # Students can only see their published marks or allow them to see unpublished too based on requirements
            student_profile = StudentProfile.objects.filter(user=user).first()
            if student_profile:
                return Marks.objects.filter(student=student_profile, published=True)
            return Marks.objects.none()
        elif user.role == 'teacher':
            # Teachers can see all marks for subjects they teach
            return Marks.objects.filter(subject__teacher=user)
        # Admins can see all marks
        return Marks.objects.all()

    @action(detail=False, methods=['post'], url_path='publish')
    def publish_results(self, request):
        """Publish marks for students"""
        subject_id = request.data.get('subject_id')
        student_ids = request.data.get('student_ids', [])
        publish_all = request.data.get('publish_all', False)
        
        if not subject_id:
            return Response({"error": "Subject ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if teacher teaches this subject
        subject = Subject.objects.filter(id=subject_id, teacher=request.user).first()
        if not subject:
            return Response(
                {"error": "You can only publish results for subjects you teach"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Build the filter
        filter_kwargs = {'subject': subject}
        if not publish_all and student_ids:
            filter_kwargs['student__id__in'] = student_ids
        
        # Update marks to published
        marks_count = Marks.objects.filter(**filter_kwargs).update(published=True)
        
        return Response({
            "message": f"Published {marks_count} results successfully",
            "count": marks_count
        })
    
    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        """Add marks for multiple students at once"""
        subject_id = request.data.get('subject_id')
        marks_data = request.data.get('marks_data', [])
        
        if not subject_id:
            return Response({"error": "Subject ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not marks_data:
            return Response({"error": "Marks data is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if teacher teaches this subject
        subject = Subject.objects.filter(id=subject_id, teacher=request.user).first()
        if not subject:
            return Response(
                {"error": "You can only add marks for subjects you teach"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        created_count = 0
        updated_count = 0
        errors = []
        
        for item in marks_data:
            student_id = item.get('student_id')
            mark_value = item.get('marks')
            
            if not student_id or mark_value is None:
                errors.append(f"Missing student_id or marks for item: {item}")
                continue
                
            # Find the student profile
            student = StudentProfile.objects.filter(id=student_id).first()
            if not student:
                errors.append(f"Student with ID {student_id} not found")
                continue
                
            # Update or create the mark
            mark, created = Marks.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={'marks': mark_value}
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        return Response({
            "message": f"Created {created_count} marks and updated {updated_count} marks",
            "created": created_count,
            "updated": updated_count,
            "errors": errors
        })

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = notice.objects.all()
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return notice.objects.filter(audience__in=['student', 'both'], published=True)
        elif user.role == 'teacher':
            # Allow teachers to see notices targeted to teachers AND notices they created
            return notice.objects.filter(
                models.Q(audience__in=['teacher', 'both'], published=True) | 
                models.Q(created_by=user)
            ).distinct()
        # Admin can see all notices
        return notice.objects.all()
        
    def perform_create(self, serializer):
        user = self.request.user
        audience = serializer.validated_data.get('audience')
        
        # Admin can choose anyone as audience
        if user.role == 'admin':
            serializer.save(created_by=user)
        # Teacher can only choose student as audience
        elif user.role == 'teacher':
            if audience != 'student':
                raise serializer.ValidationError("Teachers can only create notices for students.")
            serializer.save(created_by=user)

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Assignment.objects.none()
            
        if user.role == 'student':
            # Students can see assignments for subjects they're enrolled in AND published assignments
            try:
                student_profile = StudentProfile.objects.get(user=user)
                # Get student's enrolled subjects
                student_subjects = student_profile.subjects.all()
                
                return Assignment.objects.filter(
                    subject__in=student_subjects,
                    published=True
                ).distinct()
            except StudentProfile.DoesNotExist:
                return Assignment.objects.none()
                
        elif user.role == 'teacher':
            # Teachers can see assignments they created or for subjects they teach
            return Assignment.objects.filter(
                models.Q(created_by=user) | models.Q(subject__teacher=user)
            ).distinct()
        # Admin can see all assignments
        return Assignment.objects.all()
        
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        user = self.request.user
        assignment = self.get_object()
        
        # Check permissions for updating assignments
        if user.role == 'admin':
            # Admin can edit any assignment
            pass
        elif user.role == 'teacher':
            # Teachers can only edit assignments they created
            if assignment.created_by != user:
                raise serializers.ValidationError("You can only edit assignments that you created")
        else:
            raise serializers.ValidationError("You don't have permission to edit assignments")
        
        serializer.save()
    
    def perform_destroy(self, serializer):
        user = self.request.user
        assignment = self.get_object()
        
        # Check permissions for deleting assignments (similar to update)
        if user.role == 'admin':
            # Admin can delete any assignment
            pass
        elif user.role == 'teacher':
            # Teachers can only delete assignments they created
            if assignment.created_by != user:
                raise serializers.ValidationError("You can only delete assignments that you created")
        else:
            raise serializers.ValidationError("You don't have permission to delete assignments")
        
        assignment.delete()

class StudentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = StudentSubmission.objects.all()
    serializer_class = StudentSubmissionSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Students can create (submit) assignments
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # Only students can edit/delete their own submissions
            return [permissions.IsAuthenticated()]
        # Anyone authenticated can view submissions based on get_queryset filtering
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return StudentSubmission.objects.none()
            
        if user.role == 'student':
            # Students can only see their own submissions
            try:
                student_profile = StudentProfile.objects.get(user=user)
                return StudentSubmission.objects.filter(student=student_profile)
            except StudentProfile.DoesNotExist:
                return StudentSubmission.objects.none()
        elif user.role == 'teacher':
            # Teachers can see submissions for assignments they created or in subjects they teach
            return StudentSubmission.objects.filter(
                models.Q(assignment__created_by=user) | 
                models.Q(assignment__subject__teacher=user)
            ).distinct()
        # Admin can see all submissions (READ-ONLY)
        return StudentSubmission.objects.all()
        
    def perform_create(self, serializer):
        # Set the student automatically based on the authenticated user
        user = self.request.user
        if user.role != 'student':
            raise serializers.ValidationError("Only students can submit assignments")
            
        try:
            student_profile = StudentProfile.objects.get(user=user)
            # Check if student is enrolled in the assignment's subject
            assignment = serializer.validated_data['assignment']
            if assignment.subject not in student_profile.subjects.all():
                raise serializers.ValidationError("You are not enrolled in this subject")
            serializer.save(student=student_profile)
        except StudentProfile.DoesNotExist:
            raise serializers.ValidationError("Student profile not found for the current user")
    
    def perform_update(self, serializer):
        user = self.request.user
        submission = self.get_object()
        
        # Only students can edit their own submissions
        if user.role == 'student':
            # Students can only edit their own submissions
            if submission.student.user != user:
                raise serializers.ValidationError("You can only edit your own submissions")
        else:
            # Teachers and admins cannot edit student submissions
            raise serializers.ValidationError("Only students can edit their submissions")
        
        # Save the submission (the serializer's update method will handle file preservation)
        serializer.save()
    
    def perform_destroy(self, serializer):
        user = self.request.user
        submission = self.get_object()
        
        # Only students can delete their own submissions
        if user.role == 'student':
            if submission.student.user != user:
                raise serializers.ValidationError("You can only delete your own submissions")
        else:
            # Teachers and admins cannot delete student submissions
            raise serializers.ValidationError("Only students can delete their submissions")
        
        submission.delete()

