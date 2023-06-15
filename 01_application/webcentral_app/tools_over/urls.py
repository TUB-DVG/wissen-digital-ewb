from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tool_list'),
    path('<str:id>', views.toolView, name='tool_view'),
    path('Post_Review/<str:id>', views.postReview, name='post_review'),

]
