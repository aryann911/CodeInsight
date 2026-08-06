from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.tests.base import BaseAPITestCase


class CurrentUserAPITest(BaseAPITestCase):

    def test_current_user_success(self):
        url = reverse("current_user")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["username"],
            self.user.username,
        )

        self.assertEqual(
            response.data["data"]["email"],
            self.user.email,
        )

    def test_current_user_without_token(self):
        url = reverse("current_user")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            )