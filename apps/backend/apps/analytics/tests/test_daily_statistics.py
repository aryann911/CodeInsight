from datetime import date

from apps.analytics.models import DailyStatistics
from apps.analytics.tests.base import AnalyticsBaseTestCase


class DailyStatisticsTest(
    AnalyticsBaseTestCase,
):

    def test_create_daily_statistics(self):

        stat = DailyStatistics.objects.create(
            profile=self.profile,
            date=date.today(),
            solved_count=5,
        )

        self.assertEqual(
            stat.solved_count,
            5,
        )