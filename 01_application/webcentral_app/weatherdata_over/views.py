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

    weatherdata_paginator= Paginator (weatherdata,12)

    page_num= request.GET.get('page',None)
    page=weatherdata_paginator.get_page(page_num)

       
    context = {
        'page': page
        
    }

    return render(request, 'weatherdata_over/data-service-listings.html', context)

def weatherdata_view(request, id):
    """
    shows of the key features one project
    """
    weatherdata = get_object_or_404(Weatherdata, pk= id)
    
    letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    update_properties = letztes_update
    if (weatherdata.last_update == 'laufend'):
        update_properties = laufende_updates


    context = {
        'weatherdata': weatherdata,
        'letztes_update': update_properties,
        'letztes_update_class': update_properties.class_name,
        'letztes_update_color': update_properties.color_class,
        'letztes_update_label': update_properties.label
    }

    return render(request, 'weatherdata_over/weatherdata-detail.html', context)
