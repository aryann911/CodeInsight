from django.urls import path

from apps.users.api.views import RegisterAPIView

urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
]