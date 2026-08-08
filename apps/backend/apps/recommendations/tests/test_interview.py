from apps.recommendations.services.interview_service import (
    calculate_interview_readiness,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class InterviewReadinessTest(
    RecommendationsBaseTestCase,
):

    def test_interview_readiness_structure(self):
        result = calculate_interview_readiness(
            self.profile,
        )

        self.assertIn(
            "score",
            result,
        )

        self.assertIn(
            "level",
            result,
        )

        self.assertIn(
            "breakdown",
            result,
        )

        self.assertIn(
            "recommendations",
            result,
        )

    def test_score_is_between_zero_and_hundred(self):
        result = calculate_interview_readiness(
            self.profile,
        )

        self.assertGreaterEqual(
            result["score"],
            0,
        )

        self.assertLessEqual(
            result["score"],
            100,
        )

    def test_empty_profile_needs_improvement(self):
        result = calculate_interview_readiness(
            self.profile,
        )

        self.assertEqual(
            result["score"],
            0,
        )

        self.assertEqual(
            result["level"],
            "needs_improvement",
        )

        self.assertTrue(
            result["recommendations"],
        )