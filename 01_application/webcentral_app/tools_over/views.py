from contextlib import nullcontext
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Tools # maybe I need also the other models

# Create your views here.

class UpdateProperties:
    def __init__(self, class_name, label, color_class):
        self.class_name = class_name
        self.label = label
        self.color_class = color_class

def index(request):
    """
    shows the list of all projects including some key features
    """
    tools = Tools.objects.all() # reads all data from table Teilprojekt

    project_paginator= Paginator (tools,12)

    page_num= request.GET.get('page',None)
    page=project_paginator.get_page(page_num)

    filtered_by = [None]*3
    if (request.method=='GET' and ((request.GET.get("1") != None) |(request.GET.get("2") != None)| (request.GET.get("3") != None)) ):
        
        Kategorie=request.GET.get('1')
        Lizenz=request.GET.get('2')
        Lebenszyklusphase=request.GET.get('3')
        results=Tools.objects.filter(kategorie__contains=Kategorie,lebenszyklusphase__contains=Lebenszyklusphase,lizenz__contains=Lizenz)
        project_paginator= Paginator (results,12)
        page_num= request.GET.get('page')
        page=project_paginator.get_page(page_num)
        filtered_by = [Kategorie, Lizenz, Lebenszyklusphase]
       
    context = {
        'page': page,
        'kategorie': filtered_by[0],
        'lizenz': filtered_by[1],
        'lebenszyklusphase': filtered_by[2]
    }
    return render(request, 'tools_over/tool-listings.html', context)


def tool_view(request, id):
    """
    shows of the key features one project
    """
    tool = get_object_or_404(Tools, pk= id)
    kategorien = tool.kategorie.split(", ")
    lebenszyklusphasen = tool.lebenszyklusphase.split(", ")
    laufende_updates = tool.letztes_update
    
    letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    update_properties = letztes_update
    if (tool.letztes_update == 'laufend'):
        update_properties = laufende_updates


    context = {
        'tool': tool,
        'kategorien': kategorien,
        'lebenszyklusphasen': lebenszyklusphasen,
        'letztes_update': update_properties,
        'letztes_update_class': update_properties.class_name,
        'letztes_update_color': update_properties.color_class,
        'letztes_update_label': update_properties.label
    }

    return render(request, 'tools_over/tool-detail.html', context)