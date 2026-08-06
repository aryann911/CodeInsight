from django.conf import settings
from django.db import models


class LeetCodeProfile(models.Model):
    """
    Stores a CodeInsight user's connected LeetCode profile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leetcode_profile",
    )

    username = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    ranking = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    reputation = models.IntegerField(
        default=0,
    )

    total_solved = models.PositiveIntegerField(
        default=0,
    )

    easy_solved = models.PositiveIntegerField(
        default=0,
    )

    medium_solved = models.PositiveIntegerField(
        default=0,
    )

    hard_solved = models.PositiveIntegerField(
        default=0,
    )

    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.username}"
    
class LeetCodeSubmission(models.Model):
    """
    Stores a user's LeetCode submission history.
    """

    profile = models.ForeignKey(
        LeetCodeProfile,
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    submission_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
    )

    title_slug = models.CharField(
        max_length=255,
        db_index=True,
    )

    status = models.CharField(
        max_length=50,
    )

    language = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )

    submitted_at = models.DateTimeField(
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.profile.username} - {self.title}"