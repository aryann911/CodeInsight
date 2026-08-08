from django.urls import reverse

from apps.analytics.tests.base import (
    AnalyticsBaseTestCase,
)


class DashboardAPITest(
    AnalyticsBaseTestCase,
):

    def test_dashboard(self):

        response = self.client.get(
            reverse(
                "analytics:dashboard",
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"],
        )