from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def register_user(validated_data: dict):
    """
    Create and return a new user.
    """
    data = validated_data.copy()

    data.pop("password_confirm")
    password = data.pop("password")

    user = User(**data)

    try:
        validate_password(password, user)
    except ValidationError as exc:
        raise ValueError(exc.messages)

    user.set_password(password)
    user.save()

    return user


def authenticate_user(user):
    """
    Generate JWT tokens for the authenticated user.
    """
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": user,
    }


def logout_user(refresh_token):
    """
    Blacklist a refresh token.
    """
    try:
        RefreshToken(refresh_token).blacklist()
    except TokenError:
        raise ValueError(
            "Invalid or expired refresh token."
        )


def change_password(
    user,
    old_password,
    new_password,
):
    """
    Change the password of an authenticated user.
    """

    if not user.check_password(old_password):
        raise ValueError(
            "Old password is incorrect."
        )

    if old_password == new_password:
        raise ValueError(
            "New password must be different from the old password."
        )

    try:
        validate_password(
            new_password,
            user,
        )
    except ValidationError as exc:
        raise ValueError(exc.messages)

    user.set_password(new_password)
    user.save(update_fields=["password"])


def forgot_password(email):
    """
    Generate a password reset link.
    """

    try:
        user = User.objects.get(
            email__iexact=email
        )
    except User.DoesNotExist:
        return None

    token = PasswordResetTokenGenerator().make_token(user)

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    reset_link = (
        f"{settings.FRONTEND_URL}"
        f"/reset-password/"
        f"?uid={uid}&token={token}"
    )

    print("\n" + "=" * 60)
    print("PASSWORD RESET LINK")
    print(reset_link)
    print("=" * 60 + "\n")

    return reset_link


def reset_password(
    uid,
    token,
    new_password,
):
    """
    Reset a user's password.
    """

    try:
        user_id = force_str(
            urlsafe_base64_decode(uid)
        )

        user = User.objects.get(
            pk=user_id
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
    ):
        raise ValueError(
            "Invalid reset link."
        )

    generator = PasswordResetTokenGenerator()

    if not generator.check_token(
        user,
        token,
    ):
        raise ValueError(
            "Reset link is invalid or has expired."
        )

    try:
        validate_password(
            new_password,
            user,
        )
    except ValidationError as exc:
        raise ValueError(exc.messages)

    user.set_password(new_password)
    user.save(update_fields=["password"])


def refresh_access_token(serializer):
    """
    Return validated refresh token data.
    """
    serializer.is_valid(
        raise_exception=True
    )
    return serializer.validated_data