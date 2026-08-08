from apps.analytics.services.analytics_service import (
    get_monthly_statistics,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class MonthlyStatisticsTest(
    AnalyticsBaseTestCase,
):

    def test_monthly_statistics(self):

        result = get_monthly_statistics(
            self.profile,
        )

        self.assertIn(
            "solved_count",
            result,
        )