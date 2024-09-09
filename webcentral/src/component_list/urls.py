from django.urls import path

from . import views

urlpatterns = [
    path("components/", views.components, name="components"),
    path("components/<int:componentId>", views.componentsOpenId, name="componentsOpenId"),

    path("dataProcessing/", views.dataProcessing, name="dataProcessing"),
    path(
        "showImage/<path:pathToImage>",
        views.showImage,
        name="showImageComponents",
    ),
]
