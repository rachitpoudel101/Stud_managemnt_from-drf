from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_deleted = models.BooleanField(default=False)
    
    def delete(self, using=None, keep_parents=False):
        """Override delete to perform soft delete"""
        self.is_deleted = True
        self.is_active = False  # Prevent login
        self.save()
        
    def restore(self):
        """Restore a soft-deleted user"""
        self.is_deleted = False
        self.is_active = True
        self.save()
