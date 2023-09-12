"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
from project_listing.models import Subproject
from TechnicalStandards.models import Norm
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator
from datetime import date


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
                                         "lastUpdate"
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
    filteredNorms = Norm.objects.values("name",
                                        "shortDescription"
                                        ).filter(
                                            criterionNormsOne |
                                            criterionNormsTwo
                                        )
    print(filteredNorms)

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
        elif toolDate == "":
            toolVirtDate = date.fromisoformat("1949-09-09")
            toolDate = "unbekannt"
        tool["date"] = toolDate
        tool["virtDate"] = toolVirtDate

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
    # concat the prepared querySets to one QuerySet
    filteredData = list(chain(filteredTools, filteredProjects))
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
