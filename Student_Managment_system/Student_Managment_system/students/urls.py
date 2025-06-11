from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentProfileViewSet, MarksViewSet, SubjectViewSet

router = DefaultRouter()
router.register('students/profiles', StudentProfileViewSet)
router.register('students/marks', MarksViewSet, basename='marks')
router.register('subjects', SubjectViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
