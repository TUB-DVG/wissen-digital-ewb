from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (
    Category,
    Component,
    ComponentClass,
)


# Create your views here.
def components(request):
    """Load the Component Modeldata and render the components-template"""

    listingShowOrCollapse = "collapse"

    # get the values of the multi-level dropdown field:
    firstLevelDropdown = request.GET.get("firstLevel", "")
    secondLevelDropdown = request.GET.get("secondLevel", "")

    # get the values of the input-fields:
    searchInputValue = request.GET.get("searched", "")
    categoryValue = request.GET.get("category", "")
    componentValue = request.GET.get("component", "")
    # sortingValue = request.GET.get("sorting", "")
    overviewValue = request.GET.get("overview", "")

    searchQuery = Q()

    if searchInputValue:
        searchQuery = searchQuery | Q(
            category__category__icontains=searchInputValue)
        searchQuery = searchQuery | Q(
            component__componentClass__icontains=searchInputValue)
        searchQuery = searchQuery | Q(description__icontains=searchInputValue)
        searchQuery = searchQuery | Q(
            furtherInformationNotes__icontains=searchInputValue)
        searchQuery = searchQuery | Q(sources__icontains=searchInputValue)

    if categoryValue:
        categoryForSelectValue = Category.objects.filter(
            category=categoryValue)
        if len(categoryForSelectValue) == 1:
            searchQuery = searchQuery | Q(category=categoryForSelectValue[0])

    if componentValue:
        componentForSelectValue = ComponentClass.objects.filter(
            componentClass=componentValue)
        if len(componentForSelectValue) == 1:
            searchQuery = searchQuery | Q(component=componentForSelectValue[0])

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
                "objectReference": "category",
                "description": "",
            },
            {
                "objectReference": "component",
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
                        "shown": _("Kategorie"),
                        "name": "category",
                    },
                    {
                        "shown": _("Komponente"),
                        "name": "component",
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
            {
                "placeholder": _("Übersicht"),
                "objects": [
                    _("Ausgeklappt"),
                    _("Eingeklappt"),
                ],
                "fieldName": "overview",
            },
        ],
    }
    return render(request, "component_list/components.html", context)


def dataProcessing(request):
    context = {
        "focusBorder": "ecological",
        "focusName": "ecological",
        "urlName": "dataProcessing",
        "backLinkText": _("Negative Umweltwirkungen"),
        "backLink": "environmentalIntegrityNegativ",
        "leftColumn": "component_list/dataProcessingLeftColumn.html",
        "rightColumn": "component_list/dataProcessingRightColumn.html",
    }
    return render(request, "common/detailsPage.html", context)
