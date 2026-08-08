from apps.analytics.services.analytics_service import (
    get_streak_statistics,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class StreakStatisticsTest(
    AnalyticsBaseTestCase,
):

    def test_streak(self):

        result = get_streak_statistics(
            self.profile,
        )

        self.assertIn(
            "current_streak",
            result,
        )

        self.assertIn(
            "longest_streak",
            result,
        )