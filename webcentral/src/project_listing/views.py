from django.shortcuts import render, get_object_or_404

from .models import Subproject # maybe I need also the other models

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    projects = Subproject.objects.all() # reads all data from table Teilprojekt

    context = {
        'projects': projects
    }

    return render(request, 'project_listing/project_list.html', context)

def project_view(request, referenceNumber_id):
    """
    shows of the key features one project
    """
    projekt = get_object_or_404(Subproject, pk= referenceNumber_id)
    context = {
        'projekt': projekt
    }

    return render(request, 'project_listing/project_view.html', context)

def search(request):
    """
    search page
    """
    return render(request, 'project_listing/search.html')
