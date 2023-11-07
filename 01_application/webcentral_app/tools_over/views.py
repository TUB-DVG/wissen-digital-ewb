"""Definitions of the views of the tools overview app."""

# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
# maybe I need also the other models
from tools_over.models import (
    Tools,
    Usage,
    Accessibility,
    LifeCyclePhase,
)
# from project_listing.models import Subproject

class UpdateProperties:
    """It shoud be needed to update the icons for the function tool view."""

    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass


def index(request):
    """Shows the list of all projects including some key features."""
    tools = Tools.objects.filter(
        # classification__classification="Digitales Werkzeug", 
        focus__focus="technisch",
    ) # reads all data from table Teilprojekt
    filteredBy = [None]*3
    searched=None
 
    if ((request.GET.get("u") != None) |(request.GET.get("l") != None)| 
        (request.GET.get("lcp") != None) |(request.GET.get("searched") != None)):
        usage = request.GET.get('u')
        accessibility = request.GET.get('l')
        lifeCyclePhase = request.GET.get('lcp')
        searched = request.GET.get('searched')
        
        criterionToolsOne = Q(programmingLanguages__icontains=searched)
        criterionToolsTwo = Q(scale__scale__icontains=searched)
        criterionToolsThree = Q(classification__classification__icontains=searched)
        criterionToolsFour = Q(name__icontains=searched)
        tools = Tools.objects.filter(criterionToolsOne | criterionToolsTwo | criterionToolsThree | criterionToolsFour).filter(name__icontains=searched,  usage__usage__icontains=usage, lifeCyclePhase__lifeCyclePhase__icontains=lifeCyclePhase,
                        accessibility__accessibility__icontains=accessibility,
                        focus__focus="technisch"
                        # classification__classification="Digitales Werkzeug",
        ).distinct() #.annotate(num_features=Count('id'))#.filter(num_features__gt=1)
        # having distinct removes the duplicates, 
        # but filters out e.g., solely open-source tools!
        filteredBy = [usage, accessibility, lifeCyclePhase]
              
    tools = list(sorted(tools, key=lambda obj:obj.name))  
    toolsPaginator= Paginator(tools,12)
    pageNum= request.GET.get('page',None)
    page=toolsPaginator.get_page(pageNum)

    usageElements = Usage.objects.all()
    usageNames = []
    for currentUsage in usageElements:
        usageNames.append(currentUsage.usage)

    accessibilityElements = Accessibility.objects.all()
    accessibilityNames = []
    for currentAccessibility in accessibilityElements:
        accessibilityNames.append(currentAccessibility.accessibility)

    lifeCyclePhaseElements = LifeCyclePhase.objects.all()
    lifeCyclePhaseNames = []
    for currentLifeCyclePhase in lifeCyclePhaseElements:
        lifeCyclePhaseNames.append(currentLifeCyclePhase.lifeCyclePhase)
    

    context = {
        'page': page,
        'search':searched,
        'usage': filteredBy[0],
        'accessibility': filteredBy[1],
        'lifeCyclePhase': filteredBy[2],
        'usageFields': usageNames,
        'accessibilityFields': accessibilityNames,
        'lifeCyclePhaseFields': lifeCyclePhaseNames,
    }

    return render(request, 'tools_over/tool-listings.html', context)

def indexBuisnessApplication(request):
    """serves a request for digital applications search
    
    """
    applications = Tools.objects.filter(
        # classification__classification="Digitale Anwendung", 
        focus__focus="betrieblich"
    ) # reads all data from table Teilprojekt
    usage = request.GET.get('u')
    accessibility = request.GET.get('l')
    lifeCyclePhase = request.GET.get('lcp')
    searched = request.GET.get('searched')
    filteredBy = [None]*3
    searched=None
 
    if ((request.GET.get("u") != None) |(request.GET.get("l") != None)| 
        (request.GET.get("lcp") != None) |(request.GET.get("searched") != None)):
        usage = request.GET.get('u')
        licence = request.GET.get('l')
        lifeCyclePhase = request.GET.get('lcp')
        searched = request.GET.get('searched')
        
        criterionToolsOne = Q(programmingLanguages__icontains=searched)
        criterionToolsTwo = Q(scale__scale__icontains=searched)
        criterionToolsThree = Q(classification__classification__icontains=searched)
        criterionToolsFour = Q(name__icontains=searched)
        applications = Tools.objects.filter(criterionToolsOne | criterionToolsTwo | criterionToolsThree | criterionToolsFour).filter(name__icontains=searched,  usage__usage__icontains=usage, lifeCyclePhase__lifeCyclePhase__icontains=lifeCyclePhase,
                        accessibility__accessibility__icontains=accessibility,
                        focus__focus="betrieblich"
                        # classification__classification="Digitales Werkzeug",
        ).distinct() #.annotate(num_features=Count('id'))#.filter(num_features__gt=1)
        # having distinct removes the duplicates, 
        # but filters out e.g., solely open-source tools!
        filteredBy = [usage, accessibility, lifeCyclePhase]
              
    applications = list(sorted(applications, key=lambda obj:obj.name))
    toolsPaginator= Paginator(applications,12)
    pageNum= request.GET.get('page',None)
    page=toolsPaginator.get_page(pageNum)

    usageElements = Usage.objects.all()
    usageNames = []
    for currentUsage in usageElements:
        usageNames.append(currentUsage.usage)

    accessibilityElements = Accessibility.objects.all()
    accessibilityNames = []
    for currentAccessibility in accessibilityElements:
        accessibilityNames.append(currentAccessibility.accessibility)

    lifeCyclePhaseElements = LifeCyclePhase.objects.all()
    lifeCyclePhaseNames = []
    for currentLifeCyclePhase in lifeCyclePhaseElements:
        lifeCyclePhaseNames.append(currentLifeCyclePhase.lifeCyclePhase)

    context = {
        'page': page,
        'search':searched,
        'usage': filteredBy[0],
        'licence': filteredBy[1],
        'lifeCyclePhase': filteredBy[2],
        'usageFields': usageNames,
        'accessibilityFields': accessibilityNames,
        'lifeCyclePhaseFields': lifeCyclePhaseNames,
    }

    return render(request, 'tools_over/buisnessApplications-listings.html', context)  

def buisnessApplicationView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk= id)
    applicationAreas = tool.applicationArea.all()
    usages = tool.usage.all()#.split(", ")
    targetGroups = tool.targetGroup.all()
    lifeCyclePhases = tool.lifeCyclePhase.all()#.split(", ")
    userInterfaces = tool.userInterface.all()
    accessibilities = tool.accessibility.all()
    specificApplications = tool.specificApplication.all()
    scales = tool.scale.all()
    technicalStandardsNorms = tool.technicalStandardsNorms.all()
    technicalStandardsProtocols = tool.technicalStandardsProtocols.all()
    classifications = tool.classification.all() 
    focus = tool.focus.all()
    resources = tool.resources.split(", ")
    
    continuousUpdates = tool.lastUpdate

    lastUpdate = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    continuousUpdates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    updateProperties = lastUpdate
    if (tool.lastUpdate == 'laufend'): # continuous
        updateProperties = continuousUpdates


    context = {
        'tool': tool,
        'applicationAreas': ', '.join([a.applicationArea for a in applicationAreas]),
        'usages': ', '.join([a.usage for a in usages]),
        'targetGroups': ', '.join([a.targetGroup for a in targetGroups]),
        'lifeCyclePhases': ', '.join([a.lifeCyclePhase for a in lifeCyclePhases]),
        'userInterfaces': ', '.join([a.userInterface for a in userInterfaces]),
        'accessibilities': ', '.join([a.accessibility for a in accessibilities]),
        'specificApplications': [str(a.referenceNumber_id) for a in specificApplications], #specificApplications, #
        'scales': ', '.join([a.scale for a in scales]),
        'technicalStandardsNorms': ', '.join([a.technicalStandardsNorms for a in technicalStandardsNorms]),
        'technicalStandardsProtocols': ', '.join([a.technicalStandardsProtocols for a in technicalStandardsProtocols]),
        'classifications': ', '.join([a.classification for a in classifications]),
        'focus': ', '.join([a.focus for a in focus]),       
        'resources': resources,
        'lastUpdate': updateProperties,
        'lastUpdateClass': updateProperties.className,
        'lastUpdateColor': updateProperties.colorClass,
        'lastUpdateLabel': updateProperties.label,
       
    }

    return render(request, 'tools_over/buisnessApplications-detail.html', context)


def toolView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk= id)
    applicationAreas = tool.applicationArea.all()
    usages = tool.usage.all()#.split(", ")
    targetGroups = tool.targetGroup.all()
    lifeCyclePhases = tool.lifeCyclePhase.all()#.split(", ")
    userInterfaces = tool.userInterface.all()
    accessibilities = tool.accessibility.all()
    specificApplications = tool.specificApplication.all()
    scales = tool.scale.all()
    technicalStandardsNorms = tool.technicalStandardsNorms.all()
    technicalStandardsProtocols = tool.technicalStandardsProtocols.all()
    classifications = tool.classification.all() 
    focus = tool.focus.all()
    resources = tool.resources.split(", ")
    
    continuousUpdates = tool.lastUpdate
    
    lastUpdate = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    continuousUpdates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    updateProperties = lastUpdate
    if (tool.lastUpdate == 'laufend'): # continuous
        updateProperties = continuousUpdates


    context = {
        'tool': tool,
        'applicationAreas': ', '.join([a.applicationArea for a in applicationAreas]),
        'usages': ', '.join([a.usage for a in usages]),
        'targetGroups': ', '.join([a.targetGroup for a in targetGroups]),
        'lifeCyclePhases': ', '.join([a.lifeCyclePhase for a in lifeCyclePhases]),
        'userInterfaces': ', '.join([a.userInterface for a in userInterfaces]),
        'accessibilities': ', '.join([a.accessibility for a in accessibilities]),
        'specificApplications': [str(a.referenceNumber_id) for a in specificApplications], #specificApplications, #
        'scales': ', '.join([a.scale for a in scales]),
        'technicalStandardsNorms': ', '.join([a.technicalStandardsNorms for a in technicalStandardsNorms]),
        'technicalStandardsProtocols': ', '.join([a.technicalStandardsProtocols for a in technicalStandardsProtocols]),
        'classifications': ', '.join([a.classification for a in classifications]),
        'focus': ', '.join([a.focus for a in focus]),       
        'resources': resources,
        'lastUpdate': updateProperties,
        'lastUpdateClass': updateProperties.className,
        'lastUpdateColor': updateProperties.colorClass,
        'lastUpdateLabel': updateProperties.label,
       
    }

    return render(request, 'tools_over/tool-detail.html', context)
