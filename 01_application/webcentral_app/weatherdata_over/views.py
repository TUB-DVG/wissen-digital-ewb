from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Weatherdata 

# Create your views here.

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
  