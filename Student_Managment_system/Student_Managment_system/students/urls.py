from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet, MarksViewSet, SubjectViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'marks', MarksViewSet)
router.register(r'subjects', SubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
