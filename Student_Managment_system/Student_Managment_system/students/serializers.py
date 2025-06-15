from rest_framework import serializers
from .models import StudentProfile, Marks, Subject
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
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'user_details', 'education_level', 'subjects', 'subject_details']
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
