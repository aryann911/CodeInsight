from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    """
    Serializer for the analytics dashboard.
    """

    profile = serializers.DictField()

    weekly_statistics = serializers.DictField()

    monthly_statistics = serializers.DictField()

    difficulty_distribution = serializers.DictField()

    language_statistics = serializers.ListField()

    activity_heatmap = serializers.ListField()

    streak_statistics = serializers.DictField()