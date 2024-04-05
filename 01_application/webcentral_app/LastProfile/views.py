from django.shortcuts import render
from django.utils.translation import get_language

def index(request):

    request.session['current_language'] = get_language()
    return render(request, 'LastProfile/explanation.html')

def stromlast(request):
    request.session['current_language'] = get_language()
    return render (request, 'pages/stromlast.html')


def warmelast(request):
    return render (request, 'pages/warmelast.html')

