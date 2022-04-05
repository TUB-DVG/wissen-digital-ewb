from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Weatherdata 

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
    weatherdata = Weatherdata.objects.all() # reads all data from table Teilprojekt       
    filtered_by = [None]*2
    searched=None

    if ((request.GET.get("1") != None) |(request.GET.get("2") != None) |(request.GET.get("searched") != None)):
        Kategorie=request.GET.get('1')
        Lizenz=request.GET.get('2')
        searched=request.GET.get('searched')
        weatherdata=Weatherdata.objects.filter(category__icontains=Kategorie,license__icontains=Lizenz,data_service__icontains=searched)
        filtered_by = [Kategorie, Lizenz]
         

    weatherdata_paginator= Paginator (weatherdata,12)

    page_num= request.GET.get('page',None)
    page=weatherdata_paginator.get_page(page_num)

       
    context = {
        'page': page,
        'search': searched,
        'kategorie': filtered_by[0],
        'lizenz': filtered_by[1],
    }

    return render(request, 'weatherdata_over/data-service-listings.html', context)

def weatherdata_view(request, id):
    
    """
    shows of the key features one project
    """

    category_icons = {
#        'window': 'bi bi-window',
        'Anwendung': 'bi bi-terminal fa-lg',
        'Datensätze': 'fas fa-database',
        'default': 'fas fa-bars'
    }

    weatherdata = get_object_or_404(Weatherdata, pk= id)
    
    letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    update_properties = letztes_update
    if (weatherdata.last_update == 'laufend'):
        update_properties = laufende_updates

    category_icon = category_icons['default']
    if (weatherdata.category in category_icons):
        category_icon = category_icons[weatherdata.category]

    context = {
        'weatherdata': weatherdata,
        'letztes_update': update_properties,
        'letztes_update_class': update_properties.class_name,
        'letztes_update_color': update_properties.color_class,
        'letztes_update_label': update_properties.label,
        'category_icon': category_icon
    }

    return render(request, 'weatherdata_over/weatherdata-detail.html', context)
