from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.analytics.models import DailyStatistics
from apps.leetcode.models import LeetCodeSubmission
from apps.recommendations.models import (
    Recommendation,
    WeeklyStudyPlan,
)
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
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class AICoachIntegrationTest(
    RecommendationsBaseTestCase,
):
    """
    Integration tests for the complete AI Coach engine.
    """

    def setUp(self):
        super().setUp()

        self._create_submission_data()
        self._create_activity_data()

    def _create_submission_data(self):
        """
        Create realistic submission data representing
        a user who is heavily focused on Easy problems.
        """

        difficulties = [
            "Easy",
            "Easy",
            "Easy",
            "Easy",
            "Easy",
            "Easy",
            "Medium",
        ]

        for index, difficulty in enumerate(
            difficulties,
            start=1,
        ):
            LeetCodeSubmission.objects.create(
                profile=self.profile,
                submission_id=(
                    f"ai-coach-submission-{index}"
                ),
                title=f"Problem {index}",
                title_slug=f"problem-{index}",
                status="Accepted",
                language="python",
                difficulty=difficulty,
                submitted_at=(
                    timezone.now()
                    - timedelta(days=index)
                ),
            )

    def _create_activity_data(self):
        """
        Create recent daily activity.
        """

        today = timezone.localdate()

        for days_ago in range(7):

            DailyStatistics.objects.create(
                profile=self.profile,
                date=(
                    today
                    - timedelta(days=days_ago)
                ),
                solved_count=2,
                easy_count=1,
                medium_count=1,
            )

    def test_interview_readiness_works(self):
        result = calculate_interview_readiness(
            self.profile,
        )

        self.assertGreaterEqual(
            result["score"],
            0,
        )

        self.assertLessEqual(
            result["score"],
            100,
        )

        self.assertIn(
            "breakdown",
            result,
        )

    def test_consistency_score_works(self):
        result = calculate_consistency_score(
            self.profile,
        )

        self.assertGreaterEqual(
            result["score"],
            0,
        )

        self.assertLessEqual(
            result["score"],
            100,
        )

        self.assertIn(
            "metrics",
            result,
        )

    def test_weekly_study_plan_is_generated(self):
        plan = generate_weekly_study_plan(
            self.profile,
        )

        self.assertIsInstance(
            plan,
            WeeklyStudyPlan,
        )

        self.assertEqual(
            plan.user,
            self.user,
        )

        self.assertEqual(
            len(plan.tasks),
            7,
        )

    def test_recommendations_are_generated(self):
        recommendations = (
            generate_recommendations(
                self.profile,
            )
        )

        self.assertIsInstance(
            recommendations,
            list,
        )

        self.assertTrue(
            Recommendation.objects.filter(
                user=self.user,
            ).exists()
        )

    def test_study_plan_is_idempotent(self):
        first = generate_weekly_study_plan(
            self.profile,
        )

        second = generate_weekly_study_plan(
            self.profile,
        )

        self.assertEqual(
            first.id,
            second.id,
        )

        self.assertEqual(
            WeeklyStudyPlan.objects.filter(
                user=self.user,
                week_start=first.week_start,
            ).count(),
            1,
        )

    def test_recommendation_api(self):
        response = self.client.get(
            reverse(
                "recommendation-list",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_study_plan_api(self):
        response = self.client.get(
            reverse(
                "weekly-study-plan",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "data",
            response.data,
        )

    def test_interview_readiness_api(self):
        response = self.client.get(
            reverse(
                "interview-readiness",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_consistency_api(self):
        response = self.client.get(
            reverse(
                "coding-consistency",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )