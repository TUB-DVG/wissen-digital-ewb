from django.shortcuts import render
from django.utils.translation import get_language

def index(request):
    context = {
        "focusBorder": "technical",
    }
    request.session['current_language'] = get_language()
    return render(request, 'LastProfile/explanation.html', context)

def stromlast(request):
    context = {
        "focusBorder": "technical",
    }   
    request.session['current_language'] = get_language()
    return render (request, 'pages/stromlast.html', context)


def warmelast(request):
    context = {
        "focusBorder": "technical",
    }   
    return render (request, 'pages/warmelast.html', context)

