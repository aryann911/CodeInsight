from rest_framework import serializers

from apps.recommendations.models import (
    Recommendation,
    WeeklyStudyPlan,
)


class RecommendationSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for personalized recommendations.
    """

    class Meta:
        model = Recommendation
        fields = (
            "id",
            "recommendation_type",
            "priority",
            "title",
            "description",
            "status",
            "metadata",
            "expires_at",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class WeeklyStudyPlanSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for a weekly study plan.
    """

    class Meta:
        model = WeeklyStudyPlan
        fields = (
            "id",
            "week_start",
            "week_end",
            "target_problems",
            "completed_problems",
            "target_minutes",
            "completed_minutes",
            "focus_topics",
            "focus_difficulties",
            "tasks",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class InterviewReadinessSerializer(
    serializers.Serializer,
):
    """
    Serializer for interview readiness results.
    """

    score = serializers.IntegerField(
        min_value=0,
        max_value=100,
    )

    level = serializers.CharField()

    breakdown = serializers.DictField()

    recommendations = serializers.ListField(
        child=serializers.CharField(),
    )


class CodingConsistencySerializer(
    serializers.Serializer,
):
    """
    Serializer for coding consistency results.
    """

    score = serializers.IntegerField(
        min_value=0,
        max_value=100,
    )

    level = serializers.CharField()

    breakdown = serializers.DictField()

    metrics = serializers.DictField()

    recommendations = serializers.ListField(
        child=serializers.CharField(),
    )