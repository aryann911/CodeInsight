from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.common.pagination import StandardPagination

from apps.common.responses import error_response, success_response
from apps.leetcode.api.serializers import (
    ConnectLeetCodeSerializer,
    LeetCodeProfileSerializer,
    LeetCodeSubmissionSerializer,
    SubmissionSyncResultSerializer,
)
from apps.leetcode.services.profile_service import (
    connect_leetcode_profile,
    get_leetcode_profile,
    sync_leetcode_profile,
    disconnect_leetcode_profile,
)
from apps.leetcode.services.submission_service import (
    sync_recent_submissions,
)


class ConnectLeetCodeAPIView(GenericAPIView):
    """
    Connect a LeetCode username to the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ConnectLeetCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error_response(
                message="Validation failed.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = connect_leetcode_profile(
                user=request.user,
                username=serializer.validated_data["username"],
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="LeetCode account connected successfully.",
            data=LeetCodeProfileSerializer(profile).data,
            status_code=status.HTTP_201_CREATED,
        )
    
class LeetCodeProfileAPIView(GenericAPIView):
    """
    Return the authenticated user's connected LeetCode profile.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LeetCodeProfileSerializer

    def get(self, request):
        profile = get_leetcode_profile(request.user)

        if profile is None:
            return error_response(
                message="No LeetCode account is connected.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(profile)

        return success_response(
            message="LeetCode profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
class SyncLeetCodeProfileAPIView(GenericAPIView):
    """
    Synchronize the connected LeetCode profile with LeetCode.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LeetCodeProfileSerializer

    def post(self, request):
        try:
            profile = sync_leetcode_profile(
                user=request.user,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(profile)

        return success_response(
            message="LeetCode profile synchronized successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )
    
class DisconnectLeetCodeAPIView(GenericAPIView):
    """
    Disconnect the authenticated user's LeetCode account.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LeetCodeProfileSerializer

    def delete(self, request):
        try:
            disconnect_leetcode_profile(
                user=request.user,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="LeetCode account disconnected successfully.",
            data={},
            status_code=status.HTTP_200_OK,
        )
    
class SyncLeetCodeSubmissionsAPIView(GenericAPIView):
    """
    Synchronize recent accepted LeetCode submissions.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSyncResultSerializer

    def post(self, request):
        try:
            created_count = sync_recent_submissions(
                user=request.user,
                limit=20,
            )

        except ValueError as exc:
            return error_response(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="LeetCode submissions synchronized successfully.",
            data={
                "created_count": created_count,
            },
            status_code=status.HTTP_200_OK,
        )
    
class LeetCodeSubmissionListAPIView(GenericAPIView):
    """
    Return stored LeetCode submissions for the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LeetCodeSubmissionSerializer
    pagination_class = StandardPagination

    def get(self, request):
        profile = get_leetcode_profile(request.user)

        if profile is None:
            return error_response(
                message="No LeetCode account is connected.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        submissions = profile.submissions.all()

        page = self.paginate_queryset(submissions)

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            submissions,
            many=True,
        )

        return success_response(
            message="LeetCode submissions retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )