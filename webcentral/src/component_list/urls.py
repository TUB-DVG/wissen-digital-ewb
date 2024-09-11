from django.urls import path

from . import views

urlpatterns = [
    path("components/", views.ComponentListView.as_view(), name="components"),
    path(
        "components/<int:componentId>",
        views.ComponentListView.as_view(),
        name="componentsOpenId",
    ),
    path("dataProcessing/", views.dataProcessing, name="dataProcessing"),
    path(
        "showImage/<path:pathToImage>",
        views.showImage,
        name="showImageComponents",
    ),
]
