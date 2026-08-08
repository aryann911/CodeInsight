from collections import defaultdict

from apps.leetcode.models import LeetCodeProfile


DIFFICULTIES = (
    "Easy",
    "Medium",
    "Hard",
)


def analyze_difficulty(
    profile: LeetCodeProfile,
) -> dict:
    """
    Analyze a user's submission distribution by difficulty.

    Returns counts, percentages, and a basic difficulty assessment.
    """

    counts = defaultdict(int)

    submissions = profile.submissions.all()

    for submission in submissions:
        difficulty = (
            submission.difficulty or ""
        ).strip().title()

        if difficulty in DIFFICULTIES:
            counts[difficulty] += 1

    total = sum(
        counts[difficulty]
        for difficulty in DIFFICULTIES
    )

    distribution = {}

    for difficulty in DIFFICULTIES:
        count = counts[difficulty]

        percentage = (
            round((count / total) * 100, 2)
            if total
            else 0.0
        )

        distribution[difficulty.lower()] = {
            "count": count,
            "percentage": percentage,
        }

    assessment = _build_assessment(
        counts=counts,
        total=total,
    )

    return {
        "total": total,
        "distribution": distribution,
        "assessment": assessment,
    }


def _build_assessment(
    counts,
    total,
) -> dict:
    """
    Determine whether the user's difficulty distribution
    is balanced.
    """

    if total == 0:
        return {
            "level": "insufficient_data",
            "message": (
                "Not enough difficulty data "
                "to evaluate progression."
            ),
        }

    easy_ratio = counts["Easy"] / total
    medium_ratio = counts["Medium"] / total
    hard_ratio = counts["Hard"] / total

    if easy_ratio >= 0.70:
        return {
            "level": "easy_heavy",
            "message": (
                "Your solved problems are heavily "
                "weighted toward Easy problems."
            ),
        }

    if medium_ratio < 0.20:
        return {
            "level": "medium_low",
            "message": (
                "Your Medium problem exposure "
                "is relatively low."
            ),
        }

    if hard_ratio < 0.05:
        return {
            "level": "hard_low",
            "message": (
                "Your Hard problem exposure "
                "is relatively low."
            ),
        }

    if (
        easy_ratio >= 0.20
        and medium_ratio >= 0.20
        and hard_ratio >= 0.05
    ):
        return {
            "level": "balanced",
            "message": (
                "Your difficulty distribution "
                "shows exposure across all levels."
            ),
        }

    return {
        "level": "developing",
        "message": (
            "Your difficulty distribution "
            "is still developing."
        ),
    }