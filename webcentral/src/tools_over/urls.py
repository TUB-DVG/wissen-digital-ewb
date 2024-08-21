from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tool_list'),
    path('<str:id>', views.toolView, name='tool_view'),
    path('technicalApps/', views.indexApps, name='app_list'),
    path('technicalApps/<str:id>', views.AppView, name='app_view'),
    path('businessApps/', views.indexBusinessApplication, name='businessModelApplication'),
    path('businessApps/<str:id>', views.businessApplicationView, name='businessAppView'),
    path('comparison/', views.toolComparison, name ='tool_comparison'),
]
