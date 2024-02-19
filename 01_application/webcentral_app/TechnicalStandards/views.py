
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import TechnicalStandard, Norm, Protocol
"""
path('', views.index, name='TechnicalStandards'),
path('norm', views.norm, name='TechnicalStandards_norm_list'),
path('protocol', views.protocol, name='TechnicalStandards_protocol_list'),
path('<str:id>', views.detailView, name='TechnicalStandards_details'),
"""
class UpdateProperties:
    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass

def index(request):
    return render(request, 'TechnicalStandards/explanation.html')

def norm(request):
    """
    shows the list of all NORMs including some key features
    """
    norms = Norm.objects.all()
    filteredBy = [None]*2 #3
    searched=None

    if ((request.GET.get("n") != None)| (request.GET.get("s") != None) |(request.GET.get("searched") != None)): #(request.GET.get("n") != None) |
        name=request.GET.get('n')
        source=request.GET.get('s')
        #link=request.GET.get('l')
        searched=request.GET.get('searched')
        norms=Norm.objects.filter(source__icontains=source,name__icontains=name,shortDescription__icontains=searched) #name__icontains=Name,
        filteredBy = [name,source]
              
    norms = list(sorted(norms, key=lambda obj:obj.name))

    normsPaginator= Paginator(norms,12)

    pageNum= request.GET.get('page',None)
    page=normsPaginator.get_page(pageNum)

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    

    if isAjaxRequest:
        html = render_to_string(
            template_name="TechnicalStandards/norm-listings-results.html", 
            context = {
                'page': page,
                'search':searched,
                'name': filteredBy[0],
                'source': filteredBy[1],
                #'link': filteredBy[1]
            }

        )

        dataDict = {"html_from_view": html}

        return JsonResponse(data=dataDict, safe=False)

       
    context = {
        'page': page,
        'search':searched,
        'name': filteredBy[0],
        'source': filteredBy[1],
        #'link': filteredBy[1]
    }
    return render(request, 'TechnicalStandards/norm-listings.html', context)
    
def normDetailView(request, id):
    """
    shows of the key features of one norm
    """
    norms = get_object_or_404(Norm, pk= id)
    # bezeichnung (DIN etc), titel, kurzbeschreibung,quelle, link
    name = norms.name #.split(", ") ### to check if split is needed
    title = norms.title
    shortDescription = norms.shortDescription
    source = norms.source #.split(", ")
    link = norms.link
    context = {
        'technicalStandards': norms,
        'name': name,
        'shortDescription': shortDescription, 
        'title': title,
        'source': source,
        'link': link
    }
    return render(request, 'TechnicalStandards/norm-detail.html', context)

def protocol(request):
    """
    shows the list of all PROTOCOLS including some key features
    """
    protocols = Protocol.objects.all()
    filteredBy = [None]*3
    searched=None
    #communicationMediumCategory	openSourceStatus
    if ((request.GET.get("n") != None)| (request.GET.get("c") != None) |(request.GET.get("os") != None) |(request.GET.get("searched") != None)): 
        name=request.GET.get('n')
        communicationMediumCategory=request.GET.get('c')
        openSourceStatus=request.GET.get('os')
        searched=request.GET.get('searched')
        criterionProtocolsOne = Q(associatedStandards__icontains=searched)
        criterionProtocolsTwo = Q(networkTopology__icontains=searched)
        criterionProtocolsThree = Q(security__icontains=searched)
        criterionProtocolsFour = Q(name__icontains=searched)
        protocols = Protocol.objects.filter(criterionProtocolsOne |
                                                    criterionProtocolsTwo | criterionProtocolsThree | criterionProtocolsFour).filter(name__icontains=name, communicationMediumCategory__icontains=communicationMediumCategory,
                                          openSourceStatus__icontains=openSourceStatus)
        

        filteredBy = [name,communicationMediumCategory,openSourceStatus]
              
    protocols = list(sorted(protocols, key=lambda obj:obj.name))

    protocolsPaginator= Paginator(protocols,12)

    pageNum= request.GET.get('page',None)
    page=protocolsPaginator.get_page(pageNum)

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if isAjaxRequest:
        html = render_to_string(
            template_name="TechnicalStandards/protocol-listings-results.html", 
            context = {
                'page': page,
                'search':searched,
                'name': filteredBy[0],
                'communicationMediumCategory': filteredBy[1],
                'openSourceStatus': filteredBy[2]
            }

        )
        dataDict = {"html_from_view": html}
        return JsonResponse(data=dataDict, safe=False) 
    context = {
        'page': page,
        'search':searched,
        'name': filteredBy[0],
        'communicationMediumCategory': filteredBy[1],
        'openSourceStatus': filteredBy[2]
    }
    return render(request, 'TechnicalStandards/protocol-listings.html', context)
    
def protocolDetailView(request, id):
    """
    shows of the key features of one norm
    """
    protocols = get_object_or_404(Protocol, pk= id)
    # bezeichnung (DIN etc), titel, kurzbeschreibung,quelle, link
    name = protocols.name #.split(", ") ### to check if split is needed
    link = protocols.link
    communicationMediumCategory = protocols.communicationMediumCategory
    supportedTransmissionMediuems = protocols.supportedTransmissionMediuems
    associatedStandards = protocols.associatedStandards
    openSourceStatus = protocols.openSourceStatus
    licensingFeeRequirement = protocols.licensingFeeRequirement
    networkTopology = protocols.networkTopology
    security = protocols.security
    bandwidth = protocols.bandwidth
    frequency = protocols.frequency
    range = protocols.range
    numberOfConnectedDevices = protocols.numberOfConnectedDevices
    dataModelArchitecture = protocols.dataModelArchitecture
    discovery = protocols.discovery
    multiMaster = protocols.multiMaster
    packetSize = protocols.packetSize
    priorities = protocols.priorities
    price = protocols.price
    osiLayers = protocols.osiLayers
    buildingAutomationLayer = protocols.buildingAutomationLayer
    context = {
        'technicalStandards': protocols,
        'name': name,
        'link': link,
        'communicationMediumCategory ': communicationMediumCategory,
        'supportedTransmissionMediuems': supportedTransmissionMediuems,
        'associatedStandards': associatedStandards,
        'openSourceStatus': openSourceStatus,
        'licensingFeeRequirement': licensingFeeRequirement,
        'networkTopology': networkTopology,
        'security': security,
        'bandwidth': bandwidth,
        'frequency': frequency,
        'range': range,
        'numberOfConnectedDevices': numberOfConnectedDevices,
        'dataModelArchitecture': dataModelArchitecture,
        'discovery': discovery,
        'multiMaster': multiMaster,
        'packetSize': packetSize,
        'priorities': priorities,
        'price': price,
        'osiLayers': osiLayers,
        'buildingAutomationLayer': buildingAutomationLayer
    }
    return render(request, 'TechnicalStandards/protocol-detail.html', context)

def protocolComparison(request):
    ids = request.GET.getlist('id')  # Retrieve list of ids from GET parameters
    protocols = []
    for id in ids:
        protocol = get_object_or_404(Protocol, pk=id)
        protocols.append(protocol)
    
    context = {
        'protocols': protocols
    }

    return render(request, 'TechnicalStandards/protocol-comparison.html', context)