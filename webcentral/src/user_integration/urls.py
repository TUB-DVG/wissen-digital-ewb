from django.urls import path

from .views import (
    userEngagementDetails,
    userEngagementDetailsTitle,
)

urlpatterns = [
    path(
        "userEngagement/<int:engagementId>/",
        userEngagementDetails,
        name="userEngagementDetails",
    ),
    path(
        "userEngagement/<path:engagmentTitle>",
        userEngagementDetailsTitle,
        name="userEngagementDetailsTitle",
    ),
]
