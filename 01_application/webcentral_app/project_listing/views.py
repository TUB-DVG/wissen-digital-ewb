from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Teilprojekt # maybe I need also the other models

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    projects = Teilprojekt.objects.all() # reads all data from table Teilprojekt

    project_paginator= Paginator (projects,9)

    page_num= request.GET.get('page')
    page=project_paginator.get_page(page_num)

    context = {
        'page': page
    }

    return render(request, 'project_listing/course-grid.html', context)

def project_view(request, fkz):
    """
    shows of the key features one project
    """
    projekt = get_object_or_404(Teilprojekt, pk= fkz)
    context = {
        'projekt': projekt
    }

    return render(request, 'project_listing/project_view.html', context)

def search(request):
    """
    search page
    """
    return render(request, 'project_listing/search.html')
