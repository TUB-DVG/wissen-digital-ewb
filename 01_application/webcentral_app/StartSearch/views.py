"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
from project_listing.models import Subproject
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, "StartSearch/StartSearch.html")


def resultSearch(request):
    """View function of the result page of the central search function."""
    # search value reading
    if request.method == "GET":
        searchInput = request.GET.get("searchValue", None)
        sortBy = request.GET.get("sortBy", None)
    elif request.method == "POST":
        # search value/s from Start page
        searchInput = request.POST.get("searchValue", None)
        sortBy = None
    # read data from data base
    # filtered tools
    criterionToolsOne = Q(name__icontains=searchInput)
    criterionToolsTwo = Q(shortDescription__icontains=searchInput)
    filteredTools = Tools.objects.values("id",
                                         "name",
                                         "shortDescription"
                                         ).filter(criterionToolsOne |
                                                  criterionToolsTwo)
    # filtered projects
    criterionProjectsOne = Q(
        enargusData__collaborativeProject__icontains=searchInput)
    criterionProejctsTwo = Q(
        enargusData__shortDescriptionDe__icontains=searchInput)
    filteredProjects = Subproject.objects.values("referenceNumber_id",
                                                  "enargusData__collaborativeProject",
                                                  "enargusData__shortDescriptionDe"
                                                  ).filter(
                                                      criterionProjectsOne |
                                                      criterionProejctsTwo)
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
    # for filteredTools (bezeichung > name, kurzbeschreibung > description )
    for project in filteredProjects:
        project["name"] = project.pop("enargusData__collaborativeProject")
        project["description"] = project.pop("enargusData__shortDescriptionDe")
        if len(project["name"]) > 40:
            project["name"] = project["name"][:40] + " ... "
        project["kindOfItem"] = "Forschungsprojekt"
    # concat the prepared querySets to one QuerySet
    filteredData = list(chain(filteredTools, filteredProjects))
    # sort data list by name/kindOfItem and so on
    if sortBy:
        filteredData = sorted(filteredData, key=lambda obj: obj[sortBy])
    else:
        filteredData = sorted(filteredData, key=lambda obj: obj["name"])

    # debuging section, delete when not needed anymore
    print(filteredTools)
    print(filteredProjects)
    print("Anzahl der gefilterten Projekte: %s" % filteredProjects.count())
    print(searchInput)
    print(sortBy)
    # test data, pls delete later
    data = [
         {"name": "Brandley", "kindOfItem": "Kol"},
         {"name": "Stevie", "kindOfItem": "Kola"},
         {"name": "Brandl", "kindOfItem": "Ksdol"},
         {"name": "Brandl", "kindOfItem": "Ksdol"},
         {"name": "434Brandley", "kindOfItem": "asdfKol"},
         {"name": "KKStevie", "kindOfItem": "Kollkjlkja"},
         {"name": "43werrandley", "kindOfItem": "aQWERsdfKol"},
         {"name": "OUStevie", "kindOfItem": "KolkUUUjlkja"},
         {"name": "YYStasevie", "kindOfItem": "jkKola"}
    ]

    # setup paginator for the table
    filterDataPaginator = Paginator(filteredData, 12)
    pageNumber = request.GET.get("page", None)
    dataPerPage = filterDataPaginator.get_page(
        pageNumber
    )

    context = {
        "searchInput": searchInput,
        "data": dataPerPage,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
