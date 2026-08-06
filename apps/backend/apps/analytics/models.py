from django.db import models

from apps.leetcode.models import LeetCodeProfile


class DailyStatistics(models.Model):
    """
    Daily aggregated statistics for a user's LeetCode activity.
    """

    profile = models.ForeignKey(
        LeetCodeProfile,
        on_delete=models.CASCADE,
        related_name="daily_statistics",
    )

    date = models.DateField()

    solved_count = models.PositiveIntegerField(
        default=0,
    )

    easy_count = models.PositiveIntegerField(
        default=0,
    )

    medium_count = models.PositiveIntegerField(
        default=0,
    )

    hard_count = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        unique_together = (
            "profile",
            "date",
        )

        ordering = [
            "-date",
        ]

    def __str__(self):
        return (
            f"{self.profile.username} - "
            f"{self.date}"
        )