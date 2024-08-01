from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _
from django.template import Template, Context

from .models import UseCase
from tools_over.models import Focus
from common.views import (
    getFocusObjectFromGetRequest,
    getFocusNameIndependentOfLanguage,
    createQ,
)


def index(request):
    """Shows the list of all projects including some key features."""
    
    explanationText = _("""
          <ol type="1">
            <p>
              Auf dieser Seite präsentieren wir eine detaillierte Analyse verschiedener Anwendungsfälle im Kontext des Smart Readiness Indicator. Das Ziel ist es die unterschiedlichen Effekte der Digitalisierung aufzudecken und die Interaktion verschiedener Anforderungen aufzuzeigen. Dabei gehen wir auf verschiedene Fragestellungen ein: 
            </p>
            <li>Was verstehen wir unter einem Anwendungsfall?</li>
            <li>Welche Anwendungsfälle werden diskutiert?</li>
            <li>Was ist in dem Graph zu sehen?
              <ol type="a">
                <li>Welche Aggreationen sind zu sehen und warum?</li>
                <li>Woher kommen die Daten?</li>
              </ol>
            </li>
          </ol>
        <p>
          Die digitale Anwendung benötigt zahlreiche Messdaten, die Verhaltensmuster erkennen lassen? 
          Die Anwendung ermöglicht durch Feedback energetische Einsparungen? 
          Die Auswirkungen digitaler Anwendungen sind durch ihre Wechselwirkungen komplex und vielschichtig.
          So werden bepspielweise Ressourcen und Energie für Erstellung und den Betrieb von Messetechnik benötigt, 
          eine genauere Messung ermöglicht aber auch ein individuelleres Feedback an Nutzende oder ein genaues Erkennen von Fehlern.
          Hier sollen einige dieser wechselwirkenenden Effekte gesammelt und in ihren Auswirkungen begreifbar gemacht werden.
        </p>
        <p>
          Als Basis wird das Rahmenwerk des Smart Readiness Indicator genutzt, der zur Bewertung der Intelligenzfähigkeit von Gebäuden
          nach Vorschriften der EU entwickelt wurde. In diesem Rahmenwerk sind “Services” definiert, welche hier als Use-Cases betrachtet werden.
          Dabei werden die folgenden Aspekte betrachtet:
        </p>
        <ul>
          <li>Use-Case: Beschreibt den konkreten Service auf den sich bezogen wird und wordurch die Effekte/Wirkungen hervorgerufen werden.</li>
          <li>Wirkebene: Die Ebenen, auf die sich der Use-Case bzw. Die Aktion/Durchführung bezieht.</li>
          <li>Level: Die Abstufungen der Durchführung des Use-Casess.</li>
          <table >
           
            <tr>
              <td>Smart Readiness Indicator Service</td>
              <td>Functionality level 0 (as non-smart default)</td>
              <td>Functionality level 1</td>
              <td>Functionality level 2</td>
              <td>Functionality level 3</td>
              <td>Functionality level 4</td>
            </tr>
            <tr>
              <td>Reporting information regarding electricity consumption</td>
              <td>None</td>
              <td>Reporting on current electricity consumption on building level</td>
              <td>Real-time feedback or benchmarking on building level</td>
              <td>Real-time feedback or benchmarking on appliance level</td>
              <td>Real-time feedback or benchmarking on appliance level with automated personalized recommendation</td>
            </tr>
          </table>

          <li>Perspektive: Die Bereiche auf denen sich die Durchführung des Use-Cases auswirkt, beispielsweise Ökonomisch, Ökologisch, aus der Nutzendenperspektive oder der technischen Sichweite.</li>

             <li>Effekt: Die mit der Durchführung des Use-Cases einhergehenden Wirkungen bzw. Erzielten/intendierten Effekte.</li>
        </ul>
        <p>
          Eine detaillierte Betrachtung anhand von Zeitreihen findet anhand des Services „Reporting information regarding electricity consumption“ statt.
          <br>
          Um diese Effekte detaillierter darzustellen wurde der IDEAL-Datensatz genutzt. In diesem Datensatz sind Montoringdaten für 255 Haushalte aus den UK und Schottland enthalten.
          39 dieser Haushalte sind in einem engmaschigen System gemonitort worden. 
          Für die Darstellung sind die engmaschig gemonitorten Haushalte 62, 105 und 106 genutzt worden. Trotz dieses engmaschigen Monitorings ist ersichtlich, das nicht immer alle Sensoren funktionieren (Haushalt 106).
          <br>
          Dargestellt sind der Durschnittliche Verbrauch in einem Zeitfenster von fünf Sekunden, 15 Minuten und einer Stunde. Dabei sind sowohl die einzelnen Werte der Haushalte dargestellt und auch die Summe der Lastgänge (three buildings).
          Die beispielhafte Darstellung zeigt, wie sich verschiedene Aggregationen (zeitlich und räumlich) auswirken. Mittels hochfrquenter Messungen sind einzelne Effekte sehr gut zu sehen, welche in anderen Aggregationen unterhgehen. Damit sollen die Nutzenden 
          ein quantaitives und qualitatives Gefühl für die eFfekte der Digitalisierung und deren Wechselwirkungen bekommen. So werden beispielsweise Ressourcen und Energie für Erstellung und den Betrieb von Messtechnik benötigt, 
          eine genauere Messung ermöglicht aber auch ein individuelleres Feedback an Nutzende oder ein genaues Erkennen von Fehlern.
          <br>
          Das Ziel ist es die unterschiedlichen Effekte der Digitalisierung aufzudecken und die Interaktion verschiedener Anforderungen aufzuzeigen. Dabei gehen wir auf verschiedene Fragestellungen ein:
      </p>
      
      <ul>
          <li>Wie wirkt sich die Frequenz (5s, 15 minütig, 1-stündig) auf die Sichtbarkeit von Effekten aus?</li>
          <li>Wie wirken sich einzelne Aggregationen (Anlagen, Gesamtverbrauch, Drei Gebäude) auf die Sichtbarkeit von Effekten aus?</li>
          <li>Was ist in dem Graph zu sehen?</li>
      </ul> 
          Weiterführende Informationen:
        </p>
        <p>
          SRI:
          <a href="https://energy.ec.europa.eu/system/files/2022-06/SRI training slide deck - Version 2 - Jan 2022 - updated.pdf">Training SlTraining Slide Deckide Deck</a>
        </p>
        <p>
          IDEAL Datensatz:
          <a href="https://pubmed.ncbi.nlm.nih.gov/34050194/">
              Pullinger et al., The IDEAL household energy dataset, electricity, gas, contextual sensor data and survey data for 255 UK homes, ci Data 2021 May 28;8(1):146. doi: 10.1038/s41597-021-00921-y.</a>
        </p>
        <br>
    """).replace("\n", "")
    explanationTemplate = Template(explanationText)
    contextObj = Context({})
    explanationText = explanationTemplate.render(contextObj)

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
            "filterNameDe": "focus__focus_de__icontains",
            "filterNameEn": "focus__focus_en__icontains",
        },
        {
            "filterValues": useElementsList,
            "filterName": "degreeOfDetail_de__icontains",
        },
        {
            "filterValues":  evalItemsList,
            "filterName": "effectEvaluation_de__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionUsageOne = Q(useCase__icontains=searched)
        criterionUsageTwo = Q(focus__focus__icontains=searched)
        criterionUsageThree = Q(
            effectName__icontains=searched)
        criterionUsageFour = Q(effectDescription__icontains=searched)
        complexCriterion &= (criterionUsageOne
                             | criterionUsageTwo
                             | criterionUsageThree
                             | criterionUsageFour)
 
    focus = request.GET.get('focus')
    focusObjectFromGetRequest = getFocusObjectFromGetRequest(focus)
    focusOptions = Focus.objects.all()  
    
    useCase = UseCase.objects.filter(complexCriterion) # reads all data from table UseCase
    # breakpoint()
    # filteredBy = [None]*3
    # searched = None
    # if ((request.GET.get("use") != None) | (focusObjectFromGetRequest is not None) | 
    #     (request.GET.get("evaluation") != None) |(request.GET.get("searched") != None)):
    #     use_case = request.GET.get("use", '')
    #     effectevaluation = request.GET.get("evaluation", '')
    #     if effectevaluation == "Positiv" or effectevaluation == "Positive":
    #         effectevaluation = '+'
    #     elif effectevaluation == "Negativ" or effectevaluation == "Negative":
    #         effectevaluation = '-'
    #     elif effectevaluation =degreeOfDetail_en__icontainsdegreeOfDetail_en__icontains= "Neutral":
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
    filteredBy = [None]*3
    
    context = {
        # descriptionContainer input:
        "heading": _("Überblick über die Anwendungsfälle"),
        "explanaitionText": explanationText,
        "showMorePresent": True,
        "charNumberToShowCollapsed": 323,
        'page': page,
        'focus': focus,
        'focus_options': focusOptions,
        "nameOfTemplate": "use_cases",    
        "optionList": [
            {
                "placeholder": _("Fokus"), 
                "objects": focusOptions,
                "fieldName": "focus",
                "filtered": focusElements,
            },
            {
                "placeholder": _("Level der Wirkebene"), 
                "objects": list(set([element.degreeOfDetail for element in UseCase.objects.all()])),
                "fieldName": "use",
                "filtered": useElements,
            },
            {
                "placeholder": _("Auswirkung der Evaluation"), 
                "objects": [_("Positiv"), _("Negativ"), _("Neutral")],
                "fieldName": "evaluation",
                "filtered": evaluationElements,
            }, 
        ],
        "focusBorder": "global",
        "urlName": "use_cases_list",
        'search':searched,
        'use_case': filteredBy[0],
        'perspective': filteredBy[1],
        'effectevaluation': filteredBy[2]
    }
    if filtering:
        return render(request, "use_cases/usecase-listings-results.html",
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

