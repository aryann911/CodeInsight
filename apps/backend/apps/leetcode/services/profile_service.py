from datetime import timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.leetcode.clients.leetcode_client import (
    LeetCodeClient,
    LeetCodeClientError,
    LeetCodeUserNotFoundError,
)
from apps.leetcode.models import LeetCodeProfile

SYNC_COOLDOWN = timedelta(minutes=5)


def _fetch_profile_data(username):
    """
    Fetch a LeetCode profile from the API.
    """

    client = LeetCodeClient()

    try:
        return client.get_user_profile(username)

    except LeetCodeUserNotFoundError as exc:
        raise ValueError(
            "LeetCode user not found."
        ) from exc

    except LeetCodeClientError as exc:
        raise ValueError(
            "Unable to retrieve LeetCode profile."
        ) from exc


def _extract_statistics(data):
    """
    Extract profile statistics returned by LeetCode.
    """

    profile = data.get("profile") or {}

    submission_stats = (
        data.get("submitStatsGlobal", {})
        .get("acSubmissionNum", [])
    )

    solved = {
        item.get("difficulty"): item.get("count", 0)
        for item in submission_stats
    }

    return {
        "username": data.get("username"),
        "ranking": profile.get("ranking"),
        "reputation": profile.get("reputation") or 0,
        "total_solved": solved.get("All", 0),
        "easy_solved": solved.get("Easy", 0),
        "medium_solved": solved.get("Medium", 0),
        "hard_solved": solved.get("Hard", 0),
    }


def connect_leetcode_profile(user, username):
    """
    Verify and connect a LeetCode account.
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

    stats = _extract_statistics(
        _fetch_profile_data(username)
    )

    try:
        with transaction.atomic():
            profile = LeetCodeProfile.objects.create(
                user=user,
                username=stats["username"] or username,
                ranking=stats["ranking"],
                reputation=stats["reputation"],
                total_solved=stats["total_solved"],
                easy_solved=stats["easy_solved"],
                medium_solved=stats["medium_solved"],
                hard_solved=stats["hard_solved"],
                last_synced_at=timezone.now(),
            )

    except IntegrityError as exc:
        raise ValueError(
            "Unable to connect LeetCode account."
        ) from exc

    return profile


def get_leetcode_profile(user):
    """
    Return the connected LeetCode profile.
    """

    try:
        return LeetCodeProfile.objects.get(user=user)

    except LeetCodeProfile.DoesNotExist:
        return None


def sync_leetcode_profile(user):
    """
    Synchronize the connected LeetCode profile.
    """

    profile = get_leetcode_profile(user)

    if profile is None:
        raise ValueError(
            "No LeetCode account is connected."
        )

    now = timezone.now()

    if profile.last_synced_at:
        next_sync = (
            profile.last_synced_at +
            SYNC_COOLDOWN
        )

        if now < next_sync:
            remaining = int(
                (next_sync - now).total_seconds()
            )

            raise ValueError(
                f"Profile was recently synchronized. "
                f"Try again in {remaining} seconds."
            )

    stats = _extract_statistics(
        _fetch_profile_data(profile.username)
    )

    profile.ranking = stats["ranking"]
    profile.reputation = stats["reputation"]
    profile.total_solved = stats["total_solved"]
    profile.easy_solved = stats["easy_solved"]
    profile.medium_solved = stats["medium_solved"]
    profile.hard_solved = stats["hard_solved"]
    profile.last_synced_at = now

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