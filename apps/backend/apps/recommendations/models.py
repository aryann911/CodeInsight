from django.conf import settings
from django.db import models


class Recommendation(models.Model):
    """
    Stores a personalized recommendation generated for a user.
    """

    class RecommendationType(models.TextChoices):
        WEAK_TOPIC = "weak_topic", "Weak Topic"
        DIFFICULTY = "difficulty", "Difficulty"
        REVISION = "revision", "Revision"
        STUDY_PLAN = "study_plan", "Study Plan"
        CONSISTENCY = "consistency", "Consistency"
        INTERVIEW = "interview", "Interview"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        DISMISSED = "dismissed", "Dismissed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )

    recommendation_type = models.CharField(
        max_length=30,
        choices=RecommendationType.choices,
        db_index=True,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["user", "status"],
            ),
            models.Index(
                fields=["user", "recommendation_type"],
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class WeeklyStudyPlan(models.Model):
    """
    Stores a personalized weekly study plan.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        EXPIRED = "expired", "Expired"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="weekly_study_plans",
    )

    week_start = models.DateField()

    week_end = models.DateField()

    target_problems = models.PositiveIntegerField(
        default=0,
    )

    completed_problems = models.PositiveIntegerField(
        default=0,
    )

    target_minutes = models.PositiveIntegerField(
        default=0,
    )

    completed_minutes = models.PositiveIntegerField(
        default=0,
    )

    focus_topics = models.JSONField(
        default=list,
        blank=True,
    )

    focus_difficulties = models.JSONField(
        default=list,
        blank=True,
    )

    tasks = models.JSONField(
        default=list,
        blank=True,
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-week_start"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "week_start"],
                name="unique_user_weekly_study_plan",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "status"],
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.week_start} to {self.week_end}"
        )