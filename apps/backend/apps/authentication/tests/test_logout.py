from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.tests.base import BaseAPITestCase


class LogoutAPITest(BaseAPITestCase):

    def test_logout_success(self):
        url = reverse("logout")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

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
            "Logout successful.",
        )
    
    def test_logout_invalid_refresh_token(self):
        url = reverse("logout")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        payload = {
            "refresh": "invalid-token",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])
    
    def test_logout_missing_refresh_token(self):
        url = reverse("logout")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

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
    
    def test_logout_without_authentication(self):
        url = reverse("logout")

        response = self.client.post(url, {}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )