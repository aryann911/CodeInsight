from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.tests.base import BaseAPITestCase


class ChangePasswordAPITest(BaseAPITestCase):

    def test_change_password_success(self):
        url = reverse("change_password")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        payload = {
            "old_password": "StrongPassword123",
            "new_password": "NewStrongPassword123",
            "confirm_password": "NewStrongPassword123",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])
    def test_change_password_wrong_old_password(self):
        url = reverse("change_password")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        payload = {
        "old_password": "WrongPassword123",
        "new_password": "NewStrongPassword123",
        "confirm_password": "NewStrongPassword123",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])
    
    def test_change_password_mismatch(self):
        url = reverse("change_password")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        payload = {
        "old_password": "StrongPassword123",
        "new_password": "NewStrongPassword123",
        "confirm_password": "DifferentPassword123",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])
    
    def test_change_password_without_authentication(self):
        url = reverse("change_password")

        payload = {
        "old_password": "StrongPassword123",
        "new_password": "NewStrongPassword123",
        "confirm_password": "NewStrongPassword123",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED,
        )
    def test_change_password_weak_password(self):
        url = reverse("change_password")

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        payload = {
        "old_password": "StrongPassword123",
        "new_password": "12345678",
        "confirm_password": "12345678",
        }

        response = self.client.post(url, payload, format="json")
        print(response.status_code)
        print(response.data)

        self.assertEqual(
        response.status_code,
        status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])