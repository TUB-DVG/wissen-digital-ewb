"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
from project_listing.models import Subproject
from TechnicalStandards.models import Norm, Protocol
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator
from datetime import date

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
        focusStrList = toolObj.focus.all().values_list("focus", flat=True)
    else:
        # for other Objects, than Tools set the default-value "Technisch"
        # this needs to be adapted later
        focusStrList = ["Technisch"]
    
    pathStr = "assets/images/"
    if len(focusStrList) == 1:
        focusStr = focusStrList[0]
        if focusStr == "Technisch":
            pathStr += "symbol_technical_focus.svg"
        elif focusStr == "Betrieblich":
            pathStr += "symbol_operational_focus.svg"
        elif focusStr == "Rechtlich":
            pathStr += "symbol_legal_focus.svg"
        elif focusStr == "Ökologisch":
            pathStr += "symbol_ecological_focus.svg"
        else:
            pass
    elif len(focusStrList) == 2:
        if "Betrieblich" in focusStrList and "Technisch" in focusStrList:
            pathStr += "symbol_technical_operational_focus.svg"
        elif "Betrieblich" in focusStrList and "Ökologisch" in focusStrList:
            pathStr += "symbol_operational_ecological_focus.svg"
        elif "Betrieblich" in focusStrList and "Rechtlich" in focusStrList:
            pathStr += "symbol_operational_legal_focus.svg"
        elif "Technisch" in focusStrList and "Ökologisch" in focusStrList:
            pathStr += "symbol_technical_ecological_focus.svg"
        elif "Technisch" in focusStrList and "Rechtlich" in focusStrList:
            pathStr += "symbol_technical_legal_focus.svg"
        elif "Ökologisch" in focusStrList and "Rechtlich" in focusStrList:
            pathStr += "symbol_ecological_legal_focus.svg"
        else:
            pass
    elif len(focusStrList) == 3:
        if ("Betrieblich" in focusStrList 
            and "Technisch" in focusStrList 
            and "Ökologisch" in focusStrList):
            pathStr += "symbol_technical_operational_ecological_focus.svg"
        elif ("Betrieblich" in focusStrList 
            and "Ökologisch" in focusStrList
            and "Rechtlich" in focusStrList):
            pathStr += "symbol_operational_ecological_legal_focus.svg"
        elif ("Technisch" in focusStrList
            and "Ökologisch" in focusStrList
            and "Rechtlich" in focusStrList):
            pathStr += "symbol_technical_ecological_legal_focus.svg"
        elif ("Technisch" in focusStrList
            and "Rechtlich" in focusStrList
            and "Betrieblich" in focusStrList):
            pathStr += "symbol_technical_operational_legal_focus.svg"
        else:
            pass
    elif len(focusStrList) == 4:
        pathStr += "symbol_technical_operational_ecological_legal_focus.svg"
    return pathStr

def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, "StartSearch/StartSearch.html")


def resultSearch(request):
    """View function of the result page of the central search function."""
    # search value reading
    if request.method == "GET":
        searchInput = request.GET.get("searchValue", None)
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
    filteredTools = Tools.objects.values("id",
                                         "name",
                                         "shortDescription",
                                         "lastUpdate",
                                         ).filter(criterionToolsOne |
                                                  criterionToolsTwo)
    # filtered projects
    criterionProjectsOne = Q(
        enargusData__collaborativeProject__icontains=searchInput)
    criterionProejctsTwo = Q(
        enargusData__shortDescriptionDe__icontains=searchInput)
    filteredProjects = Subproject.objects.values("referenceNumber_id",
                                                  "enargusData__collaborativeProject",
                                                  "enargusData__shortDescriptionDe",
                                                  "enargusData__topics",
                                                  "enargusData__startDate",
                                                  "referenceNumber_id"
                                                  ).filter(
                                                      criterionProjectsOne |
                                                      criterionProejctsTwo)
    # filtered norms
    criterionNormsOne = Q(name__icontains=searchInput)
    criterionNormsTwo = Q(shortDescription__icontains=searchInput)
    filteredNorms = Norm.objects.values("id",
                                        "name",
                                        "shortDescription"
                                        ).filter(
                                            criterionNormsOne |
                                            criterionNormsTwo
                                        )

    # filtered protocols
    criterionProtocolsOne = Q(name__icontains=searchInput)
    # because there is no short Description until now
    # > use buildingAutomationLayer
    criterionProtocolsTwo = Q(buildingAutomationLayer__icontains=searchInput)
    filteredProtocols = Protocol.objects.values("id",
                                                "name",
                                                "buildingAutomationLayer",
                                                ).filter(
                                                    criterionProtocolsOne |
                                                    criterionProtocolsTwo
                                                    )

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

        # make a time stamp list, including also virtual dates
        # replancning unspecific time values like "laufend" or
        # no given date
        toolDate = tool.pop("lastUpdate")
        toolVirtDate = toolDate
        if toolDate == "laufend":
            toolVirtDate = date.fromisoformat("2049-09-09")
        elif toolDate == "unbekannt":
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
        project["name"] = projecName + " [..." + referenceNumberLastCharacters + "]"
        project["description"] = project.pop("enargusData__shortDescriptionDe")
        project["kindOfItem"] = "Forschungsprojekt"
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
        norm["date"] = "noch nicht hinterlegt"
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
        protocol["date"] = "noch nicht hinterlegt"
        protocol["virtDate"] = date.fromisoformat("2049-09-09")
        protocol["pathToFocusImage"] = findPicturesForFocus(protocol)

    # concat the prepared querySets to one QuerySet
    filteredData = list(chain(filteredTools, filteredProjects,
                              filteredNorms, filteredProtocols))
    # sort data list by name/kindOfItem and so on
    if sortBy and direction:
        if direction == "desc":
            # descending
            filteredData = sorted(filteredData, key=lambda obj: obj[sortBy],
                                  reverse=True)
        elif direction == "asc":
            # ascending
            filteredData = sorted(filteredData, key=lambda obj: obj[sortBy])
    else:
        # virtual date with descending order
        filteredData = sorted(filteredData, key=lambda obj: obj["virtDate"],
                              reverse=True)

    # setup paginator for the table
    filterDataPaginator = Paginator(filteredData, 12)
    pageNumber = request.GET.get("page", None)
    dataPerPage = filterDataPaginator.get_page(
        pageNumber
    )

    context = {
        "searchInput": searchInput,
        "data": dataPerPage,
        "sortBy": sortBy,
        "direction": direction,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
