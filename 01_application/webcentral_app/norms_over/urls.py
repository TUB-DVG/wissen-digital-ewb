from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='norm_list'),
    path('<str:id>', views.normView, name='norm_view'),
    path('Post_Review/<str:id>', views.postReview, name='post_review'),

]
