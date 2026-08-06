from django.urls import reverse
from rest_framework import status

from apps.leetcode.tests.base import BaseLeetCodeAPITestCase


class LeetCodeProfileAPITest(BaseLeetCodeAPITestCase):

    def test_get_leetcode_profile_success(self):
        profile = self.create_leetcode_profile()

        response = self.client.get(
            reverse("leetcode_profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "LeetCode profile retrieved successfully.",
        )

        data = response.data["data"]

        self.assertEqual(
            data["id"],
            profile.id,
        )

        self.assertEqual(
            data["username"],
            "test_leetcode_user",
        )

        self.assertEqual(
            data["ranking"],
            100000,
        )

        self.assertEqual(
            data["total_solved"],
            300,
        )

        self.assertEqual(
            data["easy_solved"],
            120,
        )

        self.assertEqual(
            data["medium_solved"],
            150,
        )

        self.assertEqual(
            data["hard_solved"],
            30,
        )

    def test_get_profile_without_connected_account(self):
        response = self.client.get(
            reverse("leetcode_profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertFalse(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"],
            "No LeetCode account is connected.",
        )

    def test_get_profile_requires_authentication(self):
        self.create_leetcode_profile()

        # Remove JWT credentials
        self.client.credentials()

        response = self.client.get(
            reverse("leetcode_profile")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )