from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status

from apps.authentication.tests.base import BaseAPITestCase


class ResetPasswordAPITest(BaseAPITestCase):

    def setUp(self):
        super().setUp()

        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    def test_reset_password_success(self):
        response = self.client.post(
            reverse("reset_password"),
            {
                "uid": self.uid,
                "token": self.token,
                "new_password": "NewStrongPassword123",
                "confirm_password": "NewStrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

    def test_reset_password_invalid_token(self):
        response = self.client.post(
            reverse("reset_password"),
            {
                "uid": self.uid,
                "token": "invalid-token",
                "new_password": "NewStrongPassword123",
                "confirm_password": "NewStrongPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

    def test_reset_password_password_mismatch(self):
        response = self.client.post(
            reverse("reset_password"),
            {
                "uid": self.uid,
                "token": self.token,
                "new_password": "NewStrongPassword123",
                "confirm_password": "DifferentPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

    def test_reset_password_missing_fields(self):
        response = self.client.post(
            reverse("reset_password"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])