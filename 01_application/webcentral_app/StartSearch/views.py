"""View functions for start page and start page search."""
from django.shortcuts import render


def index(request):
    """View function of the start page."""
    return render(request, 'StartSearch/StartSearch.html')
