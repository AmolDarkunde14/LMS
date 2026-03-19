from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserViewSet, MemberProfileViewSet

router = DefaultRouter()
# /api/users/manage/
router.register(r'manage', UserViewSet, basename='manage-users')
# /api/users/members/
router.register(r'members', MemberProfileViewSet, basename='members')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
