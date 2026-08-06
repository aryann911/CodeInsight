from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.base import BaseAPITestCase


class ForgotPasswordAPITest(BaseAPITestCase):

    def test_forgot_password_success(self):
        response = self.client.post(
            reverse("forgot_password"),
            {
                "email": self.user.email,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "If an account with that email exists, a password reset link has been sent.",
        )

    def test_forgot_password_invalid_email(self):
        response = self.client.post(
            reverse("forgot_password"),
            {
                "email": "unknown@example.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "If an account with that email exists, a password reset link has been sent.",
        )

    def test_forgot_password_missing_email(self):
        response = self.client.post(
            reverse("forgot_password"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])