from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.db.models import Q

from Datasets.models import Dataset
from tools_over.models import Tools
from common.models import Classification
from common.views import createQ


# Create your views here.
class UpdateProperties:

    def __init__(self, class_name, label, color_class):
        self.class_name = class_name
        self.label = label
        self.color_class = color_class


def index(request):
    """
    shows the list of all projects including some key features
    """
    classificationWeatherdata = Classification.objects.get(
        classification_de="Wetterdaten"
    )
    weatherdata = list(
        Dataset.objects.filter(classification=classificationWeatherdata)
    )
    weatherdata += list(
        Tools.objects.filter(classification=classificationWeatherdata)
    )

    filtered_by = [None] * 2
    searched = None

    filtering = bool(request.GET.get("filtering", False))

    categoryElements = request.GET.get("category-hidden", "")
    categoryElementsList = categoryElements.split(",")

    licenseElements = request.GET.get("license-hidden", "")
    licenseElementsList = licenseElements.split(",")

    listOfFilters = [
        {
            "filterValues": categoryElementsList,
            "filterName": "classification__classification__icontains",
        },
        {
            "filterValues": licenseElementsList,
            "filterName": "license__license__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)

    searched = request.GET.get("searched", "")
    if searched != "":
        complexCriterion &= Q(name__icontains=searched)
    complexCriterion &= Q(classification=classificationWeatherdata)
    weatherdataDatasets = Dataset.objects.filter(complexCriterion)
    weatherdataTools = Tools.objects.filter(complexCriterion)
    weatherdata = list(weatherdataDatasets)
    weatherdata += list(weatherdataTools)
    weatherdata = list(sorted(weatherdata, key=lambda obj: obj.name))

    weatherdata_paginator = Paginator(weatherdata, 12)

    pageNum = request.GET.get("page", None)
    page = weatherdata_paginator.get_page(pageNum)

    context = {
        "page": page,
        "search": searched,
        # "kategorie":
        # filtered_by[0],
        # "lizenz":
        # filtered_by[1],
        "title": _("Überblick über Wetterdaten-Services"),
        "nameOfTemplate": "weatherdata",
        "urlName": "publicationPage",
        "introductionText": _(
            """Die hier vorgestellten Wetterdaten bzw. Anwendungen zum Umgang mit Wetterdaten
                    sind in einer ersten Recherche durch das Modul Digitalisierung der
                    wissenschaftliche Begleitforschung der Forschungsinitiative Energiewendebauen
                    entstanden. Der Fokus der Recherche lag auf der Region Deutschland."""
        ),
        "pathToExplanationTemplate": "weatherdata_over/explanation.html",
        "optionList": [
            {
                "placeholder": _("Kategorie"),
                "objects": [
                    _("Datensätze"),
                    _("Anwendung"),
                ],
                "fieldName": "category",
                "filter": filtered_by[0],
            },
            {
                "placeholder": _("Lizenz"),
                "objects": [
                    _("Frei nutzbar"),
                    "Open Data",
                    "CC BY 4.0",
                    _("MIT-Lizenz"),
                ],
                "fieldName": "license",
                "filter": filtered_by[1],
            },
        ],
        "focusBorder": "technical",
        "urlDetailsPage": "weatherdata_view",
        "subHeading1": _("Anbieter"),
        "subHeadingAttr1": "provider",
        "subHeading2": _("Lizenz"),
        "subHeadingAttr2": _("license__license"),
    }
    if filtering:
        return render(
            request,
            "partials/listing_results.html",
            context,
        )
    return render(request, "pages/grid_listing.html", context)


def weatherdata_view(request, id):
    """
    shows of the key features one project
    """

    category_icons = {
        #        'window': 'bi bi-window',
        "Anwendung": "bi bi-terminal fa-lg",
        "Datensätze": "fas fa-database",
        "default": "fas fa-bars",
        "focusBorder": "technical",
    }

    try:
        weatherdata = Dataset.objects.get(pk=id)
    except:
        weatherdata = get_object_or_404(Tools, pk=id)

    letztes_update = UpdateProperties(
        "bi bi-patch-exclamation-fill", "letztes Update", "text-danger"
    )
    laufende_updates = UpdateProperties(
        "fas fa-sync", "Updates", "text-success"
    )

    # changing labels and icon
    # update_properties = letztes_update
    # if weatherdata.lastUpdate == "laufend":
    #     update_properties = laufende_updates
    #
    # category_icon = category_icons["default"]
    # if weatherdata.classification in category_icons:
    #     category_icon = category_icons[weatherdata.category]
    #
    context = {
        # "weatherdata": weatherdata,
        # "letztes_update": update_properties,
        # "letztes_update_class": update_properties.class_name,
        # "letztes_update_color": update_properties.color_class,
        # "letztes_update_label": update_properties.label,
        # "category_icon": category_icon,
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Wetterdaten"),
        "backLink": "weatherdata_list",
        "focusBorder": "technical",
    }
    context["boxObject"] = weatherdata
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "weatherdata_over/details_right_column.html"
    return render(request, "pages/details_page.html", context)


def wetterdienst(request):
    return render(request, "weatherdata_over/wetterdienst(example).html")


def _checkDjangoDict(request, key):
    if key in request.GET:
        return request.GET[key]
    return None
