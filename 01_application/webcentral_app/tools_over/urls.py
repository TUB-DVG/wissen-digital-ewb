from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tool_list'),
    path('<str:id>', views.tool_view, name='tool_view'),
    path('Post_Review/<str:id>', views.Post_Review, name='Post_Review'),

]
