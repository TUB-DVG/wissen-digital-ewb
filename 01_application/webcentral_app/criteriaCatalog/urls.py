from django.urls import path

from . import views
from django.views.generic.base import TemplateView

app_name = "criteriaCatalog"

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:id>', views.useCaseView, name='usecase_view'),
    # path('warmelast', views.warmelast, name='LastProfile_warme_display'),   
]