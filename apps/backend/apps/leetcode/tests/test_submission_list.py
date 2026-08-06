from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeSubmission,
)
from apps.leetcode.tests.base import BaseLeetCodeAPITestCase

User = get_user_model()


class SubmissionListAPITest(BaseLeetCodeAPITestCase):

    def setUp(self):
        super().setUp()

        self.profile = LeetCodeProfile.objects.create(
            user=self.user,
            username="test_leetcode_user",
        )

    def create_submission(self, submission_id, title):
        return LeetCodeSubmission.objects.create(
            profile=self.profile,
            submission_id=str(submission_id),
            title=title,
            title_slug=title.lower().replace(" ", "-"),
            status="Accepted",
            language="python3",
            submitted_at="2026-01-01T10:00:00Z",
        )

    def test_submission_list_success(self):
        self.create_submission("1001", "Two Sum")
        self.create_submission("1002", "Valid Parentheses")

        response = self.client.get(
            reverse("leetcode_submissions")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["count"],
            2,
        )

        self.assertEqual(
            len(response.data["data"]["results"]),
            2,
        )

    def test_empty_submission_list(self):
        response = self.client.get(
            reverse("leetcode_submissions")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["count"],
            0,
        )

    def test_requires_authentication(self):
        self.client.credentials()

        response = self.client.get(
            reverse("leetcode_submissions")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_isolation(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPassword123",
        )

        other_profile = LeetCodeProfile.objects.create(
            user=other_user,
            username="other_leetcode",
        )

        LeetCodeSubmission.objects.create(
            profile=other_profile,
            submission_id="9999",
            title="Hidden Problem",
            title_slug="hidden-problem",
            status="Accepted",
            language="python3",
            submitted_at="2026-01-01T10:00:00Z",
        )

        self.create_submission(
            "1001",
            "Two Sum",
        )

        response = self.client.get(
            reverse("leetcode_submissions")
        )

        self.assertEqual(
            response.data["data"]["count"],
            1,
        )

        self.assertEqual(
            response.data["data"]["results"][0]["title"],
            "Two Sum",
        )

    def test_pagination(self):
        for i in range(15):
            self.create_submission(
                str(i),
                f"Problem {i}",
            )

        response = self.client.get(
            reverse("leetcode_submissions")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["data"]["count"],
            15,
        )

        self.assertEqual(
            len(response.data["data"]["results"]),
            10,
        )