from django.db.models import Count

from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeTopic,
)


def get_topic_statistics(
    profile: LeetCodeProfile,
):
    """
    Return submission counts grouped by LeetCode topic.
    """

    return (
        LeetCodeTopic.objects.filter(
            questions__submissions__profile=profile,
        )
        .annotate(
            submission_count=Count(
                "questions__submissions",
                distinct=True,
            ),
        )
        .order_by(
            "-submission_count",
            "name",
        )
    )