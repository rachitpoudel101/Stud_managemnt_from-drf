from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdmin

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
        if self.action in ['update', 'partial_update', 'retrieve', 'list', 'change_username']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
        if user.role == 'admin':
            return User.objects.all()
        if user.role == 'teacher':
            # Teachers can see only student users
            return User.objects.filter(role='student')
        # Students can only see themselves
        return User.objects.filter(id=user.id)

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

        if requesting_user.role == 'admin':
            return super().destroy(request, *args, **kwargs)

        if requesting_user.role == 'teacher':
            if target_user.role != 'student':
                raise PermissionDenied("Teachers can only delete student users.")
            return super().destroy(request, *args, **kwargs)

        raise PermissionDenied("You do not have permission to delete users.")
