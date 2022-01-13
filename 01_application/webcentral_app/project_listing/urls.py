from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='project_list'),
    path('<int:fkz>', views.project_view, name='project_view'),
    path('search', views.search, name='search'),
]
