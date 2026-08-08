from django.urls import path

from apps.authentication.api.views import (
    ChangePasswordAPIView,
    CurrentUserAPIView,
    ForgotPasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshTokenAPIView,
    RegisterAPIView,
    ResetPasswordAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("me/", CurrentUserAPIView.as_view(), name="current_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot_password",
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path(
        "token/refresh/",
        RefreshTokenAPIView.as_view(),
        name="token_refresh",
    ),
]