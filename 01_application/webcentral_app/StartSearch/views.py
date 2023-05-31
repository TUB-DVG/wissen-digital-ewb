"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools
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
    criterionOne = Q(bezeichnung__icontains=searchInput)
    criterionTwo = Q(kurzbeschreibung__icontains=searchInput)
    filteredTools = Tools.objects.filter(
        criterionOne | criterionTwo)
    # debuging section, delete when not needed anymore
    print(searchInput)
    print(filteredTools)

    context = {
        "searchValue": searchInput,
        "tools": filteredTools,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
