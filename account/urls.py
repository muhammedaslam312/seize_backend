from django.urls import path
from .views import UserMultiView

urlpatterns = [
    path(
        "users/",
        UserMultiView.as_view(),
        name="user_multi_view",
    ),
]
