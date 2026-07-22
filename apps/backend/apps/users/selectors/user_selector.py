"""
User selectors.

Selectors contain read-only database queries.
"""

from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_email(email: str):
    """
    Return a user by email or None.
    """
    return User.objects.filter(email__iexact=email).first()


def get_user_by_username(username: str):
    """
    Return a user by username or None.
    """
    return User.objects.filter(username__iexact=username).first()


def get_user_by_id(user_id: int):
    """
    Return a user by ID or None.
    """
    return User.objects.filter(id=user_id).first()