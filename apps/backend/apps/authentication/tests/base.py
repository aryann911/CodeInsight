from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


User = get_user_model()


class BaseAPITestCase(APITestCase):
    """
    Base class for authentication API tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123",
            first_name="Test",
            last_name="User",
        )