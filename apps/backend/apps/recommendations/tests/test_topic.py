from apps.recommendations.services.topic_service import (
    analyze_topics,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class TopicAnalysisTest(
    RecommendationsBaseTestCase,
):
    def test_topic_analysis_returns_list(self):
        result = analyze_topics(
            self.profile,
        )

        self.assertIsInstance(
            result,
            list,
        )