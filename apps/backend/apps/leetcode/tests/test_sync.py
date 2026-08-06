from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.leetcode.tests.base import BaseLeetCodeAPITestCase


class SyncLeetCodeProfileAPITest(BaseLeetCodeAPITestCase):

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_sync_leetcode_profile_success(
        self,
        mock_get_profile,
    ):
        profile = self.create_leetcode_profile()

        # Make profile old enough to bypass 5-minute cooldown
        profile.last_synced_at = (
            timezone.now() - timedelta(minutes=6)
        )
        profile.save(update_fields=["last_synced_at"])

        mock_get_profile.return_value = {
            "username": "test_leetcode_user",
            "profile": {
                "ranking": 50000,
                "reputation": 20,
            },
            "submitStatsGlobal": {
                "acSubmissionNum": [
                    {
                        "difficulty": "All",
                        "count": 500,
                    },
                    {
                        "difficulty": "Easy",
                        "count": 200,
                    },
                    {
                        "difficulty": "Medium",
                        "count": 250,
                    },
                    {
                        "difficulty": "Hard",
                        "count": 50,
                    },
                ]
            },
        }

        response = self.client.post(
            reverse("leetcode_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "LeetCode profile synchronized successfully.",
        )

        # Reload from database
        profile.refresh_from_db()

        self.assertEqual(profile.ranking, 50000)
        self.assertEqual(profile.reputation, 20)
        self.assertEqual(profile.total_solved, 500)
        self.assertEqual(profile.easy_solved, 200)
        self.assertEqual(profile.medium_solved, 250)
        self.assertEqual(profile.hard_solved, 50)

        self.assertIsNotNone(
            profile.last_synced_at
        )

        mock_get_profile.assert_called_once_with(
            "test_leetcode_user"
        )

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_sync_cooldown(
        self,
        mock_get_profile,
    ):
        profile = self.create_leetcode_profile()

        # Profile was just synchronized
        profile.last_synced_at = timezone.now()
        profile.save(update_fields=["last_synced_at"])

        response = self.client.post(
            reverse("leetcode_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

        self.assertIn(
            "Profile was recently synchronized.",
            response.data["message"],
        )

        # Cooldown should stop the request BEFORE
        # contacting LeetCode.
        mock_get_profile.assert_not_called()

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_sync_without_connected_profile(
        self,
        mock_get_profile,
    ):
        response = self.client.post(
            reverse("leetcode_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "No LeetCode account is connected.",
        )

        mock_get_profile.assert_not_called()

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_sync_requires_authentication(
        self,
        mock_get_profile,
    ):
        self.create_leetcode_profile()

        self.client.credentials()

        response = self.client.post(
            reverse("leetcode_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        mock_get_profile.assert_not_called()