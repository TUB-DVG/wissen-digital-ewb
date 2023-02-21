from django.urls import path

from . import views
from LastProfile.Dash_app import  Stromlast ,Warmelast
from django.views.generic.base import TemplateView
urlpatterns = [
    path('', views.index, name='LastProfile'),
    path('warmelast', views.warmelast, name='LastProfile_warme_display'),

    path('stromlast', views.stromlast, name='LastProfile_strom_display'),
   
]
