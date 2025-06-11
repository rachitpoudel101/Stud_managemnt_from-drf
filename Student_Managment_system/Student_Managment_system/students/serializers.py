from rest_framework import serializers
from .models import StudentProfile, Marks

class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    marks = MarksSerializer(many=True, read_only=True, source='marks_set')

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'education_level', 'marks']
