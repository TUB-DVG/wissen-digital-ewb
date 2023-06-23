from contextlib import nullcontext
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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
    filtered_by = [None]*3
    searched=None
    if ((request.GET.get("k") != None) |(request.GET.get("l") != None)| (request.GET.get("lzp") != None) |(request.GET.get("searched") != None)):
        useCaseCategory=request.GET.get('k')
        categoryDataset=request.GET.get('l')
        availability=request.GET.get('lzp')
        searched=request.GET.get('searched')
        print('here')
        datasets=collectedDatasets.objects.filter(useCaseCategory__icontains=useCaseCategory,categoryDataset__icontains=categoryDataset,availability__icontains=availability,nameDataset__icontains=searched)
        filtered_by = [useCaseCategory, categoryDataset, availability]
              
    datasets = list((datasets))
    # datasets_paginator to datasetsPaginator 

    datasets_paginator= Paginator (datasets,12)

    page_num= request.GET.get('page',None)
    page=datasets_paginator.get_page(page_num)
    
    # is_ajax_request to isAjaxRequest
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if is_ajax_request:
        html = render_to_string(
            template_name="datasets_over/dataset-listings-results.html", 
            context = {
                'page': page,
                'search':searched,
                'useCaseCategory': filtered_by[0],
                'categoryDataset': filtered_by[1],
                'availability': filtered_by[2]
            }

        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

       
    context = {
            'page': page,
            'search':searched,
            'useCaseCategory': filtered_by[0],
            'categoryDataset': filtered_by[1],
            'availability': filtered_by[2]
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