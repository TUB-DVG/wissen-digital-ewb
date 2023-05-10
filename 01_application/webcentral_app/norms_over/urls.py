from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='norm_list'),
    path('<str:id>', views.norm_view, name='norm_view'),
    path('Post_Review/<str:id>', views.Post_Review, name='Post_Review'),

]
