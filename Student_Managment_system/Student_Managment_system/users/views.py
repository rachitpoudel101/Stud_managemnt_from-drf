from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdmin
from students.models import Subject, StudentProfile
from students.serializers import StudentProfileSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create' and User.objects.count() == 0:
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [IsAdmin()]
        if self.action == 'destroy':
            # Allow delete only if admin or teacher
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'retrieve', 'list', 'change_username', 'restore_user', 'deleted_users']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
            
        # By default, only show non-deleted users
        queryset = User.objects.filter(is_deleted=False)
            
        if user.role == 'admin':
            return queryset
        if user.role == 'teacher':
            # Teachers can see only student users
            return queryset.filter(role='student')
        # Students can only see themselves
        return queryset.filter(id=user.id)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if the user being created is a teacher and requires subjects
        if serializer.validated_data.get('role') == 'teacher':
            # Get the subjects from the request
            subject_ids = request.data.get('subjects', [])
            
            # Validate that subjects are provided for teachers
            if not subject_ids:
                return Response(
                    {"error": "At least one subject must be assigned to a teacher"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Validate that all subject IDs exist
            valid_subject_ids = list(Subject.objects.filter(id__in=subject_ids).values_list('id', flat=True))
            if len(valid_subject_ids) != len(subject_ids):
                return Response(
                    {"error": "One or more subject IDs are invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the user
            self.perform_create(serializer)
            
            # Assign subjects to the teacher
            teacher = serializer.instance
            for subject_id in subject_ids:
                subject = Subject.objects.get(id=subject_id)
                subject.teacher = teacher
                subject.save()
                
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        # For non-teacher users, proceed normally
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'], url_path='change-username')
    def change_username(self, request, pk=None):
        requesting_user = request.user
        target_user = self.get_object()
        new_username = request.data.get('username')

        if not new_username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=new_username).exclude(id=target_user.id).exists():
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        # Permission logic for changing username
        if requesting_user.role == 'admin':
            pass  # Admin can change any username
        elif requesting_user.role == 'teacher':
            if target_user.role != 'student':
                return Response({"error": "Teachers can only change usernames of students."}, status=status.HTTP_403_FORBIDDEN)
            if target_user.id == requesting_user.id:
                return Response({"error": "Teachers cannot change their own username."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "You are not allowed to change usernames."}, status=status.HTTP_403_FORBIDDEN)

        target_user.username = new_username
        target_user.save()
        return Response({"message": "Username updated successfully.", "username": target_user.username}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        requesting_user = request.user
        target_user = self.get_object()

        # Check permissions
        if requesting_user.role == 'admin':
            # Admin can delete any user
            pass
        elif requesting_user.role == 'teacher':
            if target_user.role != 'student':
                raise PermissionDenied("Teachers can only delete student users.")
        else:
            raise PermissionDenied("You do not have permission to delete users.")
            
        # Perform soft delete
        target_user.delete()  # This calls our custom delete method
        
        return Response(
            {"message": f"User {target_user.username} has been successfully deleted."},
            status=status.HTTP_200_OK
        )
        
    @action(detail=True, methods=['post'], url_path='restore')
    def restore_user(self, request, pk=None):
        """Restore a soft-deleted user"""
        # Only admins can restore users
        if request.user.role != 'admin':
            raise PermissionDenied("Only administrators can restore users.")
            
        try:
            # Get the user including deleted ones
            user_to_restore = User.objects.get(pk=pk)
            
            if not user_to_restore.is_deleted:
                return Response(
                    {"message": "This user is not deleted."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user_to_restore.restore()  # This calls our custom restore method
            
            return Response(
                {"message": f"User {user_to_restore.username} has been successfully restored."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
            
    @action(detail=False, methods=['get'], url_path='deleted')
    def deleted_users(self, request):
        """Get a list of soft-deleted users (admin only)"""
        if request.user.role != 'admin':
            raise PermissionDenied("Only administrators can view deleted users.")
            
        deleted_users = User.objects.filter(is_deleted=True)
        serializer = self.get_serializer(deleted_users, many=True)
        
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='profile')
    def get_profile(self, request, pk=None):
        user = self.get_object()
        
        # Check permissions
        if request.user.role == 'student' and request.user.id != user.id:
            return Response(
                {"error": "You can only access your own profile"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.role == 'teacher':
            # Teachers can access profiles of students in their subjects
            if user.role != 'student':
                return Response(
                    {"error": "Teachers can only access student profiles"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if this student is in any of the teacher's subjects
            student_in_teacher_subjects = StudentProfile.objects.filter(
                user=user,
                subjects__teacher=request.user
            ).exists()
            
            if not student_in_teacher_subjects:
                return Response(
                    {"error": "This student is not in any of your subjects"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        try:
            # Get or create the profile
            profile, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={'education_level': 'Not specified'}
            )
            
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"Failed to get profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
