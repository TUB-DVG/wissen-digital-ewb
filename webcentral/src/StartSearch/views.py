"""View functions for start page and start page search."""

from itertools import chain
from datetime import date

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

from criteria_catalog.models import (
    CriteriaCatalog,
    Tag,
    Topic,
)

from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.contrib.postgres.aggregates import StringAgg
from django.utils.translation import gettext as _

# from django.db.models.functions import StringAgg

from tools_over.models import (
    Tools,
    Classification,
)
from project_listing.models import Subproject
from TechnicalStandards.models import (
    Norm,
    Protocol,
)
from user_integration.models import UserEngagement
from businessModel.models import BusinessModel 
from positive_environmental_impact.models import EnvironmentalImpact 
from component_list.models import Component

def findPicturesForFocus(searchResultObj, tool=False):
    """Return the path to the picture, showing the Focus.

    searchResultObj:    obj
        search-result-object, for which the symbol-path should be found

    Returns:
    str
        String, which specifies the path to the symbol-image.
    tool:   bool
        This flag is a temporary argument, as long as "project", "norm" and "standards"
        have no focus
    """
    if tool:
        toolObj = Tools.objects.filter(id=searchResultObj["id"])[0]
        focusStrList = toolObj.focus.all().values_list("focus_de", flat=True)
    else:
        # for other Objects, than Tools set the default-value "Technisch"
        # this needs to be adapted later
        focusStrList = ["technisch"]
        if searchResultObj["kindOfItem"] == "Kriterienkatalog":
            focusStrList = ["rechtlich"]
        if searchResultObj["kindOfItem"] == "Nutzendenintegration":
            focusStrList = ["betrieblich"]
        if searchResultObj["kindOfItem"] == "Geschäftsmodelle":
            focusStrList = ["betrieblich"]
        if searchResultObj["kindOfItem"] == "Positive Umweltwirkungen":
            focusStrList = ["ökologisch"]
        if searchResultObj["kindOfItem"] == "Negative Umweltwirkungen":
            focusStrList = ["ökologisch"]
        

    pathStr = "assets/images/"
    if len(focusStrList) == 1:
        focusStr = focusStrList[0]
        if focusStr == "technisch":
            pathStr += "symbol_technical_focus.svg"
        elif focusStr == "betrieblich":
            pathStr += "symbol_operational_focus.svg"
        elif focusStr == "rechtlich":
            pathStr += "symbol_legal_focus.svg"
        elif focusStr == "ökologisch":
            pathStr += "symbol_ecological_focus.svg"
        else:
            pass
    elif len(focusStrList) == 2:
        if "betrieblich" in focusStrList and "technisch" in focusStrList:
            pathStr += "symbol_technical_operational_focus.svg"
        elif "betrieblich" in focusStrList and "ökologisch" in focusStrList:
            pathStr += "symbol_operational_ecological_focus.svg"
        elif "betrieblich" in focusStrList and "rechtlich" in focusStrList:
            pathStr += "symbol_operational_legal_focus.svg"
        elif "technisch" in focusStrList and "ökologisch" in focusStrList:
            pathStr += "symbol_technical_ecological_focus.svg"
        elif "technisch" in focusStrList and "rechtlich" in focusStrList:
            pathStr += "symbol_technical_legal_focus.svg"
        elif "ökologisch" in focusStrList and "rechtlich" in focusStrList:
            pathStr += "symbol_ecological_legal_focus.svg"
        else:
            pass
    elif len(focusStrList) == 3:
        if (
            "betrieblich" in focusStrList
            and "technisch" in focusStrList
            and "ökologisch" in focusStrList
        ):
            pathStr += "symbol_technical_operational_ecological_focus.svg"
        elif (
            "betrieblich" in focusStrList
            and "ökologisch" in focusStrList
            and "rechtlich" in focusStrList
        ):
            pathStr += "symbol_operational_ecological_legal_focus.svg"
        elif (
            "technisch" in focusStrList
            and "ökologisch" in focusStrList
            and "rechtlich" in focusStrList
        ):
            pathStr += "symbol_technical_ecological_legal_focus.svg"
        elif (
            "technisch" in focusStrList
            and "rechtlich" in focusStrList
            and "betrieblich" in focusStrList
        ):
            pathStr += "symbol_technical_operational_legal_focus.svg"
        else:
            pass
    elif len(focusStrList) == 4:
        pathStr += "symbol_technical_operational_ecological_legal_focus.svg"
    return pathStr


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, "start_search/start_search.html")


def resultSearch(request):
    """View function of the result page of the central search function."""
    # search value reading
    if request.method == "GET":
        searchInput = request.GET.get("searchValue", None)
        if searchInput is None:
            return render(request, "start_search/start_search.html")
        sortBy = request.GET.get("sortBy", "virtDate")
        direction = request.GET.get("direction", None)
    elif request.method == "POST":
        # search value/s from Start page
        searchInput = request.POST.get("searchValue", None)
        sortBy = None
        direction = None
    # read data from data base
    # filtered tools
    criterionToolsOne = Q(name__icontains=searchInput)
    criterionToolsTwo = Q(shortDescription__icontains=searchInput)

    if request.LANGUAGE_CODE == "de":
        classificationQueryExpression = "classification__classification_de"
    else:
        classificationQueryExpression = "classification__classification_en"

    filteredTools = (
        Tools.objects.annotate(
            classificationAgg=StringAgg(
                classificationQueryExpression, delimiter=", "
            )
        )
        .values(
            "id", "name", "shortDescription", "lastUpdate", "classificationAgg"
        )
        .filter(criterionToolsOne | criterionToolsTwo)
    )
    # filtered projects
    criterionProjectsOne = Q(
        enargusData__collaborativeProject__icontains=searchInput
    )
    criterionProejctsTwo = Q(
        enargusData__shortDescriptionDe__icontains=searchInput
    )

    criterionUserIntegrationOne = Q(category__icontains=searchInput)
    criterionUserIntegrationTwo = Q(
        subCategoryShortDescription__icontains=searchInput
    )
    filteredUserIntegration = UserEngagement.objects.values(
        "id",
        "category",
        "subCategoryShortDescription",
    ).filter(criterionUserIntegrationOne | criterionUserIntegrationTwo)

    criterionPositiveEnvironmentalImpactOne = Q(relevance__icontains=searchInput)
    criterionPositiveEnvironmentalImpactTwo = Q(
        description__icontains=searchInput
    )
    filteredPosEnvImpact = EnvironmentalImpact.objects.values(
        "id",
        "relevance",
        "description",
    ).filter(criterionPositiveEnvironmentalImpactOne | criterionPositiveEnvironmentalImpactTwo)

    criterionBusinessModelOne = Q(
        challenge__icontains=searchInput
    )
    criterionBusinessModelTwo = Q(
        shortDescription__icontains=searchInput
    )
    filteredBusinessModels = BusinessModel.objects.values(
        "id",
        "challenge",
        "shortDescription",
    ).filter(criterionBusinessModelOne | criterionBusinessModelTwo)
    
    criterionComponentListOne = Q(
        category__category__icontains=searchInput
    )
    criterionComponentListTwo = Q(
        componentClass__componentClass__icontains=searchInput
    )
    criterionComponentListThree = Q(
        category__category__icontains=searchInput
    )
    filteredComponents = Component.objects.values(
        "id",
        "category__category",
        "componentClass__componentClass",
        "description",
    ).filter(criterionComponentListOne | criterionComponentListTwo | criterionComponentListThree)

    filteredProjects = Subproject.objects.values(
        "referenceNumber_id",
        "enargusData__collaborativeProject",
        "enargusData__shortDescriptionDe",
        "enargusData__topics",
        "enargusData__startDate",
        "referenceNumber_id",
    ).filter(criterionProjectsOne | criterionProejctsTwo)
    # filtered norms
    criterionNormsOne = Q(name__icontains=searchInput)
    criterionNormsTwo = Q(shortDescription__icontains=searchInput)
    filteredNorms = Norm.objects.values(
        "id", "name", "shortDescription"
    ).filter(criterionNormsOne | criterionNormsTwo)

    # filtered protocols
    criterionProtocolsOne = Q(name__icontains=searchInput)
    # because there is no short Description until now
    # > use buildingAutomationLayer
    criterionProtocolsTwo = Q(buildingAutomationLayer__icontains=searchInput)
    filteredProtocols = Protocol.objects.values(
        "id",
        "name",
        "buildingAutomationLayer",
    ).filter(criterionProtocolsOne | criterionProtocolsTwo)

    criterionCriteriaCatalog = Q(heading__icontains=searchInput) | Q(
        text__icontains=searchInput
    )
    # get topics for tags:
    filteredTopicsOfCriteriaCatalog = Topic.objects.filter(
        criterionCriteriaCatalog
    ).values("id", "heading", "text", "criteriaCatalog")
    # filteredTopicsOfCriteriaCatalog = Topic.objects.values(
    #     "id",
    #     "heading",
    #     "criteriaCatalog",
    # ).filter(criterionCriteriaCatalog)

    # concatenate the filtered data sets to one data set,
    # which can used as input for the table in html
    # rename fields in queryset list-dicts
    # for filteredTools (bezeichung > name, kurzbeschreibung > description )
    # and extend list by needed fields like kindOfItems
    for tool in filteredTools:
        tool["name"] = tool.pop("name")
        if len(tool["name"]) > 40:
            tool["name"] = tool["name"][:40] + " ... "
        tool["description"] = tool.pop("shortDescription")
        # later use input from table tools for kindOfItem
        tool["kindOfItem"] = "digitales Werkzeug"
        # tool["classificationAgg"]

        # make a time stamp list, including also virtual dates
        # replancning unspecific time values like "laufend" or
        # no given date
        toolDate = tool.pop("lastUpdate")
        toolVirtDate = toolDate
        if toolDate == "laufend" or toolDate == "ongoing":
            toolVirtDate = date.fromisoformat("2049-09-09")
        elif toolDate == "unbekannt" or toolDate == "unknown" or toolDate == "":
            toolVirtDate = date.fromisoformat("1949-09-09")
        else:
            toolVirtDate = date.fromisoformat(toolVirtDate)

        tool["date"] = toolDate
        tool["virtDate"] = toolVirtDate
        tool["pathToFocusImage"] = findPicturesForFocus(tool, tool=True)

    # for filteredTools (bezeichung > name, kurzbeschreibung > description )
    for project in filteredProjects:
        projecName = project.pop("enargusData__collaborativeProject")
        if projecName == "nein":
            projecName = project.pop("enargusData__topics")
        if len(projecName) > 40:
            projecName = projecName[:40] + " ... "
        referenceNumber = project.get("referenceNumber_id")
        referenceNumberLastCharacters = referenceNumber[-3:]
        project["name"] = (
            projecName + " [..." + referenceNumberLastCharacters + "]"
        )
        project["description"] = project.pop("enargusData__shortDescriptionDe")
        project["kindOfItem"] = "Forschungsprojekt"
        project["classificationAgg"] = _("Forschungsprojekt")
        projectDates = project.pop("enargusData__startDate")
        project["virtDate"] = projectDates
        project["date"] = projectDates.strftime("%d.%m.%Y")
        project["pathToFocusImage"] = findPicturesForFocus(project)

    # for filteredNorms (including also virtual dates, because no information
    # about last Update is include to the database)
    for norm in filteredNorms:
        normName = norm.pop("name")
        if len(normName) > 40:
            normName = normName[:40] + " ... "
        norm["name"] = normName
        norm["kindOfItem"] = "Norm"
        norm["date"] = _("noch nicht hinterlegt")
        norm["virtDate"] = date.fromisoformat("2049-09-09")
        norm["pathToFocusImage"] = findPicturesForFocus(norm)
    # for filteredProtocols (including also virtual dates, because
    # no information about last Update is include to the database)
    for protocol in filteredProtocols:
        protocolName = protocol.pop("name")
        if len(protocolName) > 40:
            protocolName = protocolName[:40] + " ... "
        protocol["name"] = protocolName
        protocol["kindOfItem"] = "Protokoll"
        protocol["classificationAgg"] = _("Protokoll")
        protocol["date"] = _("noch nicht hinterlegt")
        protocol["virtDate"] = date.fromisoformat("2049-09-09")
        protocol["pathToFocusImage"] = findPicturesForFocus(protocol)

    for criteriaCatalog in filteredTopicsOfCriteriaCatalog:
        headingName = criteriaCatalog["heading"]
        if len(headingName) > 40:
            headingName = headingName[:40] + " ... "
        criteriaCatalog["name"] = headingName
        criteriaCatalog["kindOfItem"] = "Kriterienkatalog"
        criteriaCatalog["classificationAgg"] = _("Kriterienkatalog")
        criteriaCatalog["date"] = _("noch nicht hinterlegt")
        criteriaCatalog["virtDate"] = date.fromisoformat("2049-09-09")
        criteriaCatalog["pathToFocusImage"] = findPicturesForFocus(
            criteriaCatalog
        )
        criteriaCatalog["criteriaCatalogPath"] = ""
        criteriaCatalogName = CriteriaCatalog.objects.filter(
            id=criteriaCatalog["criteriaCatalog"]
        )[0].name
        criteriaCatalog["criteriaCatalogPath"] = criteriaCatalog[
            "criteriaCatalog"
        ]

    for userIntegration in filteredUserIntegration:
        userIntegration["name"] = userIntegration["category"]
        userIntegration["kindOfItem"] = "Nutzendenintegration"
        userIntegration["classificationAgg"] = _("Nutzendenintegration")
        userIntegration["date"] = _("2024-07-01")
        userIntegration["virtDate"] = date.fromisoformat("2049-09-09")
        userIntegration["pathToFocusImage"] = findPicturesForFocus(
            userIntegration
        )
    
    for businessModel in filteredBusinessModels:
        businessModel["name"] = businessModel["challenge"]
        businessModel["kindOfItem"] = "Geschäftsmodelle"
        businessModel["classificationAgg"] = _("Geschäftsmodelle")
        businessModel["date"] = _("2024-07-01")
        businessModel["virtDate"] = date.fromisoformat("2049-09-09")
        businessModel["pathToFocusImage"] = findPicturesForFocus(
            businessModel
        )
    for posEnvImpact in filteredPosEnvImpact:
        posEnvImpact["name"] = posEnvImpact["relevance"]
        posEnvImpact["kindOfItem"] = "Positive Umweltwirkungen"
        posEnvImpact["classificationAgg"] = _("Positive Umweltwirkungen")
        posEnvImpact["date"] = _("2024-07-01")
        posEnvImpact["virtDate"] = date.fromisoformat("2049-09-09")
        posEnvImpact["pathToFocusImage"] = findPicturesForFocus(
            posEnvImpact
        )   
    for component in filteredComponents:
        component["name"] = component["category__category"] + " - " + component["componentClass__componentClass"]
        component["kindOfItem"] = "Negative Umweltwirkungen"
        component["classificationAgg"] = _("Negative Umweltwirkungen")
        component["date"] = _("2024-07-01")
        component["virtDate"] = date.fromisoformat("2049-09-09")
        component["pathToFocusImage"] = findPicturesForFocus(
            component
        )   
 
    # concat the prepared querySets to one QuerySet
    filteredData = list(
        chain(
            filteredTools,
            filteredProjects,
            filteredNorms,
            filteredProtocols,
            filteredTopicsOfCriteriaCatalog,
            filteredUserIntegration,
            filteredBusinessModels,
            filteredPosEnvImpact,
            filteredComponents,
        )
    )
    # sort data list by name/kindOfItem and so on
    if sortBy and direction:
        if direction == "desc":
            # descending
            filteredData = sorted(
                filteredData, key=lambda obj: obj[sortBy], reverse=True
            )
        elif direction == "asc":
            # ascending
            filteredData = sorted(filteredData, key=lambda obj: obj[sortBy])
    else:
        # virtual date with descending order
        filteredData = sorted(
            filteredData, key=lambda obj: obj["virtDate"], reverse=True
        )

    # setup paginator for the table
    filterDataPaginator = Paginator(filteredData, 12)
    pageNumber = request.GET.get("page", None)
    dataPerPage = filterDataPaginator.get_page(pageNumber)

    context = {
        "searchInput": searchInput,
        "data": dataPerPage,
        "sortBy": sortBy,
        "direction": direction,
    }
    return render(request, "start_search/result_search.html", context)
