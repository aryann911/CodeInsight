from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.base import BaseAPITestCase


class LoginAPITest(BaseAPITestCase):

    def test_login_success(self):
        url = reverse("login")

        payload = {
            "username": "testuser",
            "password": "StrongPassword123",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
        self.assertIn("user", response.data["data"])

    def test_login_invalid_username(self):
        url = reverse("login")

        payload = {
        "username": "wronguser",
        "password": "TestPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_login_wrong_password(self):
        url = reverse("login")

        payload = {
        "username": "testuser",
        "password": "WrongPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_login_missing_username(self):
        url = reverse("login")

        payload = {
        "password": "TestPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"]) 

    def test_login_missing_password(self):
        url = reverse("login")

        payload = {
        "username": "testuser",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])  

