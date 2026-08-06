from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta
SYNC_COOLDOWN = timedelta(minutes=5)

from apps.leetcode.clients.leetcode_client import (
    LeetCodeClient,
    LeetCodeClientError,
    LeetCodeUserNotFoundError,

)
from apps.leetcode.models import LeetCodeProfile


def connect_leetcode_profile(user, username):
    """
    Verify a LeetCode account and connect it to a CodeInsight user.
    """

    username = username.strip()

    if LeetCodeProfile.objects.filter(user=user).exists():
        raise ValueError(
            "A LeetCode account is already connected to this user."
        )

    if LeetCodeProfile.objects.filter(
        username__iexact=username
    ).exists():
        raise ValueError(
            "This LeetCode account is already connected."
        )

    client = LeetCodeClient()

    try:
        data = client.get_user_profile(username)
    except LeetCodeUserNotFoundError as exc:
        raise ValueError(
            "LeetCode user not found."
        ) from exc
    except LeetCodeClientError as exc:
        raise ValueError(
            "Unable to retrieve LeetCode profile."
        ) from exc

    profile_data = data.get("profile") or {}

    submission_stats = (
        data.get("submitStatsGlobal", {})
        .get("acSubmissionNum", [])
    )

    solved_counts = {
        item.get("difficulty"): item.get("count", 0)
        for item in submission_stats
    }

    try:
        with transaction.atomic():
            profile = LeetCodeProfile.objects.create(
                user=user,
                username=data.get("username", username),
                ranking=profile_data.get("ranking"),
                reputation=profile_data.get("reputation") or 0,
                total_solved=solved_counts.get("All", 0),
                easy_solved=solved_counts.get("Easy", 0),
                medium_solved=solved_counts.get("Medium", 0),
                hard_solved=solved_counts.get("Hard", 0),
                last_synced_at=timezone.now(),
            )

    except IntegrityError as exc:
        raise ValueError(
            "Unable to connect LeetCode account."
        ) from exc

    return profile


def get_leetcode_profile(user):
    """
    Return the connected LeetCode profile for a user.
    """

    try:
        return LeetCodeProfile.objects.get(user=user)
    except LeetCodeProfile.DoesNotExist:
        return None
    
def sync_leetcode_profile(user):
    """
    Fetch the latest LeetCode profile data and update
    the authenticated user's connected profile.

    Manual synchronization is limited by a cooldown
    to avoid unnecessary requests to LeetCode.
    """

    profile = get_leetcode_profile(user)

    if profile is None:
        raise ValueError(
            "No LeetCode account is connected."
        )

    # Prevent excessive external requests
    if profile.last_synced_at:
        next_sync_at = profile.last_synced_at + SYNC_COOLDOWN

        if timezone.now() < next_sync_at:
            remaining_seconds = int(
                (next_sync_at - timezone.now()).total_seconds()
            )

            raise ValueError(
                f"Profile was recently synchronized. "
                f"Try again in {remaining_seconds} seconds."
            )

    client = LeetCodeClient()

    try:
        data = client.get_user_profile(profile.username)

    except LeetCodeUserNotFoundError as exc:
        raise ValueError(
            "Connected LeetCode user was not found."
        ) from exc

    except LeetCodeClientError as exc:
        raise ValueError(
            "Unable to retrieve LeetCode profile."
        ) from exc

    profile_data = data.get("profile") or {}

    submission_stats = (
        data.get("submitStatsGlobal", {})
        .get("acSubmissionNum", [])
    )

    solved_counts = {
        item.get("difficulty"): item.get("count", 0)
        for item in submission_stats
    }

    profile.ranking = profile_data.get("ranking")
    profile.reputation = profile_data.get("reputation") or 0

    profile.total_solved = solved_counts.get("All", 0)
    profile.easy_solved = solved_counts.get("Easy", 0)
    profile.medium_solved = solved_counts.get("Medium", 0)
    profile.hard_solved = solved_counts.get("Hard", 0)

    profile.last_synced_at = timezone.now()

    profile.save(
        update_fields=[
            "ranking",
            "reputation",
            "total_solved",
            "easy_solved",
            "medium_solved",
            "hard_solved",
            "last_synced_at",
            "updated_at",
        ]
    )

    return profile

def disconnect_leetcode_profile(user):
    """
    Disconnect the authenticated user's LeetCode account.
    """

    profile = get_leetcode_profile(user)

    if profile is None:
        raise ValueError(
            "No LeetCode account is connected."
        )

    profile.delete()