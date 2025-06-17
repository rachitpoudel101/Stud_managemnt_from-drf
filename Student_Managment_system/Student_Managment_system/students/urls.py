from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet, StudentProfileViewSet, MarksViewSet, SubjectViewSet, AssignmentViewSet, StudentSubmissionViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'marks', MarksViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', StudentSubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
