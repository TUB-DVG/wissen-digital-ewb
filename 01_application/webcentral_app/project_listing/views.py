from django.shortcuts import render, get_object_or_404

from .models import Teilprojekt # maybe I need also the other models

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    projects = Teilprojekt.objects.all() # reads all data from table Teilprojekt

    context = {
        'projects': projects
    }

    return render(request, 'project_listing/project_list.html', context)

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
