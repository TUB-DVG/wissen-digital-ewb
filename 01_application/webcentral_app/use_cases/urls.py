from django.urls import path
from use_cases.dashApp import useCaseTS

from . import views

urlpatterns = [
    path('', views.index, name='use_cases_list'),
    path('<str:id>', views.useCaseView, name='use_cases_view'),
]