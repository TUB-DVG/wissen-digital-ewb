"""Include url conneced to view functions."""
from django.urls import path

# from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("impressum", views.impressum, name="impressum"),
    path("about", views.about, name="about"),
    path("coming", views.coming, name="coming"),
    path(
        "Datenschutzhinweis",
        views.Datenschutzhinweis,
        name="Datenschutzhinweis",
    ),
    path(
        "businessModelsChallenge",
        views.businessModelsChallenge,
        name="businessModelsChallenge",
    ),
    path(
        "businessModelsPractice",
        views.businessModelsPractice,
        name="businessModelsPractice",
    ),
    path(
        "userIntegrationPractice",
        views.userIntegrationPractice,
        name="userIntegrationPractice",
    ),
    path(
        "userIntegrationMethod",
        views.userIntegrationMethod,
        name="userIntegrationMethod",
    ),
    path(
        "environmentalIntegrityNegativ",
        views.environmentalIntegrityNegativ,
        name="environmentalIntegrityNegativ",
    ),
    path(
        "environmentalIntegrityPositiv",
        views.environmentalIntegrityPositiv,
        name="environmentalIntegrityPositiv",
    ),
    path(
        "environmentalIntegrityPositiv/<int:idOfEnvironmentalImpactObj>/",
        views.environmentalIntegrityBox,
        name="environmentalIntegrityBox",
    ),
    path(
        "benchmarkingChallenges",
        views.benchmarkingChallenges,
        name="benchmarkingChallenges",
    ),
    path("dataSufficiency", views.dataSufficiency, name="dataSufficiency"),
    path(
        "dataSufficiencyBox/<int:idOfObject>/",
        views.dataSufficiencyBox,
        name="dataSufficiencyBox",
    ),
    path("dataSecurity", views.dataSecurity, name="dataSecurity"),
    path("iconsAndVis", views.iconsAndVis, name="iconsAndVis"),
    path("criteriaCatalog", views.criteriaCatalog, name="criteriaCatalog"),
    path(
        "showImage/<int:idOfEnvironmentalImpactObj>",
        views.showImage,
        name="showImage",
    ),
    #     redirect('criteriaCatalog:index'),
]
