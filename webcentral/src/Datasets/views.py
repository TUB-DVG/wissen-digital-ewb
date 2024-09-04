from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.db.models import Q

from .models import collectedDatasets  # maybe I need also the other models

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
    datasets = collectedDatasets.objects.all()  # reads all data from table Teilprojekt
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
            "filterName": "useCaseCategory__icontains",
        },
        {
            "filterValues": categoryElementsList,
            "filterName": "categoryDataset__icontains",
        },
        {
            "filterValues": availabilityElementsList,
            "filterName": "availability__icontains",
        },
    ]
    complexCriterion = createQ(listOfFilters)

    searched = request.GET.get("searched", "")
    if searched != "":
        complexCriterion &= Q(nameDataset__icontains=searched)

    datasets = collectedDatasets.objects.filter(complexCriterion)
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
        "nameOfTemplate": "datasets",
        "urlName": "dataset_list",
        "focusBorder": "technical",
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
    }
    if filtering:
        return render(request, "datasets_over/dataset-listings-results.html", context)
    return render(request, "datasets_over/dataset-listings.html", context)


def dataset_view(request, id):
    """
    shows of the key features one project
    """
    dataset = get_object_or_404(collectedDatasets, pk=id)
    nameDataset = dataset.nameDataset.split(", ")
    useCaseCategory = dataset.useCaseCategory.split(", ")
    categoryDataset = dataset.categoryDataset.split(", ")
    print(useCaseCategory)
    print(categoryDataset)

    context = {
        "dataset": dataset,
        "useCaseCategory": useCaseCategory,
        "categoryDataset": categoryDataset,
        "name": nameDataset,
    }

    return render(request, "datasets_over/dataset-detail.html", context)
