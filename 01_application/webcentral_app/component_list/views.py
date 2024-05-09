from django.shortcuts import render

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
                # "filter":
                # filteredBy[0],
                "fieldName":
                "category",
            },
            {
                "placeholder":
                "Komponente",
                "objects": [
                    componentItem.componentClass
                    for componentItem in ComponentClass.objects.all()
                ],
                # "filter":
                # filteredBy[1],
                "fieldName":
                "component",
            },
        ],
    }
    return render(request, "component_list/components.html", context)


def dataProcessing(request):
    return render(request, "component_list/dataProcessing.html")
