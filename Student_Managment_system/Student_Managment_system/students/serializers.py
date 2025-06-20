from rest_framework import serializers
from .models import StudentProfile, Marks, Subject, notice, Assignment, StudentSubmission
from users.models import User

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher', 'teacher_name']
        read_only_fields = ['teacher_name']

class StudentProfileSerializer(serializers.ModelSerializer):
    user_details = UserBasicSerializer(source='user', read_only=True)
    subject_details = SubjectSerializer(source='subjects', many=True, read_only=True)
    grade_display = serializers.CharField(source='get_grade_display', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'user_details', 'education_level', 'grade', 'grade_display', 'subjects', 'subject_details']
        extra_kwargs = {
            'user': {'write_only': True}
        }

class MarksSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    student_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Marks
        fields = ['id', 'student', 'subject', 'marks', 'published', 'subject_name', 'student_name']
        
    def get_student_name(self, obj):
        user = obj.student.user
        return f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username


class NoticeSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = notice
        fields = ['id', 'title', 'content', 'created_at', 'created_by', 'updated_at', 'published', 'audience', 'created_by_name']
        read_only_fields = ['created_by']
        
    def get_created_by_name(self, obj):
        user = obj.created_by
        return f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username


class AssignmentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'created_at', 'created_by', 
                  'created_by_name', 'file', 'due_date', 'subject', 'subject_name',
                  'remarks', 'audience', 'published']
        read_only_fields = ['created_by', 'created_at']

class StudentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.user.username')
    assignment_title = serializers.ReadOnlyField(source='assignment.title')
    
    class Meta:
        model = StudentSubmission
        fields = ['id', 'assignment', 'assignment_title', 'student', 
                  'student_name', 'file', 'submitted_at', 'comments']
        read_only_fields = ['student', 'submitted_at']
    
    def update(self, instance, validated_data):
        # Handle file updates carefully - only update if a new file is provided
        if 'file' in validated_data and validated_data['file'] is not None:
            instance.file = validated_data['file']
        
        # Update other fields
        instance.comments = validated_data.get('comments', instance.comments)
        instance.save()
        return instance