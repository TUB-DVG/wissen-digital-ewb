from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Teilprojekt , Tools # maybe I need also the other models

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    projects = Tools.objects.all() # reads all data from table Teilprojekt

    project_paginator= Paginator (projects,12)

    page_num= request.GET.get('page',None)
    page=project_paginator.get_page(page_num)

    #category_view=Tools.objects.filter(kategorie_contains=)
    if (request.method=='GET' and ((request.GET.get("1") != None) |(request.GET.get("2") != None)| (request.GET.get("3") != None)) ):
        
        Category=request.GET.get('1')
        Lizenz=request.GET.get('2')
        Lebenszyklusphase=request.GET.get('3')
        results=Tools.objects.filter(kategorie__contains=Category,lebenszyklusphase__contains=Lebenszyklusphase,lizenz__contains=Lizenz)
        project_paginator= Paginator (results,12)
        page_num= request.GET.get('page')
        page=project_paginator.get_page(page_num)
       
    context = {
        'page': page,
   
    }

    return render(request, 'project_listing/course-grid-2.html', context)

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
    if request.method=='POST':
        searched=request.POST['searched']
        results=Teilprojekt.objects.filter(fkz__contains=searched)
    return render(request,'project_listing/search.html',{'searched':searched,'data':results})
   
