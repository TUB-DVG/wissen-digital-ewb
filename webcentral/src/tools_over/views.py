"""Definitions of the views of the tools overview app."""

# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.translation import gettext as _

# maybe I need also the other models
from tools_over.models import (
    Tools,
    Usage,
    Accessibility,
    LifeCyclePhase,
)

from common.views import createQ


class UpdateProperties:
    """It shoud be needed to update the icons for the function tool view."""

    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass


def setLanguageForLastUpdate(request):
    """Sets the language for the last update."""
    if request.LANGUAGE_CODE == "de":
        lastUpdateText = "letztes Update"
    else:
        lastUpdateText = "last Update"

    lastUpdate = UpdateProperties(
        "bi bi-patch-exclamation-fill", lastUpdateText, "text-danger"
    )
    continuousUpdates = UpdateProperties(
        "fas fa-sync", "Updates", "text-success"
    )

    return lastUpdate, continuousUpdates


def index(request):
    """Shows the list of all projects including some key features."""
    tools = Tools.objects.filter(
        classification__classification_de__in=[
            "digitales Werkzeug",
            "Sprache",
            "Standard",
            "Framework/Bibliothek",
        ],
        focus__focus_de="technisch",
    )
    filteredBy = [None] * 3
    searched = None

    filtering = bool(request.GET.get("filtering", False))

    usageElements = request.GET.get("use-hidden", "")
    usageElementsList = usageElements.split(",")

    lifeCyclePhaseElements = request.GET.get("lifeCyclePhase-hidden", "")
    lifeCyclePhaseElementsList = lifeCyclePhaseElements.split(",")

    accessibilityElements = request.GET.get("accessibility-hidden", "")
    accessibilityElementsList = accessibilityElements.split(",")

    listOfFilters = [
        {
            "filterValues": usageElementsList,
            "filterName": "usage__usage__icontains",
        },
        {
            "filterValues": lifeCyclePhaseElementsList,
            "filterName": "lifeCyclePhase__lifeCyclePhase__icontains",
        },
        {
            "filterValues": accessibilityElementsList,
            "filterName": "accessibility__accessibility__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)

    # if ((request.GET.get("use") != None)
    #         | (request.GET.get("accessibility") != None)
    #         | (request.GET.get("lifeCyclePhase") != None)
    #         | (request.GET.get("searched") != None)):
    #     usage = request.GET.get("use", "")
    #     accessibility = request.GET.get("accessibility", "")
    #     lifeCyclePhase = request.GET.get("lifeCyclePhase", "")
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionToolsOne = Q(programmingLanguages__icontains=searched)
        criterionToolsTwo = Q(scale__scale__icontains=searched)
        criterionToolsThree = Q(
            classification__classification__icontains=searched
        )
        criterionToolsFour = Q(name__icontains=searched)
        complexCriterion &= (
            criterionToolsOne
            | criterionToolsTwo
            | criterionToolsThree
            | criterionToolsFour
        )
    tools = (
        Tools.objects.filter(complexCriterion)
        .filter(
            name__icontains=searched,
            classification__classification_de__in=[
                "digitales Werkzeug",
                "Sprache",
                "Standard",
                "Framework/Bibliothek",
            ],
            focus__focus_de="technisch",
        )
        .distinct()
    )  # .annotate(num_features=Count('id'))#.filter(num_features__gt=1)
    # having distinct removes the duplicates,
    # but filters out e.g., solely open-source tools!
    filteredBy = ["usage", "accessibility", "lifeCyclePhase"]

    tools = list(sorted(tools, key=lambda obj: obj.name))
    toolsPaginator = Paginator(tools, 12)
    pageNum = request.GET.get("page", None)
    page = toolsPaginator.get_page(pageNum)

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

    if request.LANGUAGE_CODE == "de":
        headingText = "Überblick über digitale Werkzeuge"
    else:
        headingText = "Overview of digital tools"

    context = {
        "accessibility": filteredBy[1],
        "focusBorder": "technical",
        "typeOfTool": "Tools",
        "introductionText": _(
            """Die hier vorgestellten digitalen Werkzeuge entsprechen den Werkzeugen, die im Rahmen der Auswertung
          des Fragebogens der wissenschaftlichen Begleitforschung der Forschungsinitiative Energiewendebauen von 
          2021 und 2023 erfasst wurden. Alle digitalen Werkzeuge werden dementsprechend von Projekten eingesetzt, 
          entwickelt oder weiterentwickelt, die im Rahmen der Forschungsinitiative Energiewendebauen gefördert werden."""
        ),
        "pathToExplanationTemplate": "tools_over/explanationTools.html",
        "page": page,
        "search": searched,
        "usage": filteredBy[0],
        "lifeCyclePhase": filteredBy[2],
        "usageFields": usageNames,
        "accessibilityFields": accessibilityNames,
        "lifeCyclePhaseFields": lifeCyclePhaseNames,
        "heading": headingText,
        "nameOfTemplate": "tools",
        "urlName": "tool_list",
        "model": "Tools",
        "optionList": [
            {
                "placeholder": "Nutzung",
                "objects": usageNames,
                "filtered": request.GET.get("use-hidden", ""),
                "fieldName": "use",
            },
            {
                "placeholder": "Zugänglichkeit",
                "objects": accessibilityNames,
                "filtered": request.GET.get("accessibility-hidden", ""),
                "fieldName": "accessibility",
            },
            {
                "placeholder": "Lebenszyklusphase",
                "objects": lifeCyclePhaseNames,
                "filtered": request.GET.get("lifeCyclePhase-hidden", ""),
                "fieldName": "lifeCyclePhase",
            },
        ],
        "renderComparisonRadio": True,
        "urlDetailsPage": "tool_view",
        "subHeading1": _("Nutzerschnittstelle"),
        "subHeadingAttr1": "userInterface__userInterface",
        "subHeading2": _("Updates"),
        "subHeadingAttr2": _("lastUpdate"),
    }

    if filtering:
        return render(request, "partials/listing_results.html", context)

    return render(request, "pages/grid_listing.html", context)


def indexApps(request):
    """Shows the list of all projects including some key features."""

    tools = Tools.objects.filter(
        classification__classification_de="digitale Anwendung",
        focus__focus_de="technisch",
    )
    filteredBy = [None] * 3
    searched = None
    filtering = bool(request.GET.get("filtering", False))
    usageElements = request.GET.get("use-hidden", "")
    usageElementsList = usageElements.split(",")

    lifeCyclePhaseElements = request.GET.get("lifeCyclePhase-hidden", "")
    lifeCyclePhaseElementsList = lifeCyclePhaseElements.split(",")

    accessibilityElements = request.GET.get("accessibility-hidden", "")
    accessibilityElementsList = accessibilityElements.split(",")

    listOfFilters = [
        {
            "filterValues": usageElementsList,
            "filterName": "usage__usage__icontains",
        },
        {
            "filterValues": lifeCyclePhaseElementsList,
            "filterName": "lifeCyclePhase__lifeCyclePhase__icontains",
        },
        {
            "filterValues": accessibilityElementsList,
            "filterName": "accessibility__accessibility__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    # if ((request.GET.get("Nutzung") != None)
    #         | (request.GET.get("Zugänglichkeit") != None)
    #         | (request.GET.get("Lebenszyklusphase") != None)
    #         | (request.GET.get("searched") != None)):
    #     usage = request.GET.get("Nutzung", "")
    #     accessibility = request.GET.get("Zugänglichkeit", "")
    #     lifeCyclePhase = request.GET.get("Lebenszyklusphase", "")
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionToolsOne = Q(programmingLanguages__icontains=searched)
        criterionToolsTwo = Q(scale__scale__icontains=searched)
        criterionToolsThree = Q(
            classification__classification__icontains=searched
        )
        criterionToolsFour = Q(name__icontains=searched)
        complexCriterion &= (
            criterionToolsOne
            | criterionToolsTwo
            | criterionToolsThree
            | criterionToolsFour
        )
    tools = (
        Tools.objects.filter(complexCriterion)
        .filter(
            name__icontains=searched,
            # usage__usage__icontains=usage,
            # lifeCyclePhase__lifeCyclePhase__icontains=lifeCyclePhase,
            # accessibility__accessibility__icontains=accessibility,
            focus__focus_de="technisch",
            classification__classification_de__in=[
                "digitale Anwendung",
                "Plattform",
            ],
        )
        .distinct()
    )  # .annotate(num_features=Count('id'))#.filter(num_features__gt=1)
    # having distinct removes the duplicates,
    # but filters out e.g., solely open-source tools!
    # filteredBy = [usage, accessibility, lifeCyclePhase]

    tools = list(sorted(tools, key=lambda obj: obj.name))
    toolsPaginator = Paginator(tools, 12)
    pageNum = request.GET.get("page", None)
    page = toolsPaginator.get_page(pageNum)

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

    if request.LANGUAGE_CODE == "de":
        headingText = "Überblick über digitale Anwendungen"
    else:
        headingText = "Overview of digital applications"

    context = {
        "accessibilityFields": accessibilityNames,
        "focusBorder": "technical",
        "typeOfTool": "Apps",
        "page": page,
        "search": searched,
        # "usage":
        # filteredBy[0],
        # "accessibility":
        # filteredBy[1],
        # "lifeCyclePhase":
        # filteredBy[2],
        "usageFields": usageNames,
        "lifeCyclePhaseFields": lifeCyclePhaseNames,
        "heading": headingText,
        "nameOfTemplate": "tools",
        "urlName": "tool_list",
        "model": "Tools",
        "introductionText": _(
            """Die hier vorgestellten digitalen Anwendungen entsprechen den Anwendungen, die im Rahmen der Auswertung des Fragebogens der wissenschaftlichen Begleitforschung der Forschungsinitiative Energiewendebauen von 2021 und 2023 erfasst wurden. 
          Alle digitalen Anwendungen werden dementsprechend von Projekten, die im Rahmen der 
          Forschungsinitiative Energiewendebauen gefördert werden, eingesetzt, entwickelt oder weiterentwickelt."""
        ),
        "pathToExplanationTemplate": "tools_over/explanationApps.html",
        "optionList": [
            {
                "placeholder": _("Nutzung"),
                "objects": usageNames,
                "filtered": request.GET.get("use-hidden", ""),
                "fieldName": "use",
            },
            {
                "placeholder": _("Zugänglichkeit"),
                "objects": accessibilityNames,
                "filtered": request.GET.get("accessibility-hidden", ""),
                "fieldName": "accessibility",
            },
            {
                "placeholder": _("Lebenszyklusphase"),
                "objects": lifeCyclePhaseNames,
                "filtered": request.GET.get("liefCyclePhase-hidden", ""),
                "fieldName": "lifeCyclePhase",
            },
        ],
        "renderComparisonRadio": True,
        "urlDetailsPage": "app_view",
        "subHeading1": _("Nutzerschnittstelle"),
        "subHeadingAttr1": "userInterface__userInterface",
        "subHeading2": _("Updates"),
        "subHeadingAttr2": _("lastUpdate"),
    }
    if filtering:
        return render(request, "partials/listing_results.html", context)

    return render(request, "pages/grid_listing.html", context)


def indexBusinessApplication(request):
    """serves a request for digital applications search"""
    applications = Tools.objects.filter(
        # classification__classification="Digitale Anwendung",
        focus__focus_de="betrieblich"
    )

    filteredBy = [None] * 3
    searched = None

    filtering = bool(request.GET.get("filtering", False))
    usageElements = request.GET.get("use-hidden", "")
    usageElementsList = usageElements.split(",")

    lifeCyclePhaseElements = request.GET.get("lifeCyclePhase-hidden", "")
    lifeCyclePhaseElementsList = lifeCyclePhaseElements.split(",")

    accessibilityElements = request.GET.get("accessibility-hidden", "")
    accessibilityElementsList = accessibilityElements.split(",")

    listOfFilters = [
        {
            "filterValues": usageElementsList,
            "filterName": "usage__usage__icontains",
        },
        {
            "filterValues": lifeCyclePhaseElementsList,
            "filterName": "lifeCyclePhase__lifeCyclePhase__icontains",
        },
        {
            "filterValues": accessibilityElementsList,
            "filterName": "accessibility__accessibility__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    searched = request.GET.get("searched", "")
    # if ((request.GET.get("Nutzung", "") != None)
    #         | (request.GET.get("Zugänglichkeit", "") != None)
    #         | (request.GET.get("Lebenszyklusphase", "") != None)
    #         | (request.GET.get("searched", "") != None)):
    #     usage = request.GET.get("Nutzung", "")
    #     accessibility = request.GET.get("Zugänglichkeit", "")
    #     lifeCyclePhase = request.GET.get("Lebenszyklusphase", "")
    #     searched = request.GET.get("searched", "")
    if searched != "":
        criterionToolsOne = Q(programmingLanguages__icontains=searched)
        criterionToolsTwo = Q(scale__scale__icontains=searched)
        criterionToolsThree = Q(
            classification__classification__icontains=searched
        )
        criterionToolsFour = Q(name__icontains=searched)
        complexCriterion |= (
            criterionToolsOne
            | criterionToolsTwo
            | criterionToolsThree
            | criterionToolsFour
        )
    applications = (
        Tools.objects.filter(complexCriterion)
        .filter(
            name__icontains=searched,
            # usage__usage__icontains=usage,
            # lifeCyclePhase__lifeCyclePhase__icontains=lifeCyclePhase,
            # accessibility__accessibility__icontains=accessibility,
            focus__focus_de="betrieblich",
            # classification__classification__icontains=searched,
            # classification__classification="Digitales Werkzeug",
        )
        .distinct()
    )  # .annotate(num_features=Count('id'))#.filter(num_features__gt=1)
    # having distinct removes the duplicates,
    # but filters out e.g., solely open-source tools!
    # filteredBy = [usage, accessibility, lifeCyclePhase]
    applications = list(sorted(applications, key=lambda obj: obj.name))
    toolsPaginator = Paginator(applications, 12)
    pageNum = request.GET.get("page", None)
    page = toolsPaginator.get_page(pageNum)

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

    if request.LANGUAGE_CODE == "de":
        headingText = "Überblick über Geschäftsmodellanwendungen"
    else:
        headingText = "Overview of Business Applications"

    context = {
        "accessibilityFields": accessibilityNames,
        "focusBorder": "operational",
        "typeOfTool": "BusinessApps",
        "page": page,
        "search": searched,
        # "usage":
        # filteredBy[0],
        # "licence":
        # filteredBy[1],
        # "lifeCyclePhase":
        # filteredBy[2],
        "introductionText": _(
            """Neben der wissenschaftlichen Entwicklung digitaler Anwendungen,
          müssen erprobte Technologien auch ökonomisch umgesetzt werden. 
          Hierzu sind Geschäftsmodelle notwendig, sodass das Potenzial der digitalen Anwendung 
          als Produkt oder Service einer möglichst breiten Anwenderschaft zur Verfügung gestellt werden kann. 
          Eine Reihe von Tools kann die Geschäftsmodellentwicklungunterstützen. Einige von diesen werden hier vorgestellt."""
        ),
        "pathToExplanationTemplate": "tools_over/explanationBusinessApps.html",
        "dontShowMore": True,
        "usageFields": usageNames,
        "lifeCyclePhaseFields": lifeCyclePhaseNames,
        "heading": headingText,
        "nameOfTemplate": "tools",
        "urlName": "businessModelApplication",
        "model": "BusinessApps",
        "optionList": [
            {
                "placeholder": "Nutzung",
                "objects": usageNames,
                "filter": filteredBy[0],
                "fieldName": "use",
            },
            {
                "placeholder": "Zugänglichkeit",
                "objects": accessibilityNames,
                "filter": filteredBy[1],
                "fieldName": "accessibility",
            },
            {
                "placeholder": "Lebenszyklusphase",
                "objects": lifeCyclePhaseNames,
                "filter": filteredBy[2],
                "fieldName": "lifeCyclePhase",
            },
        ],
        "renderComparisonRadio": True,
        "urlDetailsPage": "businessAppView",
        "subHeading1": _("Nutzerschnittstelle"),
        "subHeadingAttr1": "userInterface__userInterface",
        "subHeading2": _("Updates"),
        "subHeadingAttr2": _("lastUpdate"),
    }
    if filtering:
        return render(request, "partials/listing_results.html", context)
    return render(request, "pages/grid_listing.html", context)


def businessApplicationView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk=id)
    applicationAreas = tool.applicationArea.all()
    usages = tool.usage.all()  # .split(", ")
    targetGroups = tool.targetGroup.all()
    lifeCyclePhases = tool.lifeCyclePhase.all()  # .split(", ")
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

    lastUpdate, continuousUpdates = setLanguageForLastUpdate(request)

    # changing labels and icon
    updateProperties = lastUpdate
    if tool.lastUpdate_de == "laufend":  # continuous
        updateProperties = continuousUpdates

    context = {
        "tool": tool,
        "applicationAreas": ", ".join(
            [a.applicationArea for a in applicationAreas]
        ),
        "usages": ", ".join([a.usage for a in usages]),
        "targetGroups": ", ".join([a.targetGroup for a in targetGroups]),
        "lifeCyclePhases": ", ".join(
            [a.lifeCyclePhase for a in lifeCyclePhases]
        ),
        "userInterfaces": ", ".join([a.userInterface for a in userInterfaces]),
        "accessibilities": ", ".join(
            [a.accessibility for a in accessibilities]
        ),
        "specificApplications": [
            str(a.referenceNumber_id) for a in specificApplications
        ],  # specificApplications, #
        "scales": ", ".join([a.scale for a in scales]),
        "technicalStandardsNorms": ", ".join(
            [a.technicalStandardsNorms for a in technicalStandardsNorms]
        ),
        "technicalStandardsProtocols": ", ".join(
            [a.technicalStandardsProtocols for a in technicalStandardsProtocols]
        ),
        "classifications": ", ".join(
            [a.classification for a in classifications]
        ),
        "focus": ", ".join([a.focus for a in focus]),
        "focusBorder": "operational",
        "resources": resources,
        "lastUpdate": updateProperties,
        "lastUpdateClass": updateProperties.className,
        "lastUpdateColor": updateProperties.colorClass,
        "lastUpdateLabel": updateProperties.label,
        "imageInBackButton": "assets/images/backArrowOperational.svg",
        "backLinkText": _("Geschäftsmodellanwendungen"),
        "backLink": "businessModelApplication",
    }
    context["boxObject"] = tool
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "tools_over/details_right_column.html"
    return render(request, "pages/details_page.html", context)


def toolView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk=id)
    applicationAreas = tool.applicationArea.all()
    usages = tool.usage.all()  # .split(", ")
    targetGroups = tool.targetGroup.all()
    lifeCyclePhases = tool.lifeCyclePhase.all()  # .split(", ")
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

    lastUpdate, continuousUpdates = setLanguageForLastUpdate(request)

    # changing labels and icon
    updateProperties = lastUpdate
    if tool.lastUpdate_de == "laufend":  # continuous
        updateProperties = continuousUpdates

    context = {
        "tool": tool,
        "applicationAreas": ", ".join(
            [a.applicationArea for a in applicationAreas]
        ),
        "usages": ", ".join([a.usage for a in usages]),
        "targetGroups": ", ".join([a.targetGroup for a in targetGroups]),
        "lifeCyclePhases": ", ".join(
            [a.lifeCyclePhase for a in lifeCyclePhases]
        ),
        "userInterfaces": ", ".join([a.userInterface for a in userInterfaces]),
        "accessibilities": ", ".join(
            [a.accessibility for a in accessibilities]
        ),
        "specificApplications": [
            str(a.referenceNumber_id) for a in specificApplications
        ],  # specificApplications, #
        "scales": ", ".join([a.scale for a in scales]),
        "technicalStandardsNorms": ", ".join(
            [a.technicalStandardsNorms for a in technicalStandardsNorms]
        ),
        "technicalStandardsProtocols": ", ".join(
            [a.technicalStandardsProtocols for a in technicalStandardsProtocols]
        ),
        "classifications": ", ".join(
            [a.classification for a in classifications]
        ),
        "focus": ", ".join([a.focus for a in focus]),
        "focusBorder": "technical",
        "resources": resources,
        "lastUpdate": updateProperties,
        "lastUpdateClass": updateProperties.className,
        "lastUpdateColor": updateProperties.colorClass,
        "lastUpdateLabel": updateProperties.label,
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Werkzeuge"),
        "backLink": "tool_list",
    }
    context["boxObject"] = tool
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "tools_over/details_right_column.html"
    return render(request, "pages/details_page.html", context)


def AppView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk=id)
    applicationAreas = tool.applicationArea.all()
    usages = tool.usage.all()  # .split(", ")
    targetGroups = tool.targetGroup.all()
    lifeCyclePhases = tool.lifeCyclePhase.all()  # .split(", ")
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

    lastUpdate, continuousUpdates = setLanguageForLastUpdate(request)

    # changing labels and icon
    updateProperties = lastUpdate
    if tool.lastUpdate_de == "laufend":  # continuous
        updateProperties = continuousUpdates

    context = {
        "tool": tool,
        "applicationAreas": ", ".join(
            [a.applicationArea for a in applicationAreas]
        ),
        "usages": ", ".join([a.usage for a in usages]),
        "targetGroups": ", ".join([a.targetGroup for a in targetGroups]),
        "lifeCyclePhases": ", ".join(
            [a.lifeCyclePhase for a in lifeCyclePhases]
        ),
        "userInterfaces": ", ".join([a.userInterface for a in userInterfaces]),
        "accessibilities": ", ".join(
            [a.accessibility for a in accessibilities]
        ),
        "specificApplications": [
            str(a.referenceNumber_id) for a in specificApplications
        ],  # specificApplications, #
        "scales": ", ".join([a.scale for a in scales]),
        "technicalStandardsNorms": ", ".join(
            [a.technicalStandardsNorms for a in technicalStandardsNorms]
        ),
        "technicalStandardsProtocols": ", ".join(
            [a.technicalStandardsProtocols for a in technicalStandardsProtocols]
        ),
        "classifications": ", ".join(
            [a.classification for a in classifications]
        ),
        "focus": ", ".join([a.focus for a in focus]),
        "focusBorder": "technical",
        "resources": resources,
        "lastUpdate": updateProperties,
        "lastUpdateClass": updateProperties.className,
        "lastUpdateColor": updateProperties.colorClass,
        "lastUpdateLabel": updateProperties.label,
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Anwendungen"),
        "backLink": "app_list",
    }

    context["boxObject"] = tool
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "tools_over/details_right_column.html"
    return render(request, "pages/details_page.html", context)


def toolComparison(request):
    ids = request.GET.getlist("id")

    # Retrieve tools based on the ids
    tools = []
    for id in ids:
        tool = get_object_or_404(Tools, pk=id)
        tools.append(tool)

    context = {"tools": tools}

    return render(request, "tools_over/tool-comparison.html", context)
