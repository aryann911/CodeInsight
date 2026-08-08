from apps.leetcode.models import LeetCodeProfile

from apps.recommendations.selectors.topic_selector import (
    get_topic_statistics,
)


def analyze_topics(
    profile: LeetCodeProfile,
) -> list[dict]:
    """
    Analyze a user's LeetCode topic activity.

    Returns topic-level submission statistics.
    """

    topics = get_topic_statistics(profile)

    return [
        {
            "topic": topic.name,
            "slug": topic.slug,
            "submission_count": topic.submission_count,
        }
        for topic in topics
    ]