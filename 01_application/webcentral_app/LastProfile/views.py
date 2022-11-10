from django.shortcuts import render

# Create your views here.

def index(request):


    return render(request, 'LastProfile/explanation.html')

def stromlast(request):
    return render (request, 'pages/stromlast.html')


def warmelast(request):
    return render (request, 'pages/warmelast.html')

