from django.urls import path

from .views import (
    businessModelsChallenge,
    businessModelsChallengeDetails,
    userEngagementDetails,
)

urlpatterns = [
    path("challenges/",
         businessModelsChallenge,
         name="businessModelsChallenge"),
    path(
        "challenges/<int:challengeId>/",
        businessModelsChallengeDetails,
        name="businessModelsChallengeDetails",
    ),
    path(
        "userEngagement/<int:engagementId>/",
        userEngagementDetails,
        name="userEngagementDetails",
    ),
]
