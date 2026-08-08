from django.utils import timezone

from apps.leetcode.models import LeetCodeSubmission
from apps.recommendations.models import Recommendation
from apps.recommendations.services.recommendation_service import (
    generate_recommendations,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class PersonalizedRecommendationTest(
    RecommendationsBaseTestCase,
):

    def test_generate_recommendations_returns_list(self):
        result = generate_recommendations(
            self.profile,
        )

        self.assertIsInstance(
            result,
            list,
        )

    def test_difficulty_recommendation_is_created(self):
        LeetCodeSubmission.objects.create(
            profile=self.profile,
            submission_id="submission-1",
            title="Two Sum",
            title_slug="two-sum",
            status="Accepted",
            language="python",
            difficulty="Easy",
            submitted_at=timezone.now(),
        )

        generate_recommendations(
            self.profile,
        )

        recommendations = Recommendation.objects.filter(
            user=self.user,
        )

        self.assertTrue(
            recommendations.exists()
        )