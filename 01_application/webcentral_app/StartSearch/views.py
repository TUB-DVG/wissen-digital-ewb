"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
from project_listing.models import Teilprojekt
from django.db.models import Q
from itertools import chain


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, "StartSearch/StartSearch.html")


def resultSearch(request):
    """View function of the result page of the central search function."""
    # search value/s from Start page
    searchInput = request.POST.get("searchValue", None)
    # read data from data base
    # filtered tools
    criterionToolsOne = Q(bezeichnung__icontains=searchInput)
    criterionToolsTwo = Q(kurzbeschreibung__icontains=searchInput)
    filteredTools = Tools.objects.values("bezeichnung",
                                         "kurzbeschreibung"
                                         ).filter(criterionToolsOne |
                                                  criterionToolsTwo)
    # filtered projects
    criterionProjectsOne = Q(
        enargus_daten__verbundbezeichnung__icontains=searchInput)
    criterionProejctsTwo = Q(
        enargus_daten__kurzbeschreibung_de__icontains=searchInput)
    filteredProjects = Teilprojekt.objects.values("fkz",
                                                  "enargus_daten__verbundbezeichnung",
                                                  "enargus_daten__kurzbeschreibung_de"
                                                  ).filter(
                                                      criterionProjectsOne |
                                                      criterionProejctsTwo)
    # concatenate the filtered data sets to one data set,
    # which can used as input for the table in html
    # rename fields in queryset list-dicts
    # for filteredTools (bezeichung > name, kurzbeschreibung > description )
    for tool in filteredTools:
        tool["name"] = tool.pop("bezeichnung")
        tool["description"] = tool.pop("kurzbeschreibung")
    # for filteredTools (bezeichung > name, kurzbeschreibung > description )
    for project in filteredProjects:
        project["name"] = project.pop("enargus_daten__verbundbezeichnung")
        project["description"] = project.pop("enargus_daten__kurzbeschreibung_de")
    # concat the prepared querySets to one QuerySet
    filteredData = list(chain(filteredTools, filteredProjects))

    # debuging section, delete when not needed anymore
    print(searchInput)
    print(filteredTools)
    print(filteredProjects)
    print("Anzahl der gefilterten Projekte: %s" % filteredProjects.count())

    context = {
        "searchValue": searchInput,
        "data": filteredData,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
