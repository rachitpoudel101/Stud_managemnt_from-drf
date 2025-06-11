from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet, MarksViewSet

router = DefaultRouter()
router.register('profiles', StudentProfileViewSet)
router.register('marks', MarksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

