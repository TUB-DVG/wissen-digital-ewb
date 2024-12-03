from django.urls import path
from .dashApp import protocolToolChain
from . import views
from protocols.views import *

urlpatterns = [
    path("", views.index, name="TechnicalStandards"),
    path("norm", views.norm, name="TechnicalStandards_norm_list"),
    path(
        "norm/<str:id>",
        views.normDetailView,
        name="TechnicalStandards_norm_details",
    ),
    path(
        "comparison/",
        protocolComparison,
        name="TechnicalStandards_protocol_comparison",
    ),
]
