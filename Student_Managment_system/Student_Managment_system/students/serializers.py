from rest_framework import serializers
from .models import StudentProfile, Marks, Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    marks = MarksSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'education_level', 'subjects', 'marks']
