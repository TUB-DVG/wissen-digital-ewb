
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import (
    TechnicalStandard, 
    Norm, 
    Protocol,
)


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

    if ((request.GET.get("name") != None)| (request.GET.get("source") != None) |(request.GET.get("searched") != None)): #(request.GET.get("n") != None) |
        name=request.GET.get(_('Bezeichnung'), "")
        source=request.GET.get("source", "")
        #link=request.GET.get('l')
        searched=request.GET.get('searched', "")
        norms=Norm.objects.filter(source__icontains=source,name__icontains=name,shortDescription__icontains=searched) #name__icontains=Name,
        filteredBy = [name,source]
              
    norms = list(sorted(norms, key=lambda obj:obj.name))

    normsPaginator= Paginator(norms,12)

    pageNum= request.GET.get('page',None)
    page=normsPaginator.get_page(pageNum)

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"

    context = {
        'page': page,
        'search':searched,
        'name': filteredBy[0],
        'source': filteredBy[1],
        "nameOfTemplate": "norms",
        "focusBorder": "technical",
        "urlName": "TechnicalStandards_norm_list",
        "optionList": [
            {
                "placeholder": _("Bezeichnung"), 
                "objects": [
                    "ANSI / ASHRAE Standard 140-2017 - Standard Method of Test for the Evaluation of Building Energy Analysis Computer Programs",
                    "Arbeitsstättenrichtllinie ASR A4.1",
                    "BISKO",
                    "DIN 14095",
                    "DIN 14675",
                    "DIN 18017-3",
                    "DIN 18599",
                    "DIN 1946-6",
                    "DIN 1986-100",
                    "DIN 1988",
                    "DIN 1988-300",
                    "DIN 2000",
                    "DIN 276",
                    "DIN 4108",
                    "DIN 4108 Beiblatt 2",
                    "DIN 4108-2",
                    "DIN 4108-3",
                    "DIN 4108-6",
                    "DIN 4109-1",
                    "DIN 4701-10/12",
                    "DIN 4708",
                    "DIN 4753",
                    "DIN EN 12056-2",
                    "DIN EN 12056-3",
                    "DIN EN 12502 1-5",
                    "DIN EN 1264-1",
                    "DIN EN 12831-1",
                    "DIN EN 12831-Beiblatt 2",
                    "DIN EN 15450",
                    "DIN EN 16798-1",
                    "DIN EN 1717",
                    "DIN EN 442-1",
                    "DIN EN 442-2",
                    "DIN EN ISO 10077-02",
                    "DIN EN ISO 10211",
                    "DIN SPEC 15240",
                    "DIN V 18599-9",
                    "DIN/TS 12831-1:2020-04",
                    "DVGW W 291",
                    "DVGW W 293",
                    "DVGW W 294",
                    "DVGW W551",
                    "DVGW W553",
                    "DVGW-TRGI 2018",
                    "DVGW-VP 670",
                    "EN 1264-1",
                    "EN 1264-2",
                    "EN 13384-1",
                    "EN 13384-2",
                    "EN 13384-3",
                    "EN 806 Teil 1 und 2",
                    "EN ISO 13788",
                    "EN ISO 6946",
                    "GPC",
                    "ISO 14.064",
                    "ISO 50.001",
                    "ISO 50.006",
                    "OENORM H 7500-1",
                    "TrinkwV",
                    "VDI 2078",
                    "VDI 2081",
                    "VDI 3805",
                    "VDI 4650",
                    "VDI 6007 Blatt 1",
                    "VDI 6007 Blatt 2",
                    "VDI 6023",
                    "ÖNORM EN 12831-1",
                    "ÖNORM EN 12831-3",
                ],
                "filter": filteredBy[0],
                "fieldName": "name",
            },
            {
                "placeholder": _("Quelle"), 
                "objects": [
                    "https://ghgprotocol.org/",
                    "Leitfaden Trinkwassererwärmung - Bundesverband Wärmepumpe",
                    "ENEKA - Energiekartenkartografie",
                    "Hottgenroth Software Katalog",
                ],
                "fieldName": "source",
                "filter": filteredBy[1],
            },
        ],     
    }

    if isAjaxRequest:
        html = render_to_string(
            template_name="TechnicalStandards/norm-listings-results.html",
            context=context,
        )

        dataDict = {"html_from_view": html}
        return JsonResponse(data=dataDict, safe=False)



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
        'link': link,
        "focusBorder": "technical",
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
    if ((request.GET.get("name") != None)| (request.GET.get("transmission") != None) |(request.GET.get("oss") != None) |(request.GET.get("searched") != None)): 
        name=request.GET.get('name', "")
        communicationMediumCategory=request.GET.get("transmission", "")
        openSourceStatus=request.GET.get("oss", "")
        searched=request.GET.get('searched', "")
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

    context = {
        'page': page,
        'search':searched,
        'name': filteredBy[0],
        'communicationMediumCategory': filteredBy[1],
        'openSourceStatus': filteredBy[2],
        "nameOfTemplate": "protocols",
        "urlName": "TechnicalStandards_protocol_list",
        "optionList": [
            {
                "placeholder": "Name", 
                "objects": [
                    "BACnet",
                    "KNX",
                    "Zigbee",
                    "Modbus",
                    "MQTT",
                    "LonWorks",
                    "OPC UA",
                    "DALI",
                    "EnOcean",
                    "LoRaWan",
                    "m-Bus",
                    "profibus",
                ],
                "filter": filteredBy[0],
                "fieldName": "name",
            },
            {
                "placeholder": "Übertragungsmethoden", 
                "objects": [
                    _("Verkabelt") +" & " + _("Drahtlos"),
                    _("Drahtlos"),
                    _("Verkabelt"), 
                ],
                "filter": filteredBy[1],
                "fieldName": "transmission",
            },
            {
                "placeholder": _("Open-Source-Status"),
                "objects": [
                    "Open Source",
                    _("Proprietär"),
                ],
                "filter": filteredBy[2],
                "fieldName": "oss",
            }
        ],
        "focusBorder": "technical",
    }

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if isAjaxRequest:
        html = render_to_string(
            template_name="TechnicalStandards/protocol-listings-results.html", 


        )
        dataDict = {"html_from_view": html}
        return JsonResponse(data=dataDict, safe=False) 

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
        'buildingAutomationLayer': buildingAutomationLayer,
        "focusBorder": "technical",
    }
    return render(request, 'TechnicalStandards/protocol-detail.html', context)

def protocolComparison(request):
    ids = request.GET.getlist('id')  # Retrieve list of ids from GET parameters
    protocols = []
    for id in ids:
        protocol = get_object_or_404(Protocol, pk=id)
        protocols.append(protocol)
    
    context = {
        'protocols': protocols,
        "focusBorder": "technical",
    }

    return render(request, 'TechnicalStandards/protocol-comparison.html', context)