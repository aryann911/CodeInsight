from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.authentication.api.urls")),
    path("leetcode/",include("apps.leetcode.api.urls"),),
]