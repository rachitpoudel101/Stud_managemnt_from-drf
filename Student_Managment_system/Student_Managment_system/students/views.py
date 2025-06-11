from rest_framework import viewsets, permissions
from .models import StudentProfile, Marks, Subject
from .serializers import StudentProfileSerializer, MarksSerializer, SubjectSerializer
from users.permissions import IsTeacher

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return Marks.objects.filter(student__user=user)
        elif user.role == 'teacher':
            return Marks.objects.filter(subject__teacher=user)
        return Marks.objects.all()
