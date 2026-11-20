from django.urls import path
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)


app_name = "users"


urlpatterns = [

    # User registration
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

        # Login - returns access and refresh tokens
        path(
        "auth/login/",
        TokenObtainPairView.as_view(
            permission_classes=[AllowAny]
        ),
        name="login",
    ),

    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(
            permission_classes=[AllowAny]
        ),
        name="token_refresh",
    ),

    # View / update authenticated user's profile
    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),
    path(
        "auth/change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path(
    "auth/logout/",
    LogoutAPIView.as_view(),
    name="logout",
),

]