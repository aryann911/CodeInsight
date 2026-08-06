from django.urls import reverse
from rest_framework import status

from apps.leetcode.models import LeetCodeProfile
from apps.leetcode.tests.base import BaseLeetCodeAPITestCase


class DisconnectLeetCodeAPITest(BaseLeetCodeAPITestCase):

    def test_disconnect_leetcode_success(self):
        self.create_leetcode_profile()

        response = self.client.delete(
            reverse("leetcode_disconnect")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "LeetCode account disconnected successfully.",
        )

        self.assertFalse(
            LeetCodeProfile.objects.filter(
                user=self.user
            ).exists()
        )

    def test_disconnect_without_connected_profile(self):
        response = self.client.delete(
            reverse("leetcode_disconnect")
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

    def test_disconnect_requires_authentication(self):
        self.create_leetcode_profile()

        # Remove JWT authentication
        self.client.credentials()

        response = self.client.delete(
            reverse("leetcode_disconnect")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        # Profile must NOT be deleted
        self.assertTrue(
            LeetCodeProfile.objects.filter(
                user=self.user
            ).exists()
        )