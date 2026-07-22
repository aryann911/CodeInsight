from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(validated_data: dict):
    """
    Create and return a new user.
    """

    validated_data = validated_data.copy()

    validated_data.pop("password_confirm")

    password = validated_data.pop("password")

    user = User(**validated_data)
    user.set_password(password)
    user.save()

    return user