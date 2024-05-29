from django.urls import path

from .views import (
    businessModelsChallenge,
    businessModelsChallengeDetails,
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
]
