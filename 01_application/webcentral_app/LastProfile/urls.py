from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='LastProfile'),
    path('warmelast', views.warmelast, name='LastProfile_warme_display'),

    path('stromlast', views.stromlast, name='LastProfile_strom_display'),
   
]
