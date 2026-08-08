from datetime import date

from apps.analytics.models import DailyStatistics
from apps.leetcode.models import LeetCodeProfile


def get_daily_statistics(
    profile: LeetCodeProfile,
):
    """
    Return all daily statistics for a profile.
    """

    return (
        DailyStatistics.objects.filter(
            profile=profile,
        )
        .order_by("date")
    )


def get_daily_statistics_between(
    profile: LeetCodeProfile,
    start_date: date,
    end_date: date,
):
    """
    Return daily statistics within a date range.
    """

    return (
        DailyStatistics.objects.filter(
            profile=profile,
            date__range=(
                start_date,
                end_date,
            ),
        )
        .order_by("date")
    )