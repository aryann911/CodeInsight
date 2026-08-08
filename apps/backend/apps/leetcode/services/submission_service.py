from datetime import UTC, datetime

from django.db import transaction

from apps.leetcode.clients.leetcode_client import (
    LeetCodeClient,
    LeetCodeClientError,
)
from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeSubmission,
)


def sync_recent_submissions(
    user,
    limit: int = 20,
) -> int:
    """
    Fetch and store a user's recent accepted LeetCode submissions.

    Existing submissions are skipped using the unique submission_id.

    Returns:
        int: Number of newly created submissions.
    """

    try:
        profile = LeetCodeProfile.objects.get(user=user)

    except LeetCodeProfile.DoesNotExist as exc:
        raise ValueError(
            "No LeetCode account is connected."
        ) from exc

    client = LeetCodeClient()

    try:
        submissions = client.get_recent_submissions(
            username=profile.username,
            limit=limit,
        )

    except LeetCodeClientError as exc:
        raise ValueError(
            "Unable to retrieve LeetCode submissions."
        ) from exc

    created_count = 0

    with transaction.atomic():

        for submission in submissions:

            submission_id = submission.get("id")
            timestamp = submission.get("timestamp")

            if not submission_id or not timestamp:
                continue

            try:
                submitted_at = datetime.fromtimestamp(
                    int(timestamp),
                    tz=UTC,
                )

            except (
                TypeError,
                ValueError,
                OverflowError,
            ):
                continue

            _, created = LeetCodeSubmission.objects.get_or_create(
                submission_id=str(submission_id),
                defaults={
                    "profile": profile,
                    "title": submission.get(
                        "title",
                        "",
                    ),
                    "title_slug": submission.get(
                        "titleSlug",
                        "",
                    ),
                    "status": "Accepted",
                    "language": submission.get(
                        "lang",
                        "",
                    ),
                    # The current LeetCode GraphQL endpoint
                    # does not expose difficulty in
                    # recentAcSubmissionList.
                    "difficulty": "",
                    "submitted_at": submitted_at,
                },
            )

            if created:
                created_count += 1

    return created_count