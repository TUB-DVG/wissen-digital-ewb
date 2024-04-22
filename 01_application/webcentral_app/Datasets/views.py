from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

from .models import collectedDatasets # maybe I need also the other models

class UpdateProperties:
    def __init__(self, class_name, label, color_class):
        self.class_name = class_name
        self.label = label
        self.color_class = color_class

def index(request):
    """
    shows the list of all projects including some key features
    """
    datasets = collectedDatasets.objects.all() # reads all data from table Teilprojekt
    filteredBy = [None]*3
    searched=None
    if ((request.GET.get(_("Anwendungsfall")) != None) |(request.GET.get(_("Kategorie")) != None)| (request.GET.get(_("Verfügbarkeit")) != None) |(request.GET.get("searched") != None)):
        useCaseCategory=request.GET.get(_('Anwendungsfall'), '')
        categoryDataset=request.GET.get(_('Kategorie'), '')
        availability=request.GET.get(_('Verfügbarkeit'), '')
        searched=request.GET.get('searched', '')
        datasets=collectedDatasets.objects.filter(useCaseCategory__icontains=useCaseCategory,
                                                  categoryDataset__icontains=categoryDataset,
                                                  availability__icontains=availability,
                                                  nameDataset__icontains=searched)
        filteredBy = [useCaseCategory, categoryDataset, availability]
              
    datasets = list((datasets))
    # datasets_paginator to datasetsPaginator 

    datasetsPaginator= Paginator (datasets, 12)

    pageNum= request.GET.get('page', None)
    page = datasetsPaginator.get_page(pageNum)
    
       
    context = {
            'page': page,
            'search': searched,
            'useCaseCategory': filteredBy[0],
            'categoryDataset': filteredBy[1],
            'availability': filteredBy[2],
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
                        "3D" +  _("Gebäude") + _("Modell"),
                        _("Gebäudetypologie"),
                        _("Zeitreihen") + ("Daten"),
                        _("Gebäudebestand"),
                        _("Infrastruktur"),
                        _("Bedarfsdaten"),
                        _("Wetterdaten"),
                        "BIM"+ _("Daten"),
                        _("Statistiken"),
                        _("Landnutzung"),
                        _("Datenbasis"),
                        _("Potential"),
                        _("Löser"),
                        "LCA",
                        _("Andere"),
                    ],
                    "filter": filteredBy[1],
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
                },
            ],
    }


    return render(request, 'datasets_over/dataset-listings.html', context)
    

   
def dataset_view(request, id):
    """
    shows of the key features one project
    """
    dataset = get_object_or_404(collectedDatasets, pk= id)
    nameDataset=dataset.nameDataset.split(", ")
    useCaseCategory = dataset.useCaseCategory.split(", ")
    categoryDataset = dataset.categoryDataset.split(", ")
    print(useCaseCategory)
    print(categoryDataset)
    
    context = {
        'dataset': dataset,
        'useCaseCategory': useCaseCategory,
        'categoryDataset': categoryDataset,
        'name':nameDataset,
       
    }


    return render(request, 'datasets_over/dataset-detail.html', context)