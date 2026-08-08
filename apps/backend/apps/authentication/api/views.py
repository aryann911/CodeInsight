from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema

from apps.authentication.api.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.authentication.services.auth_service import (
    authenticate_user,
    register_user,
)
from apps.common.responses import error_response, success_response

from apps.authentication.api.serializers import LogoutSerializer
from apps.authentication.services.auth_service import logout_user
from .serializers import ChangePasswordSerializer, RefreshTokenSerializer
from ..services.auth_service import change_password



@extend_schema(
    tags=["Authentication"],
    request=RegisterSerializer,
    responses={201: UserSerializer},
)
class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )


        try:
            user = register_user(serializer.validated_data)

            return success_response(
            message="User registered successfully.",
            data=UserSerializer(user).data,
            status_code=status.HTTP_201_CREATED,
        )

        except ValueError as exc:
            return error_response(
            message=str(exc),
            status_code=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    tags=["Authentication"],
    request=LoginSerializer,
    
)
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        data = authenticate_user(serializer.validated_data["user"])
        data["user"] = UserSerializer(data["user"]).data

        return success_response(
            message="Login successful.",
            data=data,
            status_code=status.HTTP_200_OK,
        )

@extend_schema(
    tags=["Authentication"],
    responses={200: UserSerializer},
)

class CurrentUserAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)

        return success_response(
            message="User profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
@extend_schema(
    tags=["Authentication"],
    request=LogoutSerializer,
)
class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            logout_user(serializer.validated_data["refresh"])
        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Logout successful.",
            data={},
            status_code=status.HTTP_200_OK,
        )
@extend_schema(
    tags=["Authentication"],
    request=ChangePasswordSerializer,
)
    
class ChangePasswordAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            change_password(
                user=request.user,
                old_password=serializer.validated_data["old_password"],
                new_password=serializer.validated_data["new_password"],
            )

            return success_response(
                message="Password changed successfully.",
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        

from .serializers import ForgotPasswordSerializer
from ..services.auth_service import forgot_password
@extend_schema(
    tags=["Authentication"],
    request=ForgotPasswordSerializer,
)
class ForgotPasswordAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        forgot_password(
            email=serializer.validated_data["email"],
        )

        return success_response(
            message=(
                "If an account with that email exists, "
                "a password reset link has been sent."
            ),
        )


from .serializers import ResetPasswordSerializer
from ..services.auth_service import reset_password

@extend_schema(
    tags=["Authentication"],
    request=ResetPasswordSerializer,
)
class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reset_password(
                uid=serializer.validated_data["uid"],
                token=serializer.validated_data["token"],
                new_password=serializer.validated_data["new_password"],
            )

            return success_response(
                message="Password has been reset successfully.",
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        

from rest_framework import status
from rest_framework.exceptions import ValidationError



from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)

from apps.authentication.api.serializers import RefreshTokenSerializer
from apps.authentication.services.auth_service import refresh_access_token


@extend_schema(
    tags=["Authentication"],
    request=RefreshTokenSerializer,
)
class RefreshTokenAPIView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            data = refresh_access_token(serializer)

            return success_response(
                message="Access token refreshed successfully.",
                data=data,
                status_code=status.HTTP_200_OK,
            )

        except ValidationError:
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except (InvalidToken, TokenError):
            return error_response(
                message="Invalid or expired refresh token.",
                errors={
                    "refresh": [
                        "Invalid or expired refresh token."
                    ]
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )