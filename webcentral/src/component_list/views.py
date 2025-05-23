from django.shortcuts import render
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template import Template, Context
from django.views import View

from .models import (
    Category,
    Component,
    ComponentClass,
)


class ComponentListView(View):
    """ """

    def get(self, request, componentId=None):
        """Render component-objects and open details for specified componentId

        Parameters
        ==========
        componentId : int
            Id of the component, whose details view should be opened.
        """

        listingShowOrCollapse = "collapse"

        # get the values of the multi-level dropdown field:
        firstLevelDropdown = ""
        secondLevelDropdown = ""

        # get the values of the input-fields:
        searchInputValue = request.GET.get("searched", "")
        # searchInputValues = searchInputValue.split(",")
        # searchInputValues = _removeEmtpyStringsFromList(searchInputValues)
        categoryValue = request.GET.get("category-hidden", "")

        # the values in category are a comma separated list:
        categoryValues = categoryValue.split(",")
        categoryValues = _removeEmtpyStringsFromList(categoryValues)
        componentValue = request.GET.get("component-hidden", "")
        componentValues = componentValue.split(",")
        componentValues = _removeEmtpyStringsFromList(componentValues)
        # sortingValue = request.GET.get("sorting", "")
        overviewValue = request.GET.get("overview", "")

        sortingValue = request.GET.get("sorting-hidden", "")

        if sortingValue != "":
            firstLevelDropdown = sortingValue.split("_")[0]
            secondLevelDropdown = sortingValue.split("_")[1]
        filtering = bool(request.GET.get("filtering", False))

        searchQuery = Q()
        searchQueryInput = Q()
        # if len(searchInputValues) > 0:
        # for searchInputValue in searchInputValues:
        searchQueryInput = searchQueryInput | Q(
            category__category__icontains=searchInputValue
        )
        searchQueryInput = searchQueryInput | Q(
            componentClass__componentClass__icontains=searchInputValue
        )
        searchQueryInput = searchQueryInput | Q(
            description__icontains=searchInputValue
        )
        searchQueryInput = searchQueryInput | Q(
            furtherInformationNotes__icontains=searchInputValue
        )
        searchQueryInput = searchQueryInput | Q(
            sources_de__icontains=searchInputValue
        )

        searchQueryCategory = Q()
        if len(categoryValues) > 0:
            for category in categoryValues:
                searchQueryCategory = searchQueryCategory | Q(
                    category__category__icontains=category
                )

        searchQueryComponents = Q()
        if len(componentValues) > 0:
            for component in componentValues:
                searchQueryComponents = searchQueryComponents | Q(
                    componentClass__componentClass__icontains=component
                )

            # componentForSelectValue = ComponentClass.objects.filter(
            #     componentClass=componentValues)
            # if len(componentForSelectValue) == 1:
            #     searchQuery = searchQuery | Q(component=componentForSelectValue[0])

        searchQuery = (
            searchQueryInput & searchQueryCategory & searchQueryComponents
        )

        if overviewValue:
            if overviewValue == _("Ausgeklappt"):
                listingShowOrCollapse = "show"

        if firstLevelDropdown and secondLevelDropdown:
            if (
                secondLevelDropdown == "Ascending"
                or secondLevelDropdown == "A...Z"
            ):
                if firstLevelDropdown == "category":
                    firstLevelDropdown = "category__category"
                elif firstLevelDropdown == "component":
                    firstLevelDropdown = "componentClass__componentClass"
                componentsObj = Component.objects.filter(searchQuery).order_by(
                    firstLevelDropdown
                )
            else:
                if firstLevelDropdown == "category":
                    firstLevelDropdown = "category__category"
                elif firstLevelDropdown == "component":
                    firstLevelDropdown = "componentClass__componentClass"
                componentsObj = Component.objects.filter(searchQuery).order_by(
                    f"-{firstLevelDropdown}"
                )
        else:
            componentsObj = Component.objects.filter(searchQuery)

        componentsObjList = list(componentsObj)
        componentsPaginator = Paginator(componentsObjList, 10)
        pageNum = request.GET.get("page", None)
        page = componentsPaginator.get_page(pageNum)

        if request.LANGUAGE_CODE == "de":
            descriptionImage = "backbone_de.svg"
        else:
            descriptionImage = "backbone_en.svg"

        explanationFirstPart = _(
            "Die Durchführung der Prozessschritte entlang der Daten-Wertschöpfungskette (siehe auch"
        )

        explanationRaw = "{% load i18n %} <a class=\"ecological-font-color\" href=\"{% url 'dataProcessing' %}\">„{% translate 'Aufwände für Datenverarbeitungsprozesse' %}“</a>) "
        explanationSecondPart = (
            _(
                """ist immer mit einem materiellen Einsatz für die Komponenten verbunden. In Analogie zu den Prozessschritten der Daten-Wertschöpfungskette können wichtige Komponenten von der Datenerfassung (Sensoren) bis zur Datennutzung (Aktuatoren) gedacht werden. Abbildung 2 zeigt Komponenten, die zur Realisierung digitaler Anwendungen in Gebäuden und Quartieren häufig zur Anwendung kommen (hier Fokus auf Betriebsoptimierung). Je nachdem, welche dieser – oder weitere – Komponenten zusätzlich für die digitale Anwendung verbaut werden mussten, müssen die entsprechenden Umweltlasten mitbetrachtet werden. Die Umweltlasten umfassen dabei die Emissionen, die bei der Herstellung von der Gewinnung der Rohstoffe bis zur Fertigung der Komponente reichen, über Emissionen durch den Ressourcen- und Energieverbrauch während der Nutzung der Komponente, bis zur Entsorgung und dem Recycling der Materialien. Diese Wirkungen wurden mit der Methode der Ökobilanz erfasst.
            """
            )
            .replace("\n", "<br>")
            .replace("'", "")
        )
        templateObj = Template(explanationRaw)
        explanationText = templateObj.render(Context({}))

        context = {
            "renderDetailsRadio": True,
            "heading": _("Aufwände für verwendete Komponenten"),
            "explanaitionText": explanationFirstPart
            + explanationText
            + explanationSecondPart,
            "focusBorder": "ecological",
            "focusName": "ecological",
            "urlName": "components",
            "page": page,
            "model": "Component",
            "listElementsShowOrCollapse": listingShowOrCollapse,
            "elementsFirstColumn": [
                {
                    "objectReference": "componentClass",
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
                    "objectReference": "furtherInformationNotesRendered",
                    "description": _("Weitere Informationen"),
                },
                {
                    "objectReference": "sources",
                    "description": _("Quelle"),
                },
            ],
            "elementsSecondColumn": [
                {
                    "objectReference": "energyConsumptionUsePhaseTotalRounded",
                    "description": _(
                        "Energieverbrauch Nutzungsphase (gesamt; in kWh/Jahr)"
                    ),
                },
                {
                    "objectReference": "specificGlobalWarmingPotentialRounded",
                    "description": _(
                        "Spezifisches Teibhauspotential Gesamt  (in kg CO2-e/Jahr)"
                    ),
                },
                {
                    "objectReference": "globalWarmingPotentialTotalRounded",
                    "description": _(
                        "Treibhauspotenzial (gesamt; in kg CO2-e)"
                    ),
                },
                {
                    "objectReference": "componentWeightRounded",
                    "description": _("Bauteilgewicht (in kg)"),
                },
                {
                    "objectReference": "lifetime",
                    "description": _("Lebensdauer (in Jahre)"),
                },
                {
                    "objectReference": "energyConsumptionUsePhaseActiveRoundedSup",
                    "description": _("Leistung Nutzungsphase (akitv; in W)"),
                },
                {
                    "objectReference": "energyConsumptionUsePhasePassiveRounded",
                    "description": _(
                        "Leistung Nutzungsphase (passiv/ Stand-by; in W)"
                    ),
                },
                {
                    "objectReference": "globalWarmingPotentialProductionRoundedSub",
                    "description": _(
                        "Treibhauspotenzial (Herstellung; in kg CO2-e)"
                    ),
                },
                {
                    "objectReference": "globalWarmingPotentialUsePhaseRoundedSub",
                    "description": _(
                        "Treibhauspotenzial (Nutzung; in kg CO2-e)"
                    ),
                },
                {
                    "objectReference": "globalWarmingPotentialEndOfLifeRounded",
                    "description": _(
                        "Treibhauspotenzial (Entsorgung; in kg CO2-e)"
                    ),
                },
                {
                    "objectReference": "operationTimeRendered",
                    "description": _("Betriebsdauer (h/Jahr)"),
                },
            ],
            "optionList": [
                {
                    "placeholder": "Kategorie",
                    "filtered": categoryValue,
                    "objects": [
                        categoryItem.category
                        for categoryItem in Category.objects.all()
                    ],
                    "fieldName": "category",
                },
                {
                    "placeholder": _("Komponente"),
                    "objects": [
                        componentItem.componentClass
                        for componentItem in ComponentClass.objects.all()
                    ],
                    "fieldName": "component",
                    "filtered": componentValue,
                },
                {
                    "placeholder": _("Sortierung"),
                    "multiDimensional": True,
                    "objects": [
                        {
                            "shown": _("Komponente"),
                            "name": "component",
                            "type": "alphabetic",
                        },
                        {
                            "shown": _("Kategorie"),
                            "name": "category",
                            "type": "alphabetic",
                        },
                        {
                            "shown": _(
                                "Energieverbrauch Nutzung (gesamt; in W)"
                            ),
                            "name": "energyConsumptionUsePhaseTotal",
                            "type": "numeric",
                        },
                        {
                            "shown": _(
                                "Treibhauspotenzial (gesamt; in kg CO2-e)"
                            ),
                            "name": "globalWarmingPotentialTotal",
                            "type": "numeric",
                        },
                        {
                            "shown": _("Bauteilgewicht (in kg)"),
                            "name": "componentWeight",
                            "type": "numeric",
                        },
                        {
                            "shown": _("Lebensdauer (in Jahren)"),
                            "name": "lifetime",
                            "type": "numeric",
                        },
                    ],
                    "fieldName": "sorting",
                },
            ],
            # "radioButtons": [
            #     {
            #         "description":
            #     }
            # ],
            "image": f"img/componentList/{descriptionImage}",
            "caption": _(
                "Abbildung 2: Wichtige Komponenten für das Beispiel Betriebsoptimierung, die zur Realisierung der Daten-Wertschöpfungskette notwendig sind."
            ),
            "linkOnRightSiteBool": True,
            "linkOnRightSiteName": "dataProcessing",
            "linkOnRightSiteDescription": _(
                "Zu den Aufwänden für Datenverarbeitungsprozesse"
            ),
            "imageInBackButton": "img/componentList/caret-left.svg",
            "backLink": "environmentalIntegrityNegativ",
            "backLinkText": _("Negative Umweltwirkungen"),
            "filters": {
                "searched": searchInputValue,
                "category": categoryValues,
                "component": componentValues,
                "sorting": "",
                "overview": overviewValue,
            },
            "pathToArrow": "assets/images/arrowDownEcological.svg",
            "renderComparisonRadio": True,
            "headerOfImage": _("Die Daten-Wertschöpfungkette"),
            # "assets/images/arrow.svg",
        }
        if componentId is not None:
            componentShowDetails = Component.objects.get(id=componentId)
            context["componentDetails"] = componentShowDetails
            context["componentDetailsId"] = componentShowDetails.id
            for pageNumber in range(1, page.paginator.num_pages + 1):
                for componentObj in page.paginator.page(pageNumber).object_list:
                    if componentObj == componentShowDetails:
                        context["componentDetailsPage"] = pageNumber
                        # set the current page of the paginator to the page
                        # were the search component was found.
                        page = page.paginator.get_page(pageNumber)
                        found = True  # Set flag to True
                        break
                if found:
                    break
        if filtering:
            # context["page"] = page_to_dict(context["page"])
            return render(request, "partials/listing-row.html", context)
        else:
            return render(request, "component_list/components.html", context)


def dataProcessing(request):
    if request.LANGUAGE_CODE == "de":
        descriptionImage = "datenwertschöpfungskette_de.svg"
    else:
        descriptionImage = "datenwertschöpfungskette_en.svg"

    context = {
        "pageTitle": _("Aufwände für Datenverarbeitungsprozesse"),
        "descriptionImage": "img/componentList/" + descriptionImage,
        "focusBorder": "ecological",
        "focusName": "ecological",
        "urlName": "dataProcessing",
        "backLinkText": _("Negative Umweltwirkungen"),
        "backLink": "environmentalIntegrityNegativ",
        "leftColumn": "partials/dataProcessingLeftColumn.html",
        "rightColumn": "partials/dataProcessingRightColumn.html",
        "linkOnRightSiteBool": True,
        "linkOnRightSiteName": "components",
        "linkOnRightSiteDescription": _(
            "Zu den Aufwänden für verwendete Komponenten"
        ),
        "imageInBackButton": "img/componentList/caret-left.svg",
    }
    return render(request, "pages/details_page.html", context)


def _removeEmtpyStringsFromList(listOfStrings):
    """Remove empty strings from list of strings"""
    for string in listOfStrings:
        if string == "":
            listOfStrings.remove(string)
    return listOfStrings


def showImage(request, pathToImage: str):
    """
    show image detail-page with the image, from which the image-path is provided
    """

    context = {
        "imageName": pathToImage,
        "focusBorder": "ecological",
        "backLink": "dataProcessing",
        "imageInBackButton": "img/componentList/caret-left.svg",
        "backLinkText": _("Aufwände für Datenverarbeitungsprozesse"),
    }

    return render(request, "pages/showImage.html", context)
