from apps.analytics.services.analytics_service import (
    get_language_statistics,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class LanguageStatisticsTest(
    AnalyticsBaseTestCase,
):

    def test_language_statistics(self):

        result = get_language_statistics(
            self.profile,
        )

        self.assertIsInstance(
            result,
            list,
        )