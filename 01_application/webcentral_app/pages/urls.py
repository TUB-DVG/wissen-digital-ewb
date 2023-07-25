"""Include url conneced to view functions."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('coming', views.coming, name='coming'),
    path('Datenschutzhinweis', views.Datenschutzhinweis,
         name='Datenschutzhinweis'),
    path('businessModelsDev', views.businessModelsDev,
         name='businessModelsDev'),
]
