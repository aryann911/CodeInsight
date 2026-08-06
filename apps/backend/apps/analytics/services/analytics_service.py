from collections import defaultdict

from django.db import transaction

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