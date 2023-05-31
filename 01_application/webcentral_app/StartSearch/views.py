"""View functions for start page and start page search."""
from django.shortcuts import render
from tools_over.models import Tools


def startSearch(request):
    """View function of the start page including central search function."""
    return render(request, 'StartSearch/StartSearch.html')


def resultSearch(request):
    """View function of the result page of the central search function."""
    # read data from data base
    # all tool information
    tools = Tools.objects.all()
    searchInput = request.POST.get("searchValue", None)
    print(searchInput)
    print(tools)

    context = {
        "searchValue": searchInput,
        "tools": tools,
    }
    return render(request, "StartSearch/ResultSearch.html", context)
