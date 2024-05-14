from django.shortcuts import render, get_object_or_404

from tools_over.models import Focus
from component_list.models import Component


def getFocusObjectFromGetRequest(focusStr) -> Focus:
    """Get the focus object from the get request."""
    englishFocus = Focus.objects.filter(focus_en=focusStr)
    germanFocus = Focus.objects.filter(focus_de=focusStr)
    focusElements = englishFocus | germanFocus
    if len(focusElements) > 0:
        return focusElements[0]
    return None


def getFocusNameIndependentOfLanguage(focusStr: str, focusObj: Focus) -> str:
    """Return the focus name, which is used inside the css-classname"""
    if focusStr is None or focusStr == "":
        focusName = "neutral"
    else:
        focusName = focusObj.focus_en
    return focusName


def comparison(request, model):
    """Compare instances of the model."""

    # check if the specified model exists:
    if model == "Component":
        modelObj = Component
    else:
        return render(request, "404.html")

    ids = request.GET.getlist("id")

    # Retrieve tools based on the ids
    objectsToCompare = []
    for id in ids:
        objectToCompare = get_object_or_404(modelObj, pk=id)
        objectsToCompare.append(objectToCompare)

    context = {"objectsToCompare": objectsToCompare}

    return render(request, "tools_over/tool-comparison.html", context)
