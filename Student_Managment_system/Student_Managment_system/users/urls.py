from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# No changes needed - just explaining the endpoints:

# For standard DELETE: 
# DELETE http://127.0.0.1:8000/api/users/{user_id}/

# For custom delete action:
# DELETE http://127.0.0.1:8000/api/users/{user_id}/remove_user/
