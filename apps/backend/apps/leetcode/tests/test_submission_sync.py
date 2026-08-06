from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeSubmission,
)
from apps.leetcode.tests.base import BaseLeetCodeAPITestCase


class SubmissionSyncAPITest(BaseLeetCodeAPITestCase):

    def setUp(self):
        super().setUp()

        self.profile = LeetCodeProfile.objects.create(
            user=self.user,
            username="test_leetcode_user",
        )

    @patch(
        "apps.leetcode.services.submission_service."
        "LeetCodeClient.get_recent_submissions"
    )
    def test_submission_sync_success(
        self,
        mock_recent_submissions,
    ):
        mock_recent_submissions.return_value = [
            {
                "id": "1001",
                "title": "Two Sum",
                "titleSlug": "two-sum",
                "timestamp": "1700000000",
                "lang": "python3",
            },
            {
                "id": "1002",
                "title": "Valid Parentheses",
                "titleSlug": "valid-parentheses",
                "timestamp": "1700000500",
                "lang": "python3",
            },
        ]

        response = self.client.post(
            reverse("leetcode_submissions_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["created_count"],
            2,
        )

        self.assertEqual(
            LeetCodeSubmission.objects.count(),
            2,
        )

    @patch(
        "apps.leetcode.services.submission_service."
        "LeetCodeClient.get_recent_submissions"
    )
    def test_duplicate_submissions_not_created(
        self,
        mock_recent_submissions,
    ):
        mock_recent_submissions.return_value = [
            {
                "id": "1001",
                "title": "Two Sum",
                "titleSlug": "two-sum",
                "timestamp": "1700000000",
                "lang": "python3",
            },
        ]

        self.client.post(
            reverse("leetcode_submissions_sync"),
            {},
            format="json",
        )

        response = self.client.post(
            reverse("leetcode_submissions_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["created_count"],
            0,
        )

        self.assertEqual(
            LeetCodeSubmission.objects.count(),
            1,
        )

    def test_sync_requires_authentication(self):
        self.client.credentials()

        response = self.client.post(
            reverse("leetcode_submissions_sync"),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_sync_without_connected_profile(self):
        self.profile.delete()

        response = self.client.post(
            reverse("leetcode_submissions_sync"),
            {},
            format="json",
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