from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="TechnicalStandards"),
    path("norm", views.norm, name="TechnicalStandards_norm_list"),
    path("protocol", views.protocol, name="TechnicalStandards_protocol_list"),
    path(
        "norm/<str:id>",
        views.normDetailView,
        name="TechnicalStandards_norm_details",
    ),
    path(
        "protocol/<str:id>",
        views.protocolDetailView,
        name="TechnicalStandards_protocol_details",
    ),
    path(
        "comparison/",
        views.protocolComparison,
        name="TechnicalStandards_protocol_comparison",
    ),
]
