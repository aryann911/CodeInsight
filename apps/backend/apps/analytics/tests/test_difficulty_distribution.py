from apps.analytics.services.analytics_service import (
    get_difficulty_distribution,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class DifficultyDistributionTest(
    AnalyticsBaseTestCase,
):

    def test_distribution(self):

        result = get_difficulty_distribution(
            self.profile,
        )

        self.assertIn(
            "total",
            result,
        )