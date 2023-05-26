"""View functions for start page and start page search."""
from django.shortcuts import render


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, 'StartSearch/StartSearch.html')
