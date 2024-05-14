from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _

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
    elif model == "Tools":
        modelObj = Tools
        attributesToCompare = [
            {
                "dbLocator": "name",
                "isManyToManyField": False,
                "displayedStr": _("Attribut"),
            },
            {
                "dbLocator": "image",
                "isManyToManyField": False,
                "displayedStr": "",
            },
            {
                "dbLocator": "applicationArea",
                "isManyToManyField": True,
                "displayedStr": _("Einsatzbereich"),
            },
            {
                "dbLocator": "usage",
                "isManyToManyField": True,
                "displayedStr": _("Verwendung"),
            },
            {
                "dbLocator": "lifeCyclePhase",
                "isManyToManyField": True,
                "displayedStr": _("Lebenszyklusphase"),
            },
            {
                "dbLocator": "targetGroup",
                "isManyToManyField": True,
                "displayedStr": _("Zielgruppe"),
            },
            {
                "dbLocator": "userInterface",
                "isManyToManyField": True,
                "displayedStr": _("Benutzeroberfläche"),
            },
            {
                "dbLocator": "scale",
                "isManyToManyField": True,
                "displayedStr":
                _("Räumliche Größenordnung der Anwendungsfälle"),
            },
            {
                "dbLocator": "accessibility",
                "isManyToManyField": True,
                "displayedStr": _("Zugänglichkeit"),
            },
            {
                "dbLocator": "programmingLanguages",
                "isManyToManyField": False,
                "displayedStr": _("Programmiersprache (Umsetzung)"),
            },
            {
                "dbLocator": "license",
                "isManyToManyField": False,
                "displayedStr": _("Lizenz"),
            },
            {
                "dbLocator":
                "developmentState",
                "isManyToManyField":
                False,
                "displayedStr":
                _("Entwicklungsstand") + "- 1 : pre-Alpha" + "- 2 : Alpha" +
                "- 3 : Beta" + "- 4 : Release Canidate" + "- 5 : Released",
            },
            {
                "dbLocator": "yearOfRelease",
                "isManyToManyField": False,
                "displayedStr": _("Veröffentlichungsjahr"),
            },
            {
                "dbLocator": "lastUpdate",
                "isManyToManyField": False,
                "displayedStr": _("Letztes Update"),
            },
        ]
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
