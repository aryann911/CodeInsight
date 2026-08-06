from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView

from apps.authentication.api.views import RegisterAPIView, LoginAPIView , CurrentUserAPIView, LogoutAPIView, ChangePasswordAPIView, ForgotPasswordAPIView, ResetPasswordAPIView , RefreshTokenAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    # path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserAPIView.as_view(), name="current_user"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path(
    "change-password/",
    ChangePasswordAPIView.as_view(),
    name="change_password",),
    path(
    "forgot-password/",
    ForgotPasswordAPIView.as_view(),
    name="forgot_password",),
    path(
    "reset-password/",
    ResetPasswordAPIView.as_view(),
    name="reset_password",),
    path(
    "token/refresh/",
    RefreshTokenAPIView.as_view(),
    name="token_refresh",),
]