from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Teilprojekt, Tools # maybe I need also the other models

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


def tool_view(request, id):
    """
    shows of the key features one project
    """
    tool = get_object_or_404(Tools, pk= id)
    kategorien = tool.kategorie.split(", ")
    laufende_updates = tool.letztes_update
    
    #keine infos zu updates
    update_class = 'bi bi-patch-exclamation-fill'
    update_text='letztes Update'
    if (tool.letztes_update == 'laufend'):
        update_class  = 'fas fa-sync'
        update_text = 'Updates'


    context = {
        'tool': tool,
        'kategorien': kategorien,
        'letztes_update_class': update_class,
        'letztes_update_text': update_text,
    }

    return render(request, 'project_listing/tool-detail.html', context)


def search(request):
    if request.method=='POST':
        searched=request.POST['searched']
        results=Teilprojekt.objects.filter(fkz__contains=searched)
    return render(request,'project_listing/search.html',{'searched':searched,'data':results})
   
