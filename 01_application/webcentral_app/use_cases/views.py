from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import UseCase
from tools_over.models import Focus
from common.views import (
    getFocusObjectFromGetRequest,
    getFocusNameIndependentOfLanguage,
)


def index(request):
    """Shows the list of all projects including some key features."""
    searched = request.GET.get('searched')

    focus = request.GET.get(_('Fokus'))
    focusObjectFromGetRequest = getFocusObjectFromGetRequest(focus)
    focusOptions = Focus.objects.all()
    # query_filters = Q()

    # if searched:
    #     query_filters |= Q(title__icontains=searched)
    #     query_filters |= Q(abstract__icontains=searched)
    #     query_filters |= Q(authors__icontains=searched)
    #     query_filters |= Q(keywords__icontains=searched)  
    # if focus:
    #     query_filters &= Q(focus=focusObjectFromGetRequest)
    useCase = UseCase.objects.all() # reads all data from table UseCase
    filteredBy = [None]*3
    searched = None
    if ((request.GET.get("u") != None) | (focusObjectFromGetRequest is not None) | 
        (request.GET.get("ev") != None) |(request.GET.get("searched") != None)):
        use_case = request.GET.get('u', '')
        effectevaluation = request.GET.get('ev', '')
        if effectevaluation == ' ':
            effectevaluation = '+'
        searched = request.GET.get('searched')
        useCase = UseCase.objects.filter(
            useCase__icontains=use_case,
            effectEvaluation__icontains=effectevaluation,
            sriLevel__icontains=searched,
            focus=focusObjectFromGetRequest,
        )
        filteredBy = [use_case, focusObjectFromGetRequest, effectevaluation]

    useCase = list(sorted(useCase, key=lambda obj:obj.item_code))
    useCasePaginator = Paginator(useCase,12)
    pageNum = request.GET.get('page',None)
    page = useCasePaginator.get_page(pageNum)
    focusName = getFocusNameIndependentOfLanguage(focus, focusObjectFromGetRequest)

    
    context = {
        'page': page,
        'focus': focus,
        'focus_options': focusOptions,
        "nameOfTemplate": "use_cases",    
        "optionList": [
            {
                "placeholder": _("Fokus"), 
                "objects": focusOptions,
                "fieldName": "focus",
            },
            {
                "placeholder": _("Use Case"), 
                "objects": ["Aggregation"],
                "fieldName": "use",
            },
            {
                "placeholder": _("Auswirkung der Evaluation"), 
                "objects": [_("Positiv"), _("Negativ"), _("Neutral")],
                "fieldName": "evaluation",
            }, 
        ],
        "focusBorder": focusName,
        "urlName": "use_cases_list",
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