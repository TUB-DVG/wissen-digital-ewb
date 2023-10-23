
from django.urls import path

from . import views


urlpatterns = [path('', views.index, name = 'publicationPage'),
               path('<str:id>', views.publicationView, name='publicationDetails'),
               path('download_pdf/<int:pk>/', views.download_pdf, name="download_pdf"),

]
