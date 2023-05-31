"""Urlpatterns for the StartSearch App."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.startSearch, name="StartSearch"),
    path("ResultSearch", views.resultSearch, name="ResultSearch"),
]
