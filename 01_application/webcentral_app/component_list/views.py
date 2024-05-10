from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

from .models import (
    Category,
    Component,
    ComponentClass,
)


# Create your views here.
def components(request):
    """Load the Component Modeldata and render the components-template"""
    componentsObj = Component.objects.all()
    componentsObjList = list(componentsObj)
    componentsPaginator = Paginator(componentsObjList, 3)
    pageNum = request.GET.get("page", None)
    page = componentsPaginator.get_page(pageNum)
    context = {
        "focusBorder":
        "ecological",
        "urlName":
        "components",
        "page":
        page,
        "elementsFirstColum": [
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
                "description": _("Weitere Infomrationen"),
            },
            {
                "objectReference": "sources",
                "description": _("Quelle"),
            },
        ],
        "elementsSecondColumn": [
            "energyConsumptionUsePhaseTotal",
            "globalWarmingPotentialTotal",
            "componentWeight",
            "lifetime",
            "energyConsumptionUsePhaseActive",
            "energyConsumptionUsePhasePassive",
            "globalWarmingPotentialProduction",
            "globalWarmingPotentialUsePhase",
            "globalWarmingPotentialEndOfLife",
        ],
        "descriptionSecondColumn": [
            _("Energieverbrauch Nutzung (gesamt; in W):"),
            _("Treibhauspotenzial (gesamt; in kg CO2-e):"),
            _("Bauteilgewicht (in kg):"),
            _("Lebensdauer (in Jahre):"),
            _("Energieverbrauch Nutzung (akitv; in W):"),
            _("Energieverbrauch Nutzung (passiv/ Stand-by; in W):"),
            _("Treibhauspotenzial (Herstellung; in kg CO2-e):"),
            _("Treibhauspotenzial (Nutzung; in kg CO2-e):"),
            _("Treibhauspotenzial (Entsorgung; in kg CO2-e):"),
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
                "placeholder": _("Sortierung"),
                "objects": [
                    _("Aufsteigend"),
                    _("Absteigend"),
                ],
                "fieldName": "sorting",
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
    return render(request, "component_list/dataProcessing.html")
