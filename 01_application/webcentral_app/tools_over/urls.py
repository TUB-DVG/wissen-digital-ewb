from django.urls import path

from . import views

urlpatterns = [
    path('', views.Tools_view, name='Tools_view'),
    
]
