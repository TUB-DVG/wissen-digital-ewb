"""views of pages app."""
from django.shortcuts import render


def index(request):
    """Call render function for index page."""
    return render(request, 'pages/index.html')


def Datenschutzhinweis(request):
    """Call render function for datenschutzhinweis page."""
    return render(request, 'pages/Datenschutzhinweis.html')


def about(request):
    """Call render function for about page."""
    return render(request, 'pages/about.html')


def coming(request):
    """Call render function for coming soon page."""
    return render(request, 'pages/coming.html')


def businessModelsDev(request):
    """Call render function for business models development page."""
    return render(request, 'pages/businessModelsDev.html')
