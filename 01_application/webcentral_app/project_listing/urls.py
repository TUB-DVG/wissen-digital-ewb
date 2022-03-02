from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tool_list'),
    path('<int:id>', views.tool_view, name='tool_view'),
    path('search', views.search, name='search'),
]
