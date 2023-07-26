from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tool_list'),
    path('<str:id>', views.toolView, name='tool_view'),
    path('buisnessApps/', views.indexBuisnessApplication, name='buisnessModelApplication'),
    path('buisnessApps/<str:id>', views.buisnessApplicationView, name='buisnessAppView'),
]
