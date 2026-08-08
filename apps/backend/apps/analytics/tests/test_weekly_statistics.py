from apps.analytics.services.analytics_service import (
    get_weekly_statistics,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class WeeklyStatisticsTest(
    AnalyticsBaseTestCase,
):

    def test_weekly_statistics(self):

        result = get_weekly_statistics(
            self.profile,
        )

        self.assertIn(
            "solved_count",
            result,
        )