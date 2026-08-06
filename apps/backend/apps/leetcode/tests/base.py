from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.leetcode.models import LeetCodeProfile


User = get_user_model()


class BaseLeetCodeAPITestCase(APITestCase):
    """
    Base class for LeetCode API tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="leetcode_test_user",
            email="leetcode_test@example.com",
            password="StrongPassword123",
        )

        refresh = RefreshToken.for_user(self.user)

        self.access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

    def create_leetcode_profile(self, **kwargs):
        """
        Helper for creating a connected LeetCode profile.
        """

        defaults = {
            "username": "test_leetcode_user",
            "ranking": 100000,
            "reputation": 0,
            "total_solved": 300,
            "easy_solved": 120,
            "medium_solved": 150,
            "hard_solved": 30,
        }

        defaults.update(kwargs)

        return LeetCodeProfile.objects.create(
            user=self.user,
            **defaults,
        )