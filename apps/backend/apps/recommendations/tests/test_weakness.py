from apps.recommendations.services.weakness_service import (
    detect_weaknesses,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class WeaknessDetectionTest(
    RecommendationsBaseTestCase,
):
    def test_detect_weaknesses_returns_list(self):
        weaknesses = detect_weaknesses(
            self.profile,
        )

        self.assertIsInstance(
            weaknesses,
            list,
        )