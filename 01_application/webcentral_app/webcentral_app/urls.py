"""Webcentral_app URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import handler404, handler500, handler400, handler403
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("businessModels/", include("businessModel.urls")),
    path("component_list/", include("component_list.urls")),
    path("criteriaCatalog/", include("criteriaCatalog.urls")),
    path("pages/", include("pages.urls")),
    path("tool_list/", include("tools_over.urls")),
    path("dataset_list/", include("Datasets.urls")),
    path("weatherdata_list/", include("weatherdata_over.urls")),
    path("project_list/", include("project_listing.urls")),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path("LastProfile/", include("LastProfile.urls")),
    path("", include("StartSearch.urls")),
    path("TechnicalStandards/", include("TechnicalStandards.urls")),
    path("publications/", include("publications.urls")),
    path("criteriaCatalog/", include("criteriaCatalog.urls")),
    path("useCases_list/", include("use_cases.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("common/", include("common.urls")),
    path("user_integration/", include("user_integration.urls")),
)

handler404 = "webcentral_app.views.custom_404_view"
handler500 = "webcentral_app.views.custom_500_view"
handler403 = "webcentral_app.views.custom_403_view"
handler400 = "webcentral_app.views.custom_400_view"
