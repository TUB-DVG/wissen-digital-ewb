from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

# maybe I need also the other models
from .models import UseCase
# Create your views here.

def index(request):
    """Shows the list of all projects including some key features."""
    useCase = UseCase.objects.all() # reads all data from table UseCase
    filteredBy = [None]*3
    searched=None
    if ((request.GET.get("u") != None) |(request.GET.get("p") != None)| 
        (request.GET.get("ev") != None) |(request.GET.get("searched") != None)):
        use_case = request.GET.get('u')
        perspective = request.GET.get('p')
        effectevaluation = request.GET.get('ev')
        if effectevaluation == ' ':
            effectevaluation = '+'
        searched = request.GET.get('searched')
        useCase = UseCase.objects.filter(
            useCase__icontains=use_case,
            perspective__icontains=perspective,
            effectEvaluation__icontains=effectevaluation,
            sriLevel__icontains=searched,
        )
        filteredBy = [use_case, perspective, effectevaluation]

    useCase = list(sorted(useCase, key=lambda obj:obj.item_code))
    useCasePaginator= Paginator(useCase,12)
    pageNum= request.GET.get('page',None)
    page=useCasePaginator.get_page(pageNum)

    
    context = {
        'page': page,
        'search':searched,
        'use_case': filteredBy[0],
        'perspective': filteredBy[1],
        'effectevaluation': filteredBy[2]
    }

    return render(request, 'use_cases/usecase-listings.html', context)


def useCaseView(request, id):
    """Shows of the key features one project"""
    useCase = get_object_or_404(UseCase, pk = id)
    

    context = {
        'useCase': useCase,
         
    }

    return render(request, 'use_cases/usecase-detail.html', context)

def graph(request):

    return render(request, 'use_cases/DarstellungAggreagtionenEnergieverbrauchs.html') 