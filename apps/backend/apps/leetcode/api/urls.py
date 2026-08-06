from django.urls import path

from apps.leetcode.api.views import (
    ConnectLeetCodeAPIView,
    LeetCodeProfileAPIView,
    SyncLeetCodeProfileAPIView,
    DisconnectLeetCodeAPIView,
    SyncLeetCodeSubmissionsAPIView,
    LeetCodeSubmissionListAPIView,
)


urlpatterns = [
    path(
        "connect/",
        ConnectLeetCodeAPIView.as_view(),
        name="leetcode_connect",
    ),

    path(
        "profile/",
        LeetCodeProfileAPIView.as_view(),
        name="leetcode_profile",
    ),
    path(
    "sync/",
    SyncLeetCodeProfileAPIView.as_view(),
    name="leetcode_sync",
),
    path(
    "disconnect/",
    DisconnectLeetCodeAPIView.as_view(),
    name="leetcode_disconnect",
),
path(
    "submissions/sync/",
    SyncLeetCodeSubmissionsAPIView.as_view(),
    name="leetcode_submissions_sync",
),
    path(
        "submissions/",
        LeetCodeSubmissionListAPIView.as_view(),
        name="leetcode_submissions",
    ), 
]