from django.urls import path

from . import views
from project_listing.Dash_app import  Simple ,Warmelast
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='project_list'),
    #path('<str:fkz>', views.project_view, name='project_view'),
    path('search', views.search, name='search'),

]
