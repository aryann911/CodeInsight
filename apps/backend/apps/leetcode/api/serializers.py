from rest_framework import serializers

from apps.leetcode.models import (
    LeetCodeProfile,
    LeetCodeSubmission,
)


class LeetCodeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for returning a connected LeetCode profile.
    """

    class Meta:
        model = LeetCodeProfile
        fields = (
            "id",
            "username",
            "ranking",
            "reputation",
            "total_solved",
            "easy_solved",
            "medium_solved",
            "hard_solved",
            "last_synced_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class ConnectLeetCodeSerializer(serializers.Serializer):
    """
    Validate a request to connect a LeetCode account.
    """

    username = serializers.CharField(
        max_length=100,
        trim_whitespace=True,
    )

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError(
                "LeetCode username is required."
            )

        return value


class LeetCodeSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for returning stored LeetCode submissions.
    """

    class Meta:
        model = LeetCodeSubmission
        fields = (
            "id",
            "submission_id",
            "title",
            "title_slug",
            "status",
            "language",
            "submitted_at",
            "created_at",
        )
        read_only_fields = fields


class SubmissionSyncResultSerializer(serializers.Serializer):
    """
    Serializer describing submission synchronization results.
    """

    created_count = serializers.IntegerField(
        read_only=True,
    )