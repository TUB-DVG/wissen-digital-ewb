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


def businessModelsChallenge(request):
    """Call render function for business models challenge page."""
    return render(request, 'pages/businessModelsChallenge.html')


def businessModelsPractice(request):
    """Call render function for business models best practice page."""
    return render(request, 'pages/businessModelsPractice.html')


def userIntegrationPractice(request):
    """Call render function for user integration best practice page."""
    return render(request, 'pages/userIntegrationPractice.html')
