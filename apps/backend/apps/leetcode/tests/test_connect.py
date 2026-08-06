from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from apps.leetcode.clients.leetcode_client import (
    LeetCodeUserNotFoundError,
)
from apps.leetcode.models import LeetCodeProfile
from apps.leetcode.tests.base import BaseLeetCodeAPITestCase


class ConnectLeetCodeAPITest(BaseLeetCodeAPITestCase):

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_connect_leetcode_success(self, mock_get_profile):
        mock_get_profile.return_value = {
            "username": "test_leetcode_user",
            "profile": {
                "ranking": 50000,
                "reputation": 10,
            },
            "submitStatsGlobal": {
                "acSubmissionNum": [
                    {
                        "difficulty": "All",
                        "count": 400,
                    },
                    {
                        "difficulty": "Easy",
                        "count": 150,
                    },
                    {
                        "difficulty": "Medium",
                        "count": 200,
                    },
                    {
                        "difficulty": "Hard",
                        "count": 50,
                    },
                ]
            },
        }

        url = reverse("leetcode_connect")

        response = self.client.post(
            url,
            {
                "username": "test_leetcode_user",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["username"],
            "test_leetcode_user",
        )

        self.assertEqual(
            response.data["data"]["total_solved"],
            400,
        )

        self.assertEqual(
            response.data["data"]["easy_solved"],
            150,
        )

        self.assertEqual(
            response.data["data"]["medium_solved"],
            200,
        )

        self.assertEqual(
            response.data["data"]["hard_solved"],
            50,
        )

        self.assertTrue(
            LeetCodeProfile.objects.filter(
                user=self.user
            ).exists()
        )

        mock_get_profile.assert_called_once_with(
            "test_leetcode_user"
        )

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_connect_invalid_leetcode_username(
        self,
        mock_get_profile,
    ):
        mock_get_profile.side_effect = (
            LeetCodeUserNotFoundError(
                "LeetCode user not found."
            )
        )

        response = self.client.post(
            reverse("leetcode_connect"),
            {
                "username": "does_not_exist_123456",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "LeetCode user not found.",
        )

        self.assertFalse(
            LeetCodeProfile.objects.filter(
                user=self.user
            ).exists()
        )

    def test_connect_requires_authentication(self):
        self.client.credentials()

        response = self.client.post(
            reverse("leetcode_connect"),
            {
                "username": "test_leetcode_user",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch(
        "apps.leetcode.services.profile_service."
        "LeetCodeClient.get_user_profile"
    )
    def test_user_cannot_connect_second_profile(
        self,
        mock_get_profile,
    ):
        self.create_leetcode_profile()

        response = self.client.post(
            reverse("leetcode_connect"),
            {
                "username": "another_leetcode_user",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "A LeetCode account is already connected to this user.",
        )

        # External API should never be called because
        # we already know this user has a connected profile.
        mock_get_profile.assert_not_called()

    def test_connect_missing_username(self):
        response = self.client.post(
            reverse("leetcode_connect"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])