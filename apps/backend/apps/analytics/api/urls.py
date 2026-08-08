from django.urls import path

from apps.analytics.api.views import (
    DashboardAPIView,
)

app_name = "analytics"

urlpatterns = [
    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),
]