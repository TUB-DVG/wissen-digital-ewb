from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.db.models import Q

# from .models import collectedDatasets  # maybe I need also the other models
from .models import Dataset
from common.views import createQ


class UpdateProperties:

    def __init__(self, class_name, label, color_class):
        self.class_name = class_name
        self.label = label
        self.color_class = color_class


def index(request):
    """
    shows the list of all projects including some key features
    """
    datasets = Dataset.objects.all()  # reads all data from table Teilprojekt
    filteredBy = [None] * 3
    searched = None

    filtering = bool(request.GET.get("filtering", False))
    applicationAreaElements = request.GET.get("applicationArea-hidden", "")
    applicationAreaElementsList = applicationAreaElements.split(",")

    categoryElements = request.GET.get("category-hidden", "")
    categoryElementsList = categoryElements.split(",")

    availabilityElements = request.GET.get("availability-hidden", "")
    availabilityElementsList = availabilityElements.split(",")

    listOfFilters = [
        {
            "filterValues": applicationAreaElementsList,
            "filterName": "applicationArea__applicationArea__icontains",
        },
        {
            "filterValues": categoryElementsList,
            "filterName": "classification__classification__icontains",
        },
        {
            "filterValues": availabilityElementsList,
            "filterName": "availability__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)

    searched = request.GET.get("searched", "")
    if searched != "":
        complexCriterion &= Q(name__icontains=searched)

    datasets = Dataset.objects.filter(complexCriterion)
    # filteredBy = [useCaseCategory, categoryDataset, availability]
    datasets = list((datasets))
    # datasets_paginator to datasetsPaginator

    datasetsPaginator = Paginator(datasets, 12)

    pageNum = request.GET.get("page", None)
    page = datasetsPaginator.get_page(pageNum)

    context = {
        "page": page,
        "search": searched,
        # "useCaseCategory":
        # filteredBy[0],
        # "categoryDataset":
        # filteredBy[1],
        # "availability":
        # filteredBy[2],
        "heading": _("Überblick über Datensätze"),
        "introductionText": _(
            """Offene Daten spielen eine entscheidende Rolle für die Energiewende, da sie den Zugang zu Informationen und die
          Zusammenarbeit zwischen verschiedenen Akteuren ermöglichen. Durch die Bereitstellung von offenen Daten tragen
          Unternehmen, Forschende sowie Verwaltung zudem zu Transparenz bei."""
        ),
        "pathToExplanationTemplate": "datasets_over/explanation.html",
        "nameOfTemplate": "datasets",
        "urlName": "dataset_list",
        "focusBorder": "technical",
        "urlDetailsPage": "dataset_view",
        "optionList": [
            {
                "placeholder": _("Anwendungsfall"),
                "objects": [
                    _("Potential Erneuerbare Energie"),
                    _("Standardlastprofile"),
                    _("Energiesystemmodell"),
                    _("Infrastruktur Gas"),
                    _("Wetterdaten"),
                    _("Wärmebedarf"),
                    _("Zeitreihen"),
                    "Benchmark",
                    "UBEM",
                    "BIM",
                    "LCA",
                    _("Sonstiges"),
                    "Other",
                ],
                "fieldName": "applicationArea",
                "filter": filteredBy[0],
            },
            {
                "placeholder": _("Kategorie"),
                "objects": [
                    _("Übertragungsnetzentwicklungspläne"),
                    _("Gebäudebestandsentwicklung"),
                    _("Standardlastprofile für Strom"),
                    _("Digitales Geländemodell"),
                    _("Gebäudegrundrisse"),
                    "3D" + _("Gebäude") + _("Modell"),
                    _("Gebäudetypologie"),
                    _("Zeitreihen") + ("Daten"),
                    _("Gebäudebestand"),
                    _("Infrastruktur"),
                    _("Bedarfsdaten"),
                    _("Wetterdaten"),
                    "BIM" + _("Daten"),
                    _("Statistiken"),
                    _("Landnutzung"),
                    _("Datenbasis"),
                    _("Potential"),
                    _("Löser"),
                    "LCA",
                    _("Andere"),
                ],
                "filter": filteredBy[1],
                "fieldName": "category",
            },
            {
                "placeholder": _("Verfügbarkeit"),
                "objects": [
                    "Open/commercial:remote calculation and published report",
                    "Open Data Commons Open Database License 1.0",
                    "Open Database License 1.0",
                    "Open government data",
                    "Creative-Commons",
                    "Commercial",
                    "Open",
                ],
                "filter": filteredBy[2],
                "fieldName": "availability",
            },
        ],
        "subHeading1": _("Anbieter"),
        "subHeadingAttr1": "provider",
        "subHeading2": _("Abdeckung"),
        "subHeadingAttr2": _("coverage"),
    }
    if filtering:
        return render(request, "partials/listing_results.html", context)
    return render(request, "pages/grid_listing.html", context)


def dataset_view(request, id):
    """
    shows of the key features one project
    """
    dataset = get_object_or_404(Dataset, pk=id)
    nameDataset = dataset.name.split(", ")
    # useCaseCategory = dataset.useCaseCategory.split(", ")
    # categoryDataset = dataset.categoryDataset.split(", ")
    # print(useCaseCategory)
    # print(categoryDataset)

    context = {
        "dataset": dataset,
        # "useCaseCategory": useCaseCategory,
        # "categoryDataset": categoryDataset,
        "name": nameDataset,
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Datensätze"),
        "backLink": "dataset_list",
        "focusBorder": "technical",
    }
    context["boxObject"] = dataset
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "datasets_over/details_right_column.html"
    return render(request, "pages/details_page.html", context)
    # return render(request, "datasets_over/dataset-detail.html", context)
