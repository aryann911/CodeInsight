from django.contrib.auth import get_user_model

User = get_user_model()


def register_user(validated_data: dict):
    """
    Create and return a new user.
    """

    data = validated_data.copy()

    # Remove fields that are not stored
    data.pop("password_confirm")

    password = data.pop("password")

    user = User(**data)
    user.set_password(password)
    user.save()

    return user