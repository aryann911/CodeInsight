from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.analytics.api.serializers import (
    DashboardSerializer,
)
from apps.analytics.services.analytics_service import (
    get_activity_heatmap,
    get_difficulty_distribution,
    get_language_statistics,
    get_monthly_statistics,
    get_streak_statistics,
    get_weekly_statistics,
)
from apps.common.responses import (
    error_response,
    success_response,
)
from apps.leetcode.services.profile_service import (
    get_leetcode_profile,
)


class DashboardAPIView(GenericAPIView):
    """
    Return analytics dashboard data.
    """

    permission_classes = [IsAuthenticated]

    serializer_class = DashboardSerializer

    def get(self, request):

        profile = get_leetcode_profile(request.user)

        if profile is None:

            return error_response(
                message="No LeetCode account is connected.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        dashboard = {

            "profile": {
                "username": profile.username,
                "ranking": profile.ranking,
                "reputation": profile.reputation,
                "total_solved": profile.total_solved,
            },

            "weekly_statistics": (
                get_weekly_statistics(profile)
            ),

            "monthly_statistics": (
                get_monthly_statistics(profile)
            ),

            "difficulty_distribution": (
                get_difficulty_distribution(profile)
            ),

            "language_statistics": (
                get_language_statistics(profile)
            ),

            "activity_heatmap": (
                get_activity_heatmap(profile)
            ),

            "streak_statistics": (
                get_streak_statistics(profile)
            ),
        }

        serializer = self.get_serializer(
            dashboard,
        )

        return success_response(
            message=(
                "Dashboard retrieved successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )