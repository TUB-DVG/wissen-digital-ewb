from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dataset_list'),
    path('<str:id>', views.dataset_view, name='dataset_view'),

]
