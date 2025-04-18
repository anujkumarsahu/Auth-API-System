from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)
from acounts.views import *
urlpatterns = [
    
    # If this file is already under path("api/", include("authapi.urls"))
    path('reset-password-confirm/<uid>/<token>/', SetResetNewPasswordView.as_view(), name='reset_password_confirm'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]