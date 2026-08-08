from apps.recommendations.services.difficulty_service import (
    analyze_difficulty,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class DifficultyAnalysisTest(
    RecommendationsBaseTestCase,
):

    def test_difficulty_analysis_returns_expected_structure(self):
        result = analyze_difficulty(
            self.profile,
        )

        self.assertIn(
            "total",
            result,
        )

        self.assertIn(
            "distribution",
            result,
        )

        self.assertIn(
            "assessment",
            result,
        )

        self.assertIn(
            "easy",
            result["distribution"],
        )

        self.assertIn(
            "medium",
            result["distribution"],
        )

        self.assertIn(
            "hard",
            result["distribution"],
        )

    def test_empty_profile_has_insufficient_data(self):
        result = analyze_difficulty(
            self.profile,
        )

        self.assertEqual(
            result["total"],
            0,
        )

        self.assertEqual(
            result["assessment"]["level"],
            "insufficient_data",
        )