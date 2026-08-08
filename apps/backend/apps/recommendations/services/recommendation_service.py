from django.db import transaction
from django.utils import timezone

from apps.leetcode.models import LeetCodeProfile
from apps.recommendations.models import Recommendation

from apps.recommendations.services.difficulty_service import (
    analyze_difficulty,
)
from apps.recommendations.services.topic_service import (
    analyze_topics,
)
from apps.recommendations.services.weakness_service import (
    detect_weaknesses,
)


def generate_recommendations(
    profile: LeetCodeProfile,
) -> list[Recommendation]:
    """
    Generate personalized recommendations for a user.

    Recommendations are based on:
    - detected weaknesses
    - topic activity
    - difficulty distribution
    """

    weaknesses = detect_weaknesses(profile)
    difficulty = analyze_difficulty(profile)
    topics = analyze_topics(profile)

    recommendations = []

    recommendations.extend(
        _recommend_from_weaknesses(
            profile=profile,
            weaknesses=weaknesses,
        )
    )

    recommendations.extend(
        _recommend_from_difficulty(
            profile=profile,
            difficulty=difficulty,
        )
    )

    recommendations.extend(
        _recommend_from_topics(
            profile=profile,
            topics=topics,
        )
    )

    return recommendations


def _recommend_from_weaknesses(
    profile: LeetCodeProfile,
    weaknesses: list[dict],
) -> list[Recommendation]:
    """
    Generate recommendations from detected weaknesses.
    """

    recommendations = []

    for weakness in weaknesses:

        weakness_type = weakness.get("type")
        severity = weakness.get("severity")
        area = weakness.get("area")
        reason = weakness.get("reason")
        metadata = weakness.get("metadata", {})

        priority = _map_priority(severity)

        if weakness_type == "consistency":

            recommendation = Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.CONSISTENCY
                ),
                priority=priority,
                title="Improve coding consistency",
                description=(
                    f"{reason} Try solving at least "
                    "one problem each day."
                ),
                metadata=metadata,
            )

            recommendations.append(
                recommendation
            )

        elif weakness_type == "difficulty":

            recommendation = Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.DIFFICULTY
                ),
                priority=priority,
                title=f"Improve {area}",
                description=reason,
                metadata=metadata,
            )

            recommendations.append(
                recommendation
            )

        elif weakness_type == "activity":

            recommendation = Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.CONSISTENCY
                ),
                priority=priority,
                title="Start solving consistently",
                description=reason,
                metadata=metadata,
            )

            recommendations.append(
                recommendation
            )

    return _save_recommendations(
        recommendations
    )


def _recommend_from_difficulty(
    profile: LeetCodeProfile,
    difficulty: dict,
) -> list[Recommendation]:
    """
    Generate recommendations from difficulty analysis.
    """

    recommendations = []

    assessment = difficulty.get(
        "assessment",
        {},
    )

    level = assessment.get("level")

    if level == "easy_heavy":

        recommendations.append(
            Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.DIFFICULTY
                ),
                priority=(
                    Recommendation.Priority.HIGH
                ),
                title="Increase problem difficulty",
                description=(
                    "Most of your solved problems are Easy. "
                    "Start adding more Medium problems to "
                    "challenge yourself."
                ),
                metadata={
                    "difficulty_level": "medium",
                    "target": 5,
                },
            )
        )

    elif level == "medium_low":

        recommendations.append(
            Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.DIFFICULTY
                ),
                priority=(
                    Recommendation.Priority.MEDIUM
                ),
                title="Practice more Medium problems",
                description=(
                    "Your Medium problem exposure is relatively "
                    "low. Try solving several Medium problems "
                    "each week."
                ),
                metadata={
                    "difficulty_level": "medium",
                    "target": 5,
                },
            )
        )

    elif level == "hard_low":

        recommendations.append(
            Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.DIFFICULTY
                ),
                priority=(
                    Recommendation.Priority.LOW
                ),
                title="Challenge yourself with Hard problems",
                description=(
                    "Your Hard problem exposure is relatively "
                    "low. Consider adding a few Hard problems "
                    "to your practice routine."
                ),
                metadata={
                    "difficulty_level": "hard",
                    "target": 2,
                },
            )
        )

    return _save_recommendations(
        recommendations
    )


def _recommend_from_topics(
    profile: LeetCodeProfile,
    topics: list[dict],
) -> list[Recommendation]:
    """
    Generate recommendations for under-practiced topics.
    """

    if not topics:
        return []

    recommendations = []

    total_submissions = sum(
        topic["submission_count"]
        for topic in topics
    )

    if total_submissions == 0:
        return []

    # Consider topics with very low activity.
    low_activity_topics = [
        topic
        for topic in topics
        if topic["submission_count"] <= 2
    ]

    for topic in low_activity_topics[:3]:

        recommendations.append(
            Recommendation(
                user=profile.user,
                recommendation_type=(
                    Recommendation.RecommendationType.WEAK_TOPIC
                ),
                priority=(
                    Recommendation.Priority.MEDIUM
                ),
                title=(
                    f"Practice {topic['topic']}"
                ),
                description=(
                    f"You have limited activity in "
                    f"{topic['topic']}. "
                    "Practice more problems from this topic "
                    "to strengthen your understanding."
                ),
                metadata={
                    "topic": topic["topic"],
                    "topic_slug": topic["slug"],
                    "submission_count": (
                        topic["submission_count"]
                    ),
                },
            )
        )

    return _save_recommendations(
        recommendations
    )


def _map_priority(
    severity: str | None,
) -> str:
    """
    Convert weakness severity to recommendation priority.
    """

    mapping = {
        "high": Recommendation.Priority.HIGH,
        "medium": Recommendation.Priority.MEDIUM,
        "low": Recommendation.Priority.LOW,
    }

    return mapping.get(
        severity,
        Recommendation.Priority.MEDIUM,
    )


@transaction.atomic
def _save_recommendations(
    recommendations: list[Recommendation],
) -> list[Recommendation]:
    """
    Persist recommendations atomically.
    """

    if not recommendations:
        return []

    Recommendation.objects.bulk_create(
        recommendations,
    )

    return recommendations

def _has_active_recommendation(
    user,
    recommendation_type,
    title,
) -> bool:
    """
    Check whether an active recommendation already exists.
    """

    return Recommendation.objects.filter(
        user=user,
        recommendation_type=recommendation_type,
        title=title,
        status=Recommendation.Status.PENDING,
    ).exists()