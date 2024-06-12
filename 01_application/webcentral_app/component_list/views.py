from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import (
    Category,
    Component,
    ComponentClass,
)


def components(request):
    """Load the Component Modeldata and render the components-template"""

    # if request.method == "POST":
    #     breakpoint()
    listingShowOrCollapse = "collapse"

    # get the values of the multi-level dropdown field:
    firstLevelDropdown = request.GET.get("firstLevel", "")
    secondLevelDropdown = request.GET.get("secondLevel", "")

    # get the values of the input-fields:
    searchInputValue = request.GET.get("searched", "")
    searchInputValues = searchInputValue.split(",")
    searchInputValues = _removeEmtpyStringsFromList(searchInputValues)
    categoryValue = request.GET.get("category-hidden", "")

    # the values in category are a comma separated list:
    categoryValues = categoryValue.split(",")
    categoryValues = _removeEmtpyStringsFromList(categoryValues)
    componentValue = request.GET.get("component-hidden", "")
    componentValues = componentValue.split(",")
    componentValues = _removeEmtpyStringsFromList(componentValues)
    # sortingValue = request.GET.get("sorting", "")
    overviewValue = request.GET.get("overview", "")
    # breakpoint()
    filtering = bool(request.GET.get("filtering", False))

    searchQuery = Q()
    searchQueryInput = Q()
    if len(searchInputValues) > 0:
        for searchInputValue in searchInputValues:
            searchQueryInput = searchQueryInput | Q(
                category__category__icontains=searchInputValue)
            searchQueryInput = searchQueryInput | Q(
                component__componentClass__icontains=searchInputValue)
            searchQueryInput = searchQueryInput | Q(
                description__icontains=searchInputValue)
            searchQueryInput = searchQueryInput | Q(
                furtherInformationNotes__icontains=searchInputValue)
            searchQueryInput = searchQueryInput | Q(
                sources__icontains=searchInputValue)

    searchQueryCategory = Q()
    if len(categoryValues) > 0:
        for category in categoryValues:
            searchQueryCategory = searchQueryCategory | Q(
                category__category__icontains=category)

    searchQueryComponents = Q()
    if len(componentValues) > 0:
        for component in componentValues:
            searchQueryComponents = searchQueryComponents | Q(
                component__componentClass__icontains=component)

        # componentForSelectValue = ComponentClass.objects.filter(
        #     componentClass=componentValues)
        # if len(componentForSelectValue) == 1:
        #     searchQuery = searchQuery | Q(component=componentForSelectValue[0])

    searchQuery = searchQueryInput & searchQueryCategory & searchQueryComponents

    if overviewValue:
        if overviewValue == _("Ausgeklappt"):
            listingShowOrCollapse = "show"

    if firstLevelDropdown and secondLevelDropdown:
        if secondLevelDropdown == "Ascending":
            if firstLevelDropdown == "category":
                firstLevelDropdown = "category__category"
            elif firstLevelDropdown == "component":
                firstLevelDropdown = "component__componentClass"
            componentsObj = Component.objects.filter(searchQuery).order_by(
                firstLevelDropdown)
        else:
            if firstLevelDropdown == "category":
                firstLevelDropdown = "category__category"
            elif firstLevelDropdown == "component":
                firstLevelDropdown = "component__componentClass"
            componentsObj = Component.objects.filter(searchQuery).order_by(
                f"-{firstLevelDropdown}")
    else:
        componentsObj = Component.objects.filter(searchQuery)

    componentsObjList = list(componentsObj)
    componentsPaginator = Paginator(componentsObjList, 10)
    pageNum = request.GET.get("page", None)
    page = componentsPaginator.get_page(pageNum)
    context = {
        "heading":
        _("Aufwände für verwendete Komponenten"),
        "explanaitionText":
        _("In Analogie zur Daten-Wertschöpfungskette (siehe “Aufwände für Datenverarbeitungsprozesse”) können wichtige Komponenten von der Datenerfassung (Sensoren) bis zur Datennutzung (Aktuatoren) gedacht werden. Abbildung 2 zeigt wichtige Komponenten, die zur Realisierung einer effektiven Nutzung von Daten für die Betriebsoptimierung von Gebäuden und Quartieren notwendig sind. Je nachdem welche dieser – oder weitere – Komponenten zusätzlich für die digitale Anwendung verbaut werden mussten, müssen die entsprechenden Umweltlasten mit in die Bilanz einfließen. Dabei sind alle Lebenszyklusphasen mit zu betrachten. Hier finden Sie wichtige Komponenten und deren Umweltlasten."
          ),
        "focusBorder":
        "ecological",
        "focusName":
        "ecological",
        "urlName":
        "components",
        "page":
        page,
        "model":
        "Component",
        "listElementsShowOrCollapse":
        listingShowOrCollapse,
        "elementsFirstColumn": [
            {
                "objectReference": "component",
                "description": "",
            },
            {
                "objectReference": "category",
                "description": "",
            },
            {
                "objectReference": "description",
                "description": "",
            },
            {
                "objectReference": "furtherInformationNotes",
                "description": _("Weitere Informationen"),
            },
            {
                "objectReference": "sources",
                "description": _("Quelle"),
            },
        ],
        "elementsSecondColumn": [
            {
                "objectReference": "energyConsumptionUsePhaseTotal",
                "description": _("Energieverbrauch Nutzung (gesamt; in W)"),
            },
            {
                "objectReference": "globalWarmingPotentialTotal",
                "description": _("Treibhauspotenzial (gesamt; in kg CO2-e)"),
            },
            {
                "objectReference": "componentWeight",
                "description": _("Bauteilgewicht (in kg)"),
            },
            {
                "objectReference": "lifetime",
                "description": _("Lebensdauer (in Jahren)"),
            },
            {
                "objectReference": "energyConsumptionUsePhaseActive",
                "description": _("Energieverbrauch Nutzung (aktiv; in W)"),
            },
            {
                "objectReference":
                "energyConsumptionUsePhasePassive",
                "description":
                _("Energieverbrauch Nutzung (passiv/ Stand-by; in W)"),
            },
            {
                "objectReference": "globalWarmingPotentialProduction",
                "description":
                _("Treibhauspotenzial (Herstellung; in kg CO2-e)"),
            },
            {
                "objectReference": "globalWarmingPotentialUsePhase",
                "description": _("Treibhauspotenzial (Nutzung; in kg CO2-e)"),
            },
            {
                "objectReference": "globalWarmingPotentialEndOfLife",
                "description":
                _("Treibhauspotenzial (Entsorgung; in kg CO2-e)"),
            },
        ],
        "optionList": [
            {
                "placeholder":
                "Kategorie",
                "objects": [
                    categoryItem.category
                    for categoryItem in Category.objects.all()
                ],
                "fieldName":
                "category",
            },
            {
                "placeholder":
                _("Komponente"),
                "objects": [
                    componentItem.componentClass
                    for componentItem in ComponentClass.objects.all()
                ],
                "fieldName":
                "component",
            },
            {
                "placeholder":
                _("Sortierung"),
                "multiDimensional":
                True,
                "objects": [
                    {
                        "shown": _("Komponente"),
                        "name": "component",
                    },
                    {
                        "shown": _("Kategorie"),
                        "name": "category",
                    },
                    {
                        "shown": _("Energieverbrauch Nutzung (gesamt; in W)"),
                        "name": "energyConsumptionUsePhaseTotal",
                    },
                    {
                        "shown": _("Treibhauspotenzial (gesamt; in kg CO2-e)"),
                        "name": "globalWarmingPotentialTotal",
                    },
                    {
                        "shown": _("Bauteilgewicht (in kg)"),
                        "name": "componentWeight",
                    },
                    {
                        "shown": _("Lebensdauer (in Jahren)"),
                        "name": "lifetime",
                    },
                    {
                        "shown": _("Energieverbrauch Nutzung (aktiv; in W)"),
                        "name": "energyConsumptionUsePhaseActive",
                    },
                    {
                        "shown":
                        _("Energieverbrauch Nutzung (passiv/ Stand-by; in W)"),
                        "name":
                        "energyConsumptionUsePhasePassive",
                    },
                    {
                        "shown":
                        _("Treibhauspotenzial (Herstellung; in kg CO2-e)"),
                        "name": "globalWarmingPotentialProduction",
                    },
                    {
                        "shown":
                        _("Treibhauspotenzial (Nutzung; in kg CO2-e)"),
                        "name": "globalWarmingPotentialUsePhase",
                    },
                    {
                        "shown":
                        _("Treibhauspotenzial (Entsorgung; in kg CO2-e)"),
                        "name": "globalWarmingPotentialEndOfLife",
                    },
                ],
                "fieldName":
                "sorting",
            },
        ],
        # "radioButtons": [
        #     {
        #         "description":
        #     }
        # ],
        "image":
        "img/componentList/negativeEnvironmentalImpactsBox1.svg",
        "linkOnRightSiteBool":
        True,
        "linkOnRightSiteName":
        "dataProcessing",
        "linkOnRightSiteDescription":
        _("Zu den Aufwänden für Datenverarbeitungsprozesse"),
        "imageInBackButton":
        "img/componentList/caret-left.svg",
        "backLink":
        "environmentalIntegrityNegativ",
        "backLinkText":
        _("Negative Umweltwirkungen"),
        "filters": {
            "searched": searchInputValues,
            "category": categoryValues,
            "component": componentValues,
            "sorting": "",
            "overview": overviewValue,
        },
        "pathToArrow":
        "assets/images/arrowDownEcological.svg",
        # "assets/images/arrow.svg",
    }
    if filtering:
        # context["page"] = page_to_dict(context["page"])
        return render(request, "partials/listing-row.html", context)
    else:
        return render(request, "component_list/components.html", context)


def dataProcessing(request):
    context = {
        "focusBorder":
        "ecological",
        "focusName":
        "ecological",
        "urlName":
        "dataProcessing",
        "backLinkText":
        _("Negative Umweltwirkungen"),
        "backLink":
        "environmentalIntegrityNegativ",
        "leftColumn":
        "partials/dataProcessingLeftColumn.html",
        "rightColumn":
        "partials/dataProcessingRightColumn.html",
        "linkOnRightSiteBool":
        True,
        "linkOnRightSiteName":
        "components",
        "linkOnRightSiteDescription":
        _("Zu den Aufwänden für verwendete Komponenten"),
        "imageInBackButton":
        "img/componentList/caret-left.svg",
    }
    return render(request, "pages/detailsPage.html", context)


def _removeEmtpyStringsFromList(listOfStrings):
    """Remove empty strings from list of strings"""
    for string in listOfStrings:
        if string == "":
            listOfStrings.remove(string)
    return listOfStrings
