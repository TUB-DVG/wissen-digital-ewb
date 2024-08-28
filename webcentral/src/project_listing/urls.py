from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="project_list"),
    path("<str:referenceNumber_id>", views.project_view, name="project_view"),
    path("search", views.search, name="search"),
]
