from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.services.user_service import create_user

from apps.common.responses import error_response, success_response
from apps.users.api.serializers import RegisterSerializer

User = get_user_model()


class RegisterAPIView(APIView):
    """
    Register a new user.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        user = create_user(serializer.validated_data)

        return success_response(
            message="User registered successfully.",
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status_code=status.HTTP_201_CREATED,
        )