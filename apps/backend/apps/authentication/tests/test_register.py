from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.base import BaseAPITestCase

User = get_user_model()


class RegisterAPITest(BaseAPITestCase):
    def test_register_user_success(self):
        url = reverse("register")

        payload = {
            "username": "john",
            "email": "john@example.com",
            "password": "StrongPassword123",
            "password_confirm": "StrongPassword123",
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(username="john").exists()
        )

        self.assertTrue(response.data["success"])

    def test_register_duplicate_username(self):
        url = reverse("register")

        payload = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "StrongPassword123",
            "password_confirm": "StrongPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])  


    def test_register_duplicate_email(self):
        url = reverse("register")

        payload = {
        "username": "anotheruser",
        "email": "test@example.com",
        "password": "StrongPassword123",
        "password_confirm": "StrongPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])


    def test_register_password_mismatch(self):
        url = reverse("register")

        payload = {
        "username": "john",
        "email": "john@example.com",
        "password": "StrongPassword123",
        "password_confirm": "WrongPassword123",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])

    def test_register_weak_password(self):
        url = reverse("register")

        payload = {
        "username": "john",
        "email": "john@example.com",
        "password": "12345678",
        "password_confirm": "12345678",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])    

