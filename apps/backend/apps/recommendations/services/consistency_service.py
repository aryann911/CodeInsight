from datetime import timedelta

from django.utils import timezone

from apps.analytics.models import DailyStatistics
from apps.analytics.services.analytics_service import (
    get_streak_statistics,
)
from apps.leetcode.models import LeetCodeProfile


def calculate_consistency_score(
    profile: LeetCodeProfile,
) -> dict:
    """
    Calculate a 0-100 coding consistency score.

    Components:

    - Recent activity:   40 points
    - Current streak:    30 points
    - Longest streak:    20 points
    - Stability:         10 points
    """

    today = timezone.localdate()

    streak = get_streak_statistics(profile)

    current_streak = streak.get(
        "current_streak",
        0,
    )

    longest_streak = streak.get(
        "longest_streak",
        0,
    )

    recent_active_days = _get_recent_active_days(
        profile=profile,
        today=today,
    )

    recent_score = _calculate_recent_activity_score(
        recent_active_days,
    )

    current_streak_score = min(
        30,
        current_streak * 3,
    )

    longest_streak_score = min(
        20,
        longest_streak * 2,
    )

    stability_score = _calculate_stability_score(
        recent_active_days,
    )

    total_score = min(
        100,
        recent_score
        + current_streak_score
        + longest_streak_score
        + stability_score,
    )

    return {
        "score": total_score,
        "level": _get_consistency_level(
            total_score,
        ),
        "breakdown": {
            "recent_activity": recent_score,
            "current_streak": current_streak_score,
            "longest_streak": longest_streak_score,
            "stability": stability_score,
        },
        "metrics": {
            "recent_active_days": recent_active_days,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        },
        "recommendations": _build_recommendations(
            recent_active_days=recent_active_days,
            current_streak=current_streak,
            longest_streak=longest_streak,
            score=total_score,
        ),
    }


def _get_recent_active_days(
    profile: LeetCodeProfile,
    today,
) -> int:
    """
    Count active solving days during the last 30 days.
    """

    start_date = today - timedelta(days=29)

    return (
        DailyStatistics.objects.filter(
            profile=profile,
            date__gte=start_date,
            date__lte=today,
            solved_count__gt=0,
        )
        .values("date")
        .distinct()
        .count()
    )


def _calculate_recent_activity_score(
    active_days: int,
) -> int:
    """
    Calculate up to 40 points from recent activity.

    30 active days = maximum score.
    """

    return min(
        40,
        round((active_days / 30) * 40),
    )


def _calculate_stability_score(
    active_days: int,
) -> int:
    """
    Calculate up to 10 points based on
    regular activity during the last 30 days.
    """

    if active_days >= 25:
        return 10

    if active_days >= 20:
        return 8

    if active_days >= 15:
        return 6

    if active_days >= 10:
        return 4

    if active_days >= 5:
        return 2

    return 0


def _get_consistency_level(
    score: int,
) -> str:
    """
    Convert score into a consistency level.
    """

    if score >= 80:
        return "excellent"

    if score >= 60:
        return "strong"

    if score >= 40:
        return "developing"

    if score >= 20:
        return "inconsistent"

    return "needs_improvement"


def _build_recommendations(
    recent_active_days: int,
    current_streak: int,
    longest_streak: int,
    score: int,
) -> list[str]:
    """
    Generate actionable consistency recommendations.
    """

    recommendations = []

    if recent_active_days < 10:
        recommendations.append(
            "Try to solve at least one problem "
            "on most days."
        )

    if current_streak < 3:
        recommendations.append(
            "Build a small daily solving streak."
        )

    if longest_streak < 7:
        recommendations.append(
            "Aim for your first seven-day streak."
        )

    if score >= 80:
        recommendations.append(
            "Excellent consistency. Maintain your routine."
        )

    return recommendations