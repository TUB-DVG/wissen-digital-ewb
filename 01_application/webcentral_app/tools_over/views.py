"""Definitions of the views of the tools overview app."""

# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# maybe I need also the other models
from tools_over.models import Tools


class UpdateProperties:
    """It shoud be needed to update the icons for the function tool view."""

    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass


def index(request):
    """Shows the list of all projects including some key features."""
    tools = Tools.objects.filter(
        classification__classification="Digitales Werkzeug", 
        focus__focus="Technisch",
    ) # reads all data from table Teilprojekt
    filteredBy = [None]*3
    searched=None
 
    if ((request.GET.get("u") != None) |(request.GET.get("l") != None)| 
        (request.GET.get("lcp") != None) |(request.GET.get("searched") != None)):
        usage = request.GET.get('u')
        licence = request.GET.get('l')
        lifeCyclePhase = request.GET.get('lcp')
        searched = request.GET.get('searched')
        tools = Tools.objects.filter(
            usage__icontains=usage,
            lifeCyclePhase__icontains=lifeCyclePhase,
            licence__icontains=licence,
            name__icontains=searched,
            focus__focus="Technisch",
            classification__classification="Digitales Werkzeug",
        )
        filteredBy = [usage, licence, lifeCyclePhase]
              
    tools = list(sorted(tools, key=lambda obj:obj.name))
    toolsPaginator= Paginator(tools,12)
    pageNum= request.GET.get('page',None)
    page=toolsPaginator.get_page(pageNum)

    context = {
        'page': page,
        'search':searched,
        'usage': filteredBy[0],
        'licence': filteredBy[1],
        'lifeCyclePhase': filteredBy[2]
    }

    return render(request, 'tools_over/tool-listings.html', context)

def indexBuisnessApplication(request):
    """serves a request for digital applications search
    
    """
    applications = Tools.objects.filter(classification__classification="Digitale Anwendung", focus__focus="Betrieblich") # reads all data from table Teilprojekt
    
    filteredBy = [None]*3
    searched=None
 
    if ((request.GET.get("u") != None) |(request.GET.get("l") != None)| 
        (request.GET.get("lcp") != None) |(request.GET.get("searched") != None)):
        usage = request.GET.get('u')
        licence = request.GET.get('l')
        lifeCyclePhase = request.GET.get('lcp')
        searched = request.GET.get('searched')
        applications = Tools.objects.filter(
            usage__icontains=usage,
            lifeCyclePhase__icontains=lifeCyclePhase,
            licence__icontains=licence,
            name__icontains=searched,
            classification__classification="Digitale Anwendung",
            focus__focus="Betrieblich",
        )
        filteredBy = [usage, licence, lifeCyclePhase]
              
    applications = list(sorted(applications, key=lambda obj:obj.name))
    toolsPaginator= Paginator(applications,12)
    pageNum= request.GET.get('page',None)
    page=toolsPaginator.get_page(pageNum)

    context = {
        'page': page,
        'search':searched,
        'usage': filteredBy[0],
        'licence': filteredBy[1],
        'lifeCyclePhase': filteredBy[2]
    }

    return render(request, 'tools_over/buisnessApplications-listings.html', context)  

def buisnessApplicationView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk= id)
    usages = tool.usage.split(", ")
    lifeCyclePhases = tool.lifeCyclePhase.split(", ")
    continuousUpdates = tool.lastUpdate
    
    lastUpdate = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    continuousUpdates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    updateProperties = lastUpdate
    if (tool.lastUpdate == 'laufend'): # continuous
        updateProperties = continuousUpdates


    context = {
        'tool': tool,
        'usages': usages,
        'lifeCyclePhases': lifeCyclePhases,
        'lastUpdate': updateProperties,
        'lastUpdateClass': updateProperties.className,
        'lastUpdateColor': updateProperties.colorClass,
        'lastUpdateLabel': updateProperties.label,
       
    }

    return render(request, 'tools_over/buisnessApplications-detail.html', context)


def toolView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk= id)
    usages = tool.usage.split(", ")
    lifeCyclePhases = tool.lifeCyclePhase.split(", ")
    continuousUpdates = tool.lastUpdate
    
    lastUpdate = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    continuousUpdates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    updateProperties = lastUpdate
    if (tool.lastUpdate == 'laufend'): # continuous
        updateProperties = continuousUpdates


    context = {
        'tool': tool,
        'usages': usages,
        'lifeCyclePhases': lifeCyclePhases,
        'lastUpdate': updateProperties,
        'lastUpdateClass': updateProperties.className,
        'lastUpdateColor': updateProperties.colorClass,
        'lastUpdateLabel': updateProperties.label,
       
    }

    return render(request, 'tools_over/tool-detail.html', context)
