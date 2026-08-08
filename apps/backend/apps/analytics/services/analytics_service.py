from collections import defaultdict

from django.db import transaction
from django.db.models import Count

from apps.analytics.models import DailyStatistics
from apps.leetcode.models import LeetCodeProfile


def rebuild_daily_statistics(profile: LeetCodeProfile):
    """
    Rebuild daily statistics from stored submissions.
    """

    DailyStatistics.objects.filter(
        profile=profile
    ).delete()

    grouped = defaultdict(list)

    submissions = profile.submissions.all()

    for submission in submissions:
        grouped[
            submission.submitted_at.date()
        ].append(submission)

    with transaction.atomic():

        for date, submissions in grouped.items():

            easy = 0
            medium = 0
            hard = 0

            for submission in submissions:

                difficulty = getattr(
                    submission,
                    "difficulty",
                    None,
                )

                if difficulty == "Easy":
                    easy += 1

                elif difficulty == "Medium":
                    medium += 1

                elif difficulty == "Hard":
                    hard += 1

            DailyStatistics.objects.create(
                profile=profile,
                date=date,
                solved_count=len(submissions),
                easy_count=easy,
                medium_count=medium,
                hard_count=hard,
            )


from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from apps.analytics.selectors.analytics_selector import (
    get_daily_statistics_between,
)


def get_weekly_statistics(profile):
    """
    Return aggregated statistics for the last seven days.
    """

    end_date = timezone.localdate()
    start_date = end_date - timedelta(days=6)

    statistics = get_daily_statistics_between(
        profile=profile,
        start_date=start_date,
        end_date=end_date,
    )

    summary = statistics.aggregate(
        solved_count=Sum("solved_count"),
        easy_count=Sum("easy_count"),
        medium_count=Sum("medium_count"),
        hard_count=Sum("hard_count"),
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "days": statistics.count(),
        "solved_count": summary["solved_count"] or 0,
        "easy_count": summary["easy_count"] or 0,
        "medium_count": summary["medium_count"] or 0,
        "hard_count": summary["hard_count"] or 0,
    }
def get_monthly_statistics(profile):
    """
    Return aggregated statistics for the last thirty days.
    """

    end_date = timezone.localdate()
    start_date = end_date - timedelta(days=29)

    statistics = get_daily_statistics_between(
        profile=profile,
        start_date=start_date,
        end_date=end_date,
    )

    summary = statistics.aggregate(
        solved_count=Sum("solved_count"),
        easy_count=Sum("easy_count"),
        medium_count=Sum("medium_count"),
        hard_count=Sum("hard_count"),
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "days": statistics.count(),
        "solved_count": summary["solved_count"] or 0,
        "easy_count": summary["easy_count"] or 0,
        "medium_count": summary["medium_count"] or 0,
        "hard_count": summary["hard_count"] or 0,
    }
def get_difficulty_distribution(profile):
    """
    Return the cumulative solved-problem distribution by difficulty.
    """

    summary = (
        DailyStatistics.objects.filter(
            profile=profile,
        ).aggregate(
            easy=Sum("easy_count"),
            medium=Sum("medium_count"),
            hard=Sum("hard_count"),
        )
    )

    easy = summary["easy"] or 0
    medium = summary["medium"] or 0
    hard = summary["hard"] or 0

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "total": easy + medium + hard,
    }
def get_language_statistics(profile):
    """
    Return the distribution of programming languages
    used in LeetCode submissions.
    """

    queryset = (
        profile.submissions.values("language")
        .annotate(
            count=Count("id"),
        )
        .order_by(
            "-count",
            "language",
        )
    )

    return [
        {
            "language": item["language"] or "Unknown",
            "count": item["count"],
        }
        for item in queryset
    ]
def get_activity_heatmap(
    profile,
    days: int = 365,
):
    """
    Return daily activity formatted for a contribution heatmap.
    """

    end_date = timezone.localdate()
    start_date = end_date - timedelta(days=days - 1)

    statistics = get_daily_statistics_between(
        profile=profile,
        start_date=start_date,
        end_date=end_date,
    )

    return [
        {
            "date": stat.date.isoformat(),
            "count": stat.solved_count,
        }
        for stat in statistics
    ]
def get_streak_statistics(profile):
    """
    Calculate the current and longest solving streak.
    """

    statistics = list(
        profile.daily_statistics.order_by("date")
    )

    if not statistics:
        return {
            "current_streak": 0,
            "longest_streak": 0,
        }

    longest_streak = 0
    current_run = 0
    previous_date = None

    for stat in statistics:

        if stat.solved_count <= 0:
            current_run = 0
            previous_date = stat.date
            continue

        if previous_date is None:
            current_run = 1

        elif (stat.date - previous_date).days == 1:
            current_run += 1

        else:
            current_run = 1

        longest_streak = max(
            longest_streak,
            current_run,
        )

        previous_date = stat.date

    today = timezone.localdate()

    current_streak = 0

    if statistics:

        latest = statistics[-1]

        if (today - latest.date).days <= 1:

            current_streak = 1

            previous_date = latest.date

            for stat in reversed(statistics[:-1]):

                if stat.solved_count <= 0:
                    break

                if (
                    previous_date - stat.date
                ).days == 1:

                    current_streak += 1
                    previous_date = stat.date

                else:
                    break

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
    }