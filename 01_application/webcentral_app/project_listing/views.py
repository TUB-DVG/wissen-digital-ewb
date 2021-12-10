from django.shortcuts import render

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    return render(request, 'project_listing/project_list.html')

def project_view(request):
    """
    shows of the key features one project
    """
    return render(request, 'project_listing/project_view.html')

def search(request):
    """
    search page
    """
    return render(request, 'project_listing/search.html')
