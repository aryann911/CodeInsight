from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include("apps.authentication.api.urls"),
    ),
    path(
        "leetcode/",
        include("apps.leetcode.api.urls"),
    ),
    path(
        "analytics/",
        include("apps.analytics.api.urls"),

    ),
    path(
        "recommendations/",
        include(
            "apps.recommendations.api.urls"
        ),
    ),
]