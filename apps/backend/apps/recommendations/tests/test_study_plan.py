from apps.recommendations.models import WeeklyStudyPlan
from apps.recommendations.services.study_plan_service import (
    generate_weekly_study_plan,
)
from apps.recommendations.tests.base import (
    RecommendationsBaseTestCase,
)


class WeeklyStudyPlanTest(
    RecommendationsBaseTestCase,
):

    def test_generate_weekly_study_plan(self):
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

        self.assertGreater(
            plan.target_problems,
            0,
        )

        self.assertGreater(
            plan.target_minutes,
            0,
        )

        self.assertEqual(
            len(plan.tasks),
            7,
        )

    def test_generating_plan_twice_does_not_duplicate(self):
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