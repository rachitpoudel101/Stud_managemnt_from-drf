# Import User model
from django.db import models
from users.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_subjects',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education_level = models.CharField(max_length=100, blank=True)
    subjects = models.ManyToManyField(Subject, related_name='students')

class Marks(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject')
        verbose_name_plural = 'Marks'

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.marks}"
