from apps.analytics.services.analytics_service import (
    get_difficulty_distribution,
    get_streak_statistics,
)
from apps.leetcode.models import LeetCodeProfile


def detect_weaknesses(profile: LeetCodeProfile) -> list[dict]:
    """
    Detect potential learning weaknesses from a user's
    LeetCode activity.

    The detection is deterministic and explainable.
    """

    weaknesses = []

    difficulty = get_difficulty_distribution(profile)

    easy = difficulty["easy"]
    medium = difficulty["medium"]
    hard = difficulty["hard"]
    total = difficulty["total"]

    # ---------------------------------------------------------
    # Difficulty imbalance
    # ---------------------------------------------------------

    if total > 0:
        easy_ratio = easy / total
        medium_ratio = medium / total
        hard_ratio = hard / total

        if easy_ratio >= 0.70:
            weaknesses.append(
                {
                    "type": "difficulty",
                    "area": "Medium/Hard problems",
                    "severity": "high",
                    "reason": (
                        "Most solved problems are Easy. "
                        "More Medium and Hard problems are "
                        "recommended for progression."
                    ),
                    "metadata": {
                        "easy_ratio": round(easy_ratio, 2),
                        "medium_ratio": round(medium_ratio, 2),
                        "hard_ratio": round(hard_ratio, 2),
                    },
                }
            )

        elif medium_ratio < 0.20 and hard_ratio < 0.05:
            weaknesses.append(
                {
                    "type": "difficulty",
                    "area": "Medium problems",
                    "severity": "medium",
                    "reason": (
                        "Medium-problem exposure is relatively low."
                    ),
                    "metadata": {
                        "medium_ratio": round(medium_ratio, 2),
                        "hard_ratio": round(hard_ratio, 2),
                    },
                }
            )

    # ---------------------------------------------------------
    # Activity consistency
    # ---------------------------------------------------------

    streak = get_streak_statistics(profile)

    current_streak = streak["current_streak"]
    longest_streak = streak["longest_streak"]

    if longest_streak == 0:
        weaknesses.append(
            {
                "type": "consistency",
                "area": "Coding consistency",
                "severity": "high",
                "reason": (
                    "There is no recorded solving streak. "
                    "Start with a small daily solving target."
                ),
                "metadata": {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                },
            }
        )

    elif current_streak == 0:
        weaknesses.append(
            {
                "type": "consistency",
                "area": "Coding consistency",
                "severity": "medium",
                "reason": (
                    "The current solving streak has been broken."
                ),
                "metadata": {
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                },
            }
        )

    # ---------------------------------------------------------
    # Submission volume
    # ---------------------------------------------------------

    submission_count = profile.submissions.count()

    if submission_count == 0:
        weaknesses.append(
            {
                "type": "activity",
                "area": "LeetCode activity",
                "severity": "high",
                "reason": (
                    "No submissions have been synchronized yet."
                ),
                "metadata": {
                    "submission_count": submission_count,
                },
            }
        )

    return weaknesses