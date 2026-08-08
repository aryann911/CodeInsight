from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.leetcode.models import LeetCodeProfile

User = get_user_model()


class RecommendationsBaseTestCase(APITestCase):
    """
    Base test case for recommendation tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123!",
        )

        self.profile = LeetCodeProfile.objects.create(
            user=self.user,
            username="leetcode_user",
        )

        self.client.force_authenticate(
            user=self.user,
        )