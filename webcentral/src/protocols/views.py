from django.shortcuts import render
from django.db.models import Q
from django.utils.translation import gettext as _
from common.views import createQ
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Protocol


def protocol(request):
    """
    shows the list of all PROTOCOLS including some key features
    """
    protocols = Protocol.objects.all()
    filteredBy = [None] * 3
    searched = None

    filtering = bool(request.GET.get("filtering", False))

    nameElements = request.GET.get("name-hidden", "")
    nameElementsList = nameElements.split(",")

    transmissionElements = request.GET.get("transmission-hidden", "")
    transmissionElementsList = transmissionElements.split(",")

    ossElements = request.GET.get("oss-hidden", "")
    ossElementsList = ossElements.split(",")

    listOfFilters = [
        {
            "filterValues": nameElementsList,
            "filterName": "name__icontains",
        },
        {
            "filterValues": transmissionElementsList,
            "filterName": "supportedTransmissionMediuems__icontains",
        },
        {
            "filterValues": ossElementsList,
            "filterName": "license__openSourceStatus__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    # communicationMediumCategory	openSourceStatus
    # if ((request.GET.get("name") != None)| (request.GET.get("transmission") != None) |(request.GET.get("oss") != None) |(request.GET.get("searched") != None)):
    #     name=request.GET.get('name', "")
    #     communicationMediumCategory=request.GET.get("transmission", "")
    #     openSourceStatus=request.GET.get("oss", "")
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionProtocolsOne = Q(associatedStandards__icontains=searched)
        criterionProtocolsTwo = Q(networkTopology__icontains=searched)
        criterionProtocolsThree = Q(security__icontains=searched)
        criterionProtocolsFour = Q(name__icontains=searched)
        complexCriterion &= (
            criterionProtocolsOne
            | criterionProtocolsTwo
            | criterionProtocolsThree
            | criterionProtocolsFour
        )
    protocols = Protocol.objects.filter(complexCriterion)
    # breakpoint()
    # filteredBy = [name,communicationMediumCategory,openSourceStatus]

    protocols = list(sorted(protocols, key=lambda obj: obj.name))

    protocolsPaginator = Paginator(protocols, 12)

    pageNum = request.GET.get("page", None)
    page = protocolsPaginator.get_page(pageNum)

    context = {
        "page": page,
        "search": searched,
        "name": filteredBy[0],
        "communicationMediumCategory": filteredBy[1],
        "openSourceStatus": filteredBy[2],
        "nameOfTemplate": "protocols",
        "urlName": "TechnicalStandards_protocol_list",
        "heading": _("Überblick über technische Standards")
        + " - "
        + _("Protokolle"),
        "introductionText": _(
            """Auf dieser Seite befinden sich unterschiedliche technische Protokolle, die im Sommer 2023 und Frühjahr 2024 erfasst worden sind. Zu sehen sind zudem die unterschiedlichen Werkzeugketten, in denen die Protokolle verwendet werden."""
        ),
        "pathToExplanationTemplate": "TechnicalStandards/protocol-explanation.html",
        "listingSubHeadingOneKey": _("Reichweite"),
        "listingSubHeadingOneValue": "range",
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
                    _("Verkabelt") + " & " + _("Drahtlos"),
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
            },
        ],
        "focusBorder": "technical",
        "renderComparisonRadio": True,
        "model": "Protocols",
        "urlDetailsPage": "TechnicalStandards_protocol_details",
        "subHeading1": _("Sicherheit"),
        "subHeadingAttr1": "security",
        "subHeading2": _("Medium"),
        "subHeadingAttr2": _("supportedTransmissionMediuems"),
    }
    if filtering:
        return render(
            request,
            "partials/listing_results.html",
            context,
        )
    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if isAjaxRequest:
        html = render_to_string(
            template_name="partials/listing_results.html",
        )
        dataDict = {"html_from_view": html}
        return JsonResponse(data=dataDict, safe=False)

    return render(request, "protocols/protocols_listing.html", context)


def protocolDetailView(request, id):
    """
    shows of the key features of one norm
    """
    protocols = get_object_or_404(Protocol, pk=id)
    # bezeichnung (DIN etc), titel, kurzbeschreibung,quelle, link
    name = protocols.name  # .split(", ") ### to check if split is needed
    link = protocols.resources
    communicationMediumCategory = protocols.communicationMediumCategory
    supportedTransmissionMediuems = protocols.supportedTransmissionMediuems
    associatedStandards = protocols.associatedStandards

    licensesForProtocol = protocols.license.all()
    # openSourceStatusStr = ""
    # licensingFeeRequirementStr = ""
    # for license in licensesForProtocol:
    #     openSourceStatusStr += license.openSourceStatus + ", "
    #     licensingFeeRequirementStr += license.licensingFeeRequirement + ", "
    #
    openSourceStatus = protocols.license.all()
    licensingFeeRequirement = protocols.license.all()
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
        "technicalStandards": protocols,
        "name": name,
        "link": link,
        "communicationMediumCategory ": communicationMediumCategory,
        "supportedTransmissionMediuems": supportedTransmissionMediuems,
        "associatedStandards": associatedStandards,
        "openSourceStatus": openSourceStatus,
        "licensingFeeRequirement": licensingFeeRequirement,
        "networkTopology": networkTopology,
        "security": security,
        "bandwidth": bandwidth,
        "frequency": frequency,
        "range": range,
        "numberOfConnectedDevices": numberOfConnectedDevices,
        "dataModelArchitecture": dataModelArchitecture,
        "discovery": discovery,
        "multiMaster": multiMaster,
        "packetSize": packetSize,
        "priorities": priorities,
        "price": price,
        "osiLayers": osiLayers,
        "buildingAutomationLayer": buildingAutomationLayer,
        "focusBorder": "technical",
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Protokolle"),
        "backLink": "TechnicalStandards_protocol_list",
    }
    context["boxObject"] = protocols
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "protocols/details_right_column.html"
    return render(request, "pages/details_page.html", context)


def protocolComparison(request):
    ids = request.GET.getlist("id")  # Retrieve list of ids from GET parameters
    protocols = []
    for id in ids:
        protocol = get_object_or_404(Protocol, pk=id)
        protocols.append(protocol)

    context = {
        "protocols": protocols,
        "focusBorder": "technical",
    }

    return render(
        request, "TechnicalStandards/protocol-comparison.html", context
    )
