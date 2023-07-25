from django.shortcuts import render 

def index(request):
	
	return render(request, 'pages/index.html')

def Datenschutzhinweis(request):
	return render(request, 'pages/Datenschutzhinweis.html')

def about(request):
    return render(request, 'pages/about.html')


def coming(request):
    return render(request, 'pages/coming.html')



