from django.urls import path

from apps.recommendations.api.views import (
    CodingConsistencyAPIView,
    InterviewReadinessAPIView,
    RecommendationGenerateAPIView,
    RecommendationListAPIView,
    WeeklyStudyPlanAPIView,
)


urlpatterns = [
    path(
        "",
        RecommendationListAPIView.as_view(),
        name="recommendation-list",
    ),

    path(
        "generate/",
        RecommendationGenerateAPIView.as_view(),
        name="recommendation-generate",
    ),

    path(
        "study-plan/",
        WeeklyStudyPlanAPIView.as_view(),
        name="weekly-study-plan",
    ),

    path(
        "interview-readiness/",
        InterviewReadinessAPIView.as_view(),
        name="interview-readiness",
    ),

    path(
        "consistency/",
        CodingConsistencyAPIView.as_view(),
        name="coding-consistency",
    ),
]