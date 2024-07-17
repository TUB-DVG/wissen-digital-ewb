from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import UseCase
from tools_over.models import Focus
from common.views import (
    getFocusObjectFromGetRequest,
    getFocusNameIndependentOfLanguage,
    createQ,
)


def index(request):
    """Shows the list of all projects including some key features."""
    searched = request.GET.get('searched')

    filtering = bool(request.GET.get("filtering", False))

    focusElements = request.GET.get("focus-hidden", "")
    focusElementsList = focusElements.split(",")

    useElements = request.GET.get("use-hidden", "")
    useElementsList = useElements.split(",")

    evaluationElements = request.GET.get("evaluation-hidden", "")
    evaluationElementsList = evaluationElements.split(",")
    evalItemsList = []
    for evalElement in evaluationElementsList:
        if evalElement == "Positiv" or evalElement == "Positive":
            effectevaluation = '+'
        elif evalElement == "Negativ" or evalElement == "Negative":
            effectevaluation = '-'
        elif evalElement == "Neutral":
            effectevaluation = 'o'
        else:
            effectevaluation = ''

        evalItemsList.append(effectevaluation)

    listOfFilters = [
        {
            "filterValues": focusElementsList,
            "filterName": "focus__focus__icontains",
        },
        {
            "filterValues": useElementsList,
            "filterName": "degreeOfDetail__icontains",
        },
        {
            "filterValues":  evalItemsList,
            "filterName": "effectEvaluation__icontains__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionUsageOne = Q(useCase__icontains=searched)
        criterionUsageTwo = Q(focus__focus__icontains=searched)
        criterionUsageThree = Q(
            effectName__icontains=searched)
        criterionToolsFour = Q(effectDescription__icontains=searched)
        complexCriterion |= (criterionToolsOne
                             | criterionToolsTwo
                             | criterionToolsThree
                             | criterionToolsFour)
 
    focus = request.GET.get('focus')
    focusObjectFromGetRequest = getFocusObjectFromGetRequest(focus)
    focusOptions = Focus.objects.all()  
    
    useCase = UseCase.objects.filter(complexCriterion) # reads all data from table UseCase
    # filteredBy = [None]*3
    # searched = None
    # if ((request.GET.get("use") != None) | (focusObjectFromGetRequest is not None) | 
    #     (request.GET.get("evaluation") != None) |(request.GET.get("searched") != None)):
    #     use_case = request.GET.get("use", '')
    #     effectevaluation = request.GET.get("evaluation", '')
    #     # breakpoint()
    #     if effectevaluation == "Positiv" or effectevaluation == "Positive":
    #         effectevaluation = '+'
    #     elif effectevaluation == "Negativ" or effectevaluation == "Negative":
    #         effectevaluation = '-'
    #     elif effectevaluation == "Neutral":
    #         effectevaluation = 'o'
    #     else:
    #         effectevaluation = ''
    #     searched = request.GET.get('searched', "")
    #
    #     # criterionUseCaseOne = Q(levelOfAction__icontains=searched)
    #     # criterionUseCaseTwo = Q(degreeOfDetail__icontains=searched)
    #     # criterionUseCaseThree = Q(effectName__icontains=searched)
    #     criterionUseCaseFour = Q(effectDescription__icontains=searched)
    #     if focusObjectFromGetRequest is not None:
    #         useCase = UseCase.objects.filter(criterionUseCaseFour).filter(
    #             useCase__icontains=use_case,
    #             effectEvaluation__icontains=effectevaluation,
    #             focus=focusObjectFromGetRequest,
    #         )
    #     else:
    #         useCase = UseCase.objects.filter(criterionUseCaseFour).filter(
    #             useCase__icontains=use_case,
    #             effectEvaluation__icontains=effectevaluation,
    #         )            
    #     filteredBy = [use_case, focusObjectFromGetRequest, effectevaluation]
    #
    useCase = list(sorted(useCase, key=lambda obj:obj.item_code))

    for useCaseItem in useCase:
        _setUseCaseImage(useCaseItem)

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
                "placeholder": _("Level der Wirkebene"), 
                "objects": list(set([element.degreeOfDetail for element in UseCase.objects.all()])),
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
    if filtering:
        return render(request, "use_case/usecase-listings-results.html",
                      context)


    return render(request, 'use_cases/usecase-listings.html', context)


def useCaseView(request, id):
    """Shows of the key features one project"""
    useCase = get_object_or_404(UseCase, pk = id)
    
    _setUseCaseImage(useCase)

    context = {
        'useCase': useCase,
         
    }

    return render(request, 'use_cases/usecase-detail.html', context)


def _setUseCaseImage(useCaseItem):
    """

    """
    if "Monat" in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/constructionAgeClass.svg"
    elif "1 h" in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/consumptionData.svg"
    elif "Sek." in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/dataVisulization.svg"
    elif "Gebäude" == useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/Klimatisierungsdaten.svg"
    elif "3 Gebäude" == useCaseItem.degreeOfDetail or "4 Gebäude" in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/Gebäudetyp.svg"
    elif "Anlagen" in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/Klimatisierungsverhalten.svg"
    elif "Geräte" in useCaseItem.degreeOfDetail:
        useCaseItem.icon = "/assets/images/Geräte.svg"
    else:
        useCaseItem.icon = None

