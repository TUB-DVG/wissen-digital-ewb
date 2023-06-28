from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('data', views.data, name='data'),
    path('coming', views.coming, name='coming'),
    path('Datenschutzhinweis', views.Datenschutzhinweis, name='Datenschutzhinweis'),
]
