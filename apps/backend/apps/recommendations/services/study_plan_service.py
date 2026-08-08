from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.leetcode.models import LeetCodeProfile
from apps.recommendations.models import (
    Recommendation,
    WeeklyStudyPlan,
)
from apps.recommendations.services.difficulty_service import (
    analyze_difficulty,
)
from apps.recommendations.services.topic_service import (
    analyze_topics,
)


WEEKLY_PROBLEM_TARGET = 10
WEEKLY_MINUTES_TARGET = 300


def generate_weekly_study_plan(
    profile: LeetCodeProfile,
) -> WeeklyStudyPlan:
    """
    Generate or update the current week's study plan.
    """

    today = timezone.localdate()

    week_start = (
        today - timedelta(days=today.weekday())
    )

    week_end = week_start + timedelta(days=6)

    difficulty = analyze_difficulty(profile)
    topics = analyze_topics(profile)

    focus_difficulties = _select_difficulties(
        difficulty,
    )

    focus_topics = _select_topics(
        topics,
    )

    tasks = _build_tasks(
        focus_topics=focus_topics,
        focus_difficulties=focus_difficulties,
    )

    with transaction.atomic():
        plan, _ = WeeklyStudyPlan.objects.update_or_create(
            user=profile.user,
            week_start=week_start,
            defaults={
                "week_end": week_end,
                "target_problems": WEEKLY_PROBLEM_TARGET,
                "target_minutes": WEEKLY_MINUTES_TARGET,
                "focus_topics": focus_topics,
                "focus_difficulties": focus_difficulties,
                "tasks": tasks,
                "status": WeeklyStudyPlan.Status.ACTIVE,
            },
        )

    return plan


def _select_difficulties(
    difficulty: dict,
) -> list[str]:
    """
    Select difficulty levels for the weekly plan.
    """

    assessment = difficulty.get(
        "assessment",
        {},
    )

    level = assessment.get("level")

    if level == "easy_heavy":
        return ["Medium"]

    if level == "medium_low":
        return ["Medium"]

    if level == "hard_low":
        return ["Medium", "Hard"]

    if level == "insufficient_data":
        return ["Easy", "Medium"]

    return ["Medium"]


def _select_topics(
    topics: list[dict],
) -> list[str]:
    """
    Select under-practiced topics.
    """

    if not topics:
        return []

    low_activity_topics = [
        topic["topic"]
        for topic in topics
        if topic["submission_count"] <= 2
    ]

    return low_activity_topics[:2]


def _build_tasks(
    focus_topics: list[str],
    focus_difficulties: list[str],
) -> list[dict]:
    """
    Build a simple seven-day study schedule.
    """

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    tasks = []

    for index, day in enumerate(days):

        if index < 5:
            target = 2
        else:
            target = 1

        topic = (
            focus_topics[index % len(focus_topics)]
            if focus_topics
            else None
        )

        difficulty = (
            focus_difficulties[
                index % len(focus_difficulties)
            ]
            if focus_difficulties
            else "Medium"
        )

        tasks.append(
            {
                "day": day,
                "target_problems": target,
                "difficulty": difficulty,
                "topic": topic,
            }
        )

    return tasks