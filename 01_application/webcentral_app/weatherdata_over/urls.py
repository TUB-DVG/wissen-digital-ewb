from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='weatherdata_list'),
    path('<str:id>', views.weatherdata_view, name='weatherdata_view'),
]
