"""Urlpatterns for the StartSearch App."""
from django.urls import path

from . import views

app_name = "StartSearch"  # includes namespacing URL names
urlpatterns = [
    path("", views.startSearch, name="StartSearch"),
    path("ResultSearch", views.resultSearch, name="ResultSearch"),
]
