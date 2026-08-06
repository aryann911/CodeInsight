from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.tests.base import BaseAPITestCase


class RefreshTokenAPITest(BaseAPITestCase):

    def test_refresh_token_success(self):
        url = reverse("token_refresh")

        refresh = RefreshToken.for_user(self.user)

        payload = {
            "refresh": str(refresh),
     }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])
        self.assertEqual(
        response.data["message"],
        "Access token refreshed successfully.",
        )

        self.assertIn("access", response.data["data"])

    def test_refresh_token_invalid(self):
        url = reverse("token_refresh")

        payload = {
        "refresh": "invalid-token",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(response.data["success"])

    def test_refresh_token_missing(self):
        url = reverse("token_refresh")

        response = self.client.post(
        url,
        {},
        format="json",
        )

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])