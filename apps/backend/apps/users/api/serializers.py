from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used to validate user registration data.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    password_confirm = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        )

    def validate_email(self, value: str) -> str:
        """
        Validate that the email is unique.
        """
        email = value.strip().lower()
        User = get_user_model()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return email

    def validate_username(self, value: str) -> str:
        """
        Validate that the username is unique.
        """
        username = value.strip()
        User = get_user_model()

        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )

        return username

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Validate matching passwords.
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm": "Passwords do not match."
                }
            )

        return attrs