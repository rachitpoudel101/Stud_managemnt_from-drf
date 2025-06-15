from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from students.models import Subject

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Use the parent class's validate method to authenticate the user
        data = super().validate(attrs)
        
        # Get the refresh and access tokens
        refresh = self.get_token(self.user)
        
        # Add the tokens to the response
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        
        # Add user data to the response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role
        }
        
        return data

class UserSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Subject.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role', 'subjects']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        # Remove subjects field from validated_data if it exists
        subjects = validated_data.pop('subjects', None)
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        
        # The subjects will be handled in the view
        return user
