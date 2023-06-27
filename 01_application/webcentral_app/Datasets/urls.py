from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dataset_list'),
    path('<str:id>', views.dataset_view, name='dataset_view'),
    #path('Post_Review/<str:id>', views.Post_Review, name='Post_Review'),

]
