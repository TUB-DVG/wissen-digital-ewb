"""View functions for start page and start page search."""
from django.shortcuts import render


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, 'StartSearch/StartSearch.html')


def resultSearch(request):
    """View function of the result page of the central search function."""
    return render(request, 'StartSearch/ResultSearch.html')
