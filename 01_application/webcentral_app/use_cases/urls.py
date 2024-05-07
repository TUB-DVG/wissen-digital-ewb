from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='use_cases_list'),
    path('TimeSeries/',views.dashboard_view, name ='use_cases_time_graph'),
    path('<str:id>', views.useCaseView, name='use_cases_view'),
]
