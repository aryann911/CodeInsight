from apps.analytics.services.analytics_service import (
    get_streak_statistics,
)
from apps.leetcode.models import LeetCodeProfile
from apps.recommendations.services.difficulty_service import (
    analyze_difficulty,
)
from apps.recommendations.services.topic_service import (
    analyze_topics,
)


def calculate_interview_readiness(
    profile: LeetCodeProfile,
) -> dict:
    """
    Calculate an explainable interview readiness score.

    Score components:

    - Problem volume:       25 points
    - Difficulty exposure:  30 points
    - Coding consistency:   20 points
    - Topic coverage:       25 points

    Total: 100 points.
    """

    difficulty = analyze_difficulty(profile)

    topics = analyze_topics(profile)

    streak = get_streak_statistics(profile)

    volume_score = _calculate_volume_score(
        profile,
    )

    difficulty_score = _calculate_difficulty_score(
        difficulty,
    )

    consistency_score = _calculate_consistency_score(
        streak,
    )

    topic_score = _calculate_topic_score(
        topics,
    )

    total_score = min(
        100,
        volume_score
        + difficulty_score
        + consistency_score
        + topic_score,
    )

    return {
        "score": total_score,
        "level": _get_readiness_level(
            total_score,
        ),
        "breakdown": {
            "problem_volume": volume_score,
            "difficulty_exposure": difficulty_score,
            "coding_consistency": consistency_score,
            "topic_coverage": topic_score,
        },
        "recommendations": _build_recommendations(
            volume_score=volume_score,
            difficulty_score=difficulty_score,
            consistency_score=consistency_score,
            topic_score=topic_score,
        ),
    }


def _calculate_volume_score(
    profile: LeetCodeProfile,
) -> int:
    """
    Calculate up to 25 points from solved problems.
    """

    solved = profile.total_solved

    if solved >= 300:
        return 25

    if solved >= 200:
        return 20

    if solved >= 100:
        return 15

    if solved >= 50:
        return 10

    if solved >= 25:
        return 5

    return 0


def _calculate_difficulty_score(
    difficulty: dict,
) -> int:
    """
    Calculate up to 30 points from difficulty exposure.
    """

    distribution = difficulty.get(
        "distribution",
        {},
    )

    medium = distribution.get(
        "medium",
        {},
    ).get("percentage", 0)

    hard = distribution.get(
        "hard",
        {},
    ).get("percentage", 0)

    score = 0

    # Medium exposure: up to 20 points.
    if medium >= 40:
        score += 20
    elif medium >= 30:
        score += 15
    elif medium >= 20:
        score += 10
    elif medium >= 10:
        score += 5

    # Hard exposure: up to 10 points.
    if hard >= 15:
        score += 10
    elif hard >= 10:
        score += 8
    elif hard >= 5:
        score += 5
    elif hard > 0:
        score += 2

    return score


def _calculate_consistency_score(
    streak: dict,
) -> int:
    """
    Calculate up to 20 points from coding consistency.
    """

    longest = streak.get(
        "longest_streak",
        0,
    )

    current = streak.get(
        "current_streak",
        0,
    )

    longest_score = min(
        12,
        longest,
    )

    current_score = min(
        8,
        current,
    )

    return longest_score + current_score


def _calculate_topic_score(
    topics: list[dict],
) -> int:
    """
    Calculate up to 25 points from topic coverage.

    More distinct topics indicate broader preparation.
    """

    topic_count = len(topics)

    if topic_count >= 15:
        return 25

    if topic_count >= 10:
        return 20

    if topic_count >= 7:
        return 15

    if topic_count >= 4:
        return 10

    if topic_count >= 2:
        return 5

    return 0


def _get_readiness_level(
    score: int,
) -> str:
    """
    Convert the numerical score into a readiness level.
    """

    if score >= 80:
        return "interview_ready"

    if score >= 60:
        return "strong_progress"

    if score >= 40:
        return "developing"

    if score >= 20:
        return "beginner"

    return "needs_improvement"


def _build_recommendations(
    volume_score: int,
    difficulty_score: int,
    consistency_score: int,
    topic_score: int,
) -> list[str]:
    """
    Generate actionable recommendations from weak score areas.
    """

    recommendations = []

    if volume_score < 15:
        recommendations.append(
            "Increase the number of problems you solve."
        )

    if difficulty_score < 20:
        recommendations.append(
            "Increase your Medium and Hard problem exposure."
        )

    if consistency_score < 12:
        recommendations.append(
            "Build a more consistent daily solving habit."
        )

    if topic_score < 15:
        recommendations.append(
            "Practice a broader range of problem topics."
        )

    if not recommendations:
        recommendations.append(
            "Maintain your current preparation level "
            "and continue practicing consistently."
        )

    return recommendations