"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
from project_listing.models import Teilprojekt
from django.db.models import Q


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

    # debuging section, delete when not needed anymore
    print(searchInput)
    print(filteredTools)
    print(filteredProjects)
    print("Anzahl der gefilterten Projekte: %s" % filteredProjects.count())

    context = {
        "searchValue": searchInput,
        "tools": filteredTools,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
