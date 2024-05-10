from django.shortcuts import render
from django.utils.translation import gettext as _

from .models import (
    Category,
    Component,
    ComponentClass,
)


# Create your views here.
def components(request):
    context = {
        "focusBorder":
        "ecological",
        "urlName":
        "components",
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
