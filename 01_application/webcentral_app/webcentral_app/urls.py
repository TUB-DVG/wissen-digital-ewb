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

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from tools_over import views

urlpatterns = [
    path('', include('pages.urls')),
    path('tool_list/', include('tools_over.urls')),
    path('application_list/', views.indexApplication),
    path('dataset_list/',include('Datasets.urls')),
    path('weatherdata_list/', include('weatherdata_over.urls')),
    path('project_list/', include('project_listing.urls')),
    path('admin/', admin.site.urls),
    path('norm_list/',include('norms_over.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('LastProfile/', include('LastProfile.urls')),
    path('StartSearch/', include('StartSearch.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
