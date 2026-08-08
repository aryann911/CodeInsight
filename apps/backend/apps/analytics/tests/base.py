from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeSubmission,
)
from apps.analytics.models import DailyStatistics

User = get_user_model()


class AnalyticsBaseTestCase(APITestCase):
    """
    Base class for analytics tests.
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
            total_solved=100,
        )

        self.client.force_authenticate(self.user)