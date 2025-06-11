from rest_framework import viewsets, permissions
from .models import StudentProfile, Marks
from .serializers import StudentProfileSerializer, MarksSerializer
from users.permissions import IsTeacher, IsStudent

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsTeacher()]
        if self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsTeacher()]
        return [permissions.IsAuthenticated()]
