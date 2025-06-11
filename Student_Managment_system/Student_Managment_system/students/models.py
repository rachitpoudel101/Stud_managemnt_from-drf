from django.db import models
from users.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=100, blank=True)

class Marks(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.FloatField()
    