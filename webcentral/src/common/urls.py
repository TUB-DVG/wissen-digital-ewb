"""urls for the common app

"""

from django.urls import path
from . import views

urlpatterns = [
    path("comparison/", views.comparison, name="index"),
    # Add your URL patterns here
]
