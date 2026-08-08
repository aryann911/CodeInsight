from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import (
    error_response,
    success_response,
)
from apps.leetcode.models import LeetCodeProfile

from apps.recommendations.api.serializers import (
    CodingConsistencySerializer,
    InterviewReadinessSerializer,
    RecommendationSerializer,
    WeeklyStudyPlanSerializer,
)
from apps.recommendations.models import Recommendation
from apps.recommendations.services.consistency_service import (
    calculate_consistency_score,
)
from apps.recommendations.services.interview_service import (
    calculate_interview_readiness,
)
from apps.recommendations.services.recommendation_service import (
    generate_recommendations,
)
from apps.recommendations.services.study_plan_service import (
    generate_weekly_study_plan,
)


class RecommendationListAPIView(
    GenericAPIView,
):
    """
    Return pending recommendations for
    the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationSerializer

    def get(self, request):
        recommendations = (
            Recommendation.objects.filter(
                user=request.user,
                status=Recommendation.Status.PENDING,
            )
            .order_by(
                "-priority",
                "-created_at",
            )
        )

        serializer = self.get_serializer(
            recommendations,
            many=True,
        )

        return success_response(
            message=(
                "Recommendations retrieved successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class RecommendationGenerateAPIView(
    GenericAPIView,
):
    """
    Generate personalized recommendations
    for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = RecommendationSerializer

    def post(self, request):
        profile = _get_profile(request)

        if profile is None:
            return error_response(
                message=(
                    "No LeetCode account is connected."
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        recommendations = generate_recommendations(
            profile,
        )

        serializer = self.get_serializer(
            recommendations,
            many=True,
        )

        return success_response(
            message=(
                "Personalized recommendations "
                "generated successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class WeeklyStudyPlanAPIView(
    GenericAPIView,
):
    """
    Return or generate the current weekly study plan.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WeeklyStudyPlanSerializer

    def get(self, request):
        profile = _get_profile(request)

        if profile is None:
            return error_response(
                message=(
                    "No LeetCode account is connected."
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        plan = generate_weekly_study_plan(
            profile,
        )

        serializer = self.get_serializer(
            plan,
        )

        return success_response(
            message=(
                "Weekly study plan retrieved successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        profile = _get_profile(request)

        if profile is None:
            return error_response(
                message=(
                    "No LeetCode account is connected."
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        plan = generate_weekly_study_plan(
            profile,
        )

        serializer = self.get_serializer(
            plan,
        )

        return success_response(
            message=(
                "Weekly study plan generated successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class InterviewReadinessAPIView(
    GenericAPIView,
):
    """
    Return the authenticated user's interview
    readiness score.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = InterviewReadinessSerializer

    def get(self, request):
        profile = _get_profile(request)

        if profile is None:
            return error_response(
                message=(
                    "No LeetCode account is connected."
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        result = calculate_interview_readiness(
            profile,
        )

        serializer = self.get_serializer(
            data=result,
        )
        serializer.is_valid(raise_exception=True)

        return success_response(
            message=(
                "Interview readiness calculated successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class CodingConsistencyAPIView(
    GenericAPIView,
):
    """
    Return the authenticated user's coding
    consistency score.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CodingConsistencySerializer

    def get(self, request):
        profile = _get_profile(request)

        if profile is None:
            return error_response(
                message=(
                    "No LeetCode account is connected."
                ),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        result = calculate_consistency_score(
            profile,
        )

        serializer = self.get_serializer(
            data=result,
        )
        serializer.is_valid(raise_exception=True)

        return success_response(
            message=(
                "Coding consistency calculated successfully."
            ),
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


def _get_profile(request):
    """
    Return the authenticated user's LeetCode profile.
    """

    try:
        return LeetCodeProfile.objects.get(
            user=request.user,
        )
    except LeetCodeProfile.DoesNotExist:
        return None