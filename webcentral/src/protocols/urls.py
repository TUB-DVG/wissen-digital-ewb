from django.urls import path

from . import views

urlpatterns = [
    path("", views.protocol, name="TechnicalStandards_protocol_list"),
    path(
        "protocol/<str:id>",
        views.protocolDetailView,
        name="TechnicalStandards_protocol_details",
    ),
]
