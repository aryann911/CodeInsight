from django.urls import reverse
from rest_framework import status

from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class RecommendationAPITest(
    RecommendationsBaseTestCase,
):

    def test_recommendation_list_requires_authentication(self):
        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            reverse("recommendation-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_recommendation_list(self):
        response = self.client.get(
            reverse("recommendation-list"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_study_plan(self):
        response = self.client.get(
            reverse("weekly-study-plan"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_interview_readiness(self):
        response = self.client.get(
            reverse("interview-readiness"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_consistency(self):
        response = self.client.get(
            reverse("coding-consistency"),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )