from apps.analytics.services.analytics_service import (
    get_activity_heatmap,
)
from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class ActivityHeatmapTest(
    AnalyticsBaseTestCase,
):

    def test_heatmap(self):

        result = get_activity_heatmap(
            self.profile,
        )

        self.assertIsInstance(
            result,
            list,
        )