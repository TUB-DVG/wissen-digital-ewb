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

    explanationText = "<ol type='1'><p>"
    explanationText += _(
        "Auf dieser Seite präsentieren wir eine detaillierte Analyse verschiedener Anwendungsfälle im Kontext des Smart Readiness Indicator. Das Ziel ist es die unterschiedlichen Effekte der Digitalisierung aufzudecken und die Interaktion verschiedener Anforderungen aufzuzeigen. Dabei gehen wir auf verschiedene Fragestellungen ein:"
    )
    explanationText += "</p>"
    explanationText += "<li>"
    explanationText += _("Was verstehen wir unter einem Anwendungsfall?")
    explanationText += "</li>"
    explanationText += "<li>"
    explanationText += _("Welche Anwendungsfälle werden diskutiert?")
    explanationText += "</li>"
    explanationText += "<li>"
    explanationText += _("Was ist in dem Graph zu sehen?")
    explanationText += "</li>"
    explanationText += "<ol type='a'>"
    explanationText += "<li>"
    explanationText += _("Welche Aggregationen sind zu sehen und warum?")
    explanationText += "</li><li>"
    explanationText += _("Woher kommen die Daten?")
    explanationText += "</li></ol></li></ol><p>"
    explanationText += _(
        "Die digitale Anwendung benötigt zahlreiche Messdaten, die Verhaltensmuster erkennen lassen?"
    )
    explanationText += _(
        "Die Anwendung ermöglicht durch Feedback energetische Einsparungen?"
    )
    explanationText += _(
        "Die Auswirkungen digitaler Anwendungen sind durch ihre Wechselwirkungen komplex und vielschichtig."
    )
    explanationText += _(
        "So werden beispielsweise Ressourcen und Energie für Erstellung und den Betrieb von Messtechnik benötigt, "
    )
    explanationText += _(
        "eine genauere Messung ermöglicht aber auch ein individuelleres Feedback an Nutzende oder ein genaues Erkennen von Fehlern."
    )
    explanationText += _(
        "Hier sollen einige dieser wechselwirkenden Effekte gesammelt und in ihren Auswirkungen begreifbar gemacht werden."
    )
    explanationText += "</p><p>"
    explanationText += _(
        "Als Basis wird das Rahmenwerk des Smart Readiness Indicator genutzt, der zur Bewertung der Intelligenzfähigkeit von Gebäuden nach Vorschriften der EU entwickelt wurde."
    )
    explanationText += _(
        "In diesem Rahmenwerk sind „Services“ definiert, welche hier als Use-Cases betrachtet werden."
    )
    explanationText += _("Dabei werden die folgenden Aspekte betrachtet:")
    explanationText += "</p><ul><li>"
    explanationText += _(
        "Use-Case: Beschreibt den konkreten Service, auf den sich bezogen wird und wodurch die Effekte/Wirkungen hervorgerufen werden."
    )
    explanationText += "</li><li>"
    explanationText += _(
        "Wirkebene: Die Ebenen, auf die sich der Use-Case bzw. die Aktion/Durchführung bezieht."
    )
    explanationText += "</li><li>"
    explanationText += _(
        "Level: Die Abstufungen der Durchführung des Use-Cases."
    )
    explanationText += "</li></ul><table><tr><td>"
    explanationText += _("Smart Readiness Indicator Service")
    explanationText += "</td><td>"
    explanationText += _("Functionality level 0 (as non-smart default)")
    explanationText += "</td><td>"
    explanationText += _("Functionality level 1")
    explanationText += "</td><td>"
    explanationText += _("Functionality level 2")
    explanationText += "</td><td>"
    explanationText += _("Functionality level 3")
    explanationText += "</td><td>"
    explanationText += _("Functionality level 4")
    explanationText += "</td></tr><tr><td>"
    explanationText += _(
        "Reporting information regarding electricity consumption"
    )
    explanationText += "</td><td>"
    explanationText += _("None")
    explanationText += "</td><td>"
    explanationText += _(
        "Reporting on current electricity consumption on building level"
    )
    explanationText += "</td><td>"
    explanationText += _("Real-time feedback or benchmarking on building level")
    explanationText += "</td><td>"
    explanationText += _(
        "Real-time feedback or benchmarking on appliance level"
    )
    explanationText += "</td><td>"
    explanationText += _(
        "Real-time feedback or benchmarking on appliance level with automated personalized recommendation"
    )
    explanationText += "</td></tr></table><ul><li>"
    explanationText += _(
        "Perspektive: Die Bereiche, auf denen sich die Durchführung des Use-Cases auswirkt, beispielsweise ökonomisch, ökologisch, aus der Nutzendenperspektive oder der technischen Sichtweite."
    )
    explanationText += "</li><li>"
    explanationText += _(
        "Effekt: Die mit der Durchführung des Use-Cases einhergehenden Wirkungen bzw. erzielten/intendierten Effekte."
    )
    explanationText += "</li></ul><p>"
    explanationText += _(
        "Eine detaillierte Betrachtung anhand von Zeitreihen findet anhand des Services „Reporting information regarding electricity consumption“ statt."
    )
    explanationText += "<br>"
    explanationText += _(
        "Um diese Effekte detaillierter darzustellen, wurde der IDEAL-Datensatz genutzt. In diesem Datensatz sind Monitoringdaten für 255 Haushalte aus den UK und Schottland enthalten."
    )
    explanationText += _(
        "39 dieser Haushalte sind in einem engmaschigen System gemonitort worden."
    )
    explanationText += _(
        "Für die Darstellung sind die engmaschig gemonitorten Haushalte 62, 105 und 106 genutzt worden."
    )
    explanationText += _(
        "Trotz dieses engmaschigen Monitorings ist ersichtlich, dass nicht immer alle Sensoren funktionieren (Haushalt 106)."
    )
    explanationText += "<br>"
    explanationText += _(
        "Dargestellt sind der durchschnittliche Verbrauch in einem Zeitfenster von fünf Sekunden, 15 Minuten und einer Stunde."
    )
    explanationText += _(
        "Dabei sind sowohl die einzelnen Werte der Haushalte dargestellt als auch die Summe der Lastgänge (three buildings)."
    )
    explanationText += _(
        "Die beispielhafte Darstellung zeigt, wie sich verschiedene Aggregationen (zeitlich und räumlich) auswirken."
    )
    explanationText += _(
        "Mittels hochfrequenter Messungen sind einzelne Effekte sehr gut zu sehen, welche in anderen Aggregationen untergehen."
    )
    explanationText += _(
        "Damit sollen die Nutzenden ein quantitatives und qualitatives Gefühl für die Effekte der Digitalisierung und deren Wechselwirkungen bekommen."
    )
    explanationText += _(
        "So werden beispielsweise Ressourcen und Energie für Erstellung und den Betrieb von Messtechnik benötigt, "
    )
    explanationText += _(
        "eine genauere Messung ermöglicht aber auch ein individuelleres Feedback an Nutzende oder ein genaues Erkennen von Fehlern."
    )
    explanationText += "<br>"
    explanationText += _(
        "Das Ziel ist es, die unterschiedlichen Effekte der Digitalisierung aufzudecken und die Interaktion verschiedener Anforderungen aufzuzeigen."
    )
    explanationText += _(
        "Dabei gehen wir auf verschiedene Fragestellungen ein:"
    )
    explanationText += "</p><ul><li>"
    explanationText += _(
        "Wie wirkt sich die Frequenz (5s, 15-minütig, 1-stündig) auf die Sichtbarkeit von Effekten aus?"
    )
    explanationText += "</li><li>"
    explanationText += _(
        "Wie wirken sich einzelne Aggregationen (Anlagen, Gesamtverbrauch, drei Gebäude) auf die Sichtbarkeit von Effekten aus?"
    )
    explanationText += "</li><li>"
    explanationText += _("Was ist in dem Graph zu sehen?")
    explanationText += "</li></ul><p>"
    explanationText += _("Weiterführende Informationen:")
    explanationText += "</p><p>SRI: "
    explanationText += "<a href='https://energy.ec.europa.eu/system/files/2022-06/SRI training slide deck - Version 2 - Jan 2022 - updated.pdf'>"
    explanationText += _("Training Slide Deck")
    explanationText += "</a></p><p>IDEAL Datensatz: <a href='https://pubmed.ncbi.nlm.nih.gov/34050194/'>"
    explanationText += _(
        "Pullinger et al., The IDEAL household energy dataset, electricity, gas, contextual sensor data and survey data for 255 UK homes, ci Data 2021 May 28;8(1):146. doi: 10.1038/s41597-021-00921-y."
    )
    explanationText += "</a></p><br>"

    # explanationTemplate = Template(explanationText)
    # contextObj = Context({})
    # explanationText = explanationTemplate.render(contextObj)

    searched = request.GET.get("searched")

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
            effectevaluation = "+"
        elif evalElement == "Negativ" or evalElement == "Negative":
            effectevaluation = "-"
        elif evalElement == "Neutral":
            effectevaluation = "o"
        else:
            effectevaluation = ""

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
            "filterValues": evalItemsList,
            "filterName": "effectEvaluation_de__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)
    searched = request.GET.get("searched", "")
    if searched != "":
        criterionUsageOne = Q(useCase__icontains=searched)
        criterionUsageTwo = Q(focus__focus__icontains=searched)
        criterionUsageThree = Q(effectName__icontains=searched)
        criterionUsageFour = Q(effectDescription__icontains=searched)
        complexCriterion = (
            criterionUsageOne
            | criterionUsageTwo
            | criterionUsageThree
            | criterionUsageFour
        )

    focus = request.GET.get("focus")
    focusObjectFromGetRequest = getFocusObjectFromGetRequest(focus)
    focusOptions = Focus.objects.all()

    useCase = UseCase.objects.filter(
        complexCriterion
    )  # reads all data from table UseCase

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
    useCase = list(sorted(useCase, key=lambda obj: obj.item_code))

    for useCaseItem in useCase:
        _setUseCaseImage(useCaseItem)

    useCasePaginator = Paginator(useCase, 12)
    pageNum = request.GET.get("page", None)
    page = useCasePaginator.get_page(pageNum)
    focusName = getFocusNameIndependentOfLanguage(
        focus, focusObjectFromGetRequest
    )
    filteredBy = [None] * 3

    context = {
        # descriptionContainer input:
        "heading": _("Überblick über die Anwendungsfälle"),
        "explanaitionText": explanationText,
        "showMorePresent": True,
        "page": page,
        "focus": focus,
        "focus_options": focusOptions,
        "nameOfTemplate": "use_cases",
        "introductionText": _(
            "Auf dieser Seite präsentieren wir eine detaillierte Analyse verschiedener Anwendungsfälle im Kontext des Smart Readiness Indicator. Das Ziel ist es die unterschiedlichen Effekte der Digitalisierung aufzudecken und die Interaktion verschiedener Anforderungen aufzuzeigen."
        ),
        "pathToExplanationTemplate": "uses_cases/explanation.html",
        "optionList": [
            {
                "placeholder": _("Fokus"),
                "objects": focusOptions,
                "fieldName": "focus",
                "filtered": focusElements,
            },
            {
                "placeholder": _("Level der Wirkebene"),
                "objects": list(
                    set(
                        [
                            element.degreeOfDetail
                            for element in UseCase.objects.all()
                        ]
                    )
                ),
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
        "search": searched,
        "use_case": filteredBy[0],
        "perspective": filteredBy[1],
        "effectevaluation": filteredBy[2],
    }
    if filtering:
        return render(
            request, "use_cases/usecase-listings-results.html", context
        )

    return render(request, "use_cases/usecase-listings.html", context)


def useCaseView(request, id):
    """Shows of the key features one project"""
    useCase = get_object_or_404(UseCase, pk=id)

    _setUseCaseImage(useCase)

    context = {
        "useCase": useCase,
    }

    return render(request, "use_cases/usecase-detail.html", context)


def _setUseCaseImage(useCaseItem):
    """ """
    if "Monat" in useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/constructionAgeClass.svg"
    elif "1 h" in useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/consumptionData.svg"
    elif "Sek." in useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/dataVisulization.svg"
    elif "Gebäude" == useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/Klimatisierungsdaten.svg"
    elif (
        "3 Gebäude" == useCaseItem.degreeOfDetail_de
        or "4 Gebäude" in useCaseItem.degreeOfDetail_de
    ):
        useCaseItem.icon = "/assets/images/Gebäudetyp.svg"
    elif "Anlagen" in useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/Klimatisierungsverhalten.svg"
    elif "Geräte" in useCaseItem.degreeOfDetail_de:
        useCaseItem.icon = "/assets/images/Geräte.svg"
    else:
        useCaseItem.icon = None
