from datetime import timedelta

from django.utils import timezone

from apps.analytics.models import DailyStatistics
from apps.recommendations.services.consistency_service import (
    calculate_consistency_score,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class CodingConsistencyTest(
    RecommendationsBaseTestCase,
):

    def test_consistency_structure(self):
        result = calculate_consistency_score(
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
            "metrics",
            result,
        )

        self.assertIn(
            "recommendations",
            result,
        )

    def test_score_is_between_zero_and_hundred(self):
        result = calculate_consistency_score(
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

    def test_active_days_are_counted(self):
        today = timezone.localdate()

        for days_ago in range(5):
            DailyStatistics.objects.create(
                profile=self.profile,
                date=today - timedelta(
                    days=days_ago,
                ),
                solved_count=2,
            )

        result = calculate_consistency_score(
            self.profile,
        )

        self.assertEqual(
            result["metrics"]["recent_active_days"],
            5,
        )

        self.assertGreater(
            result["score"],
            0,
        )

    def test_empty_profile_has_zero_score(self):
        result = calculate_consistency_score(
            self.profile,
        )

        self.assertEqual(
            result["score"],
            0,
        )

        self.assertEqual(
            result["metrics"]["recent_active_days"],
            0,
        )

        self.assertEqual(
            result["metrics"]["current_streak"],
            0,
        )

        self.assertEqual(
            result["metrics"]["longest_streak"],
            0,
        )