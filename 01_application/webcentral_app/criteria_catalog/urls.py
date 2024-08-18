from django.urls import path

from . import views
from django.views.generic.base import TemplateView

# app_name = "criteriaCatalog"

urlpatterns = [
    path(
        "<int:criteriaCatalogId>/<int:topicIdentifier>",
        views.buildingCriteriaCatalogOpenTopic,
        name="criteriaCatalogOpenTopic",
    ),
    path(
        "<int:criteriaCatalogId>",
        views.buildCriteriaCatalog,
        name="criteriaCatalog",
    ),
]
