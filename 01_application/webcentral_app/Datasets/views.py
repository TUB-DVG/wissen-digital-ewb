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

@login_required(login_url='login')
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
        print(datasets)
        filtered_by = [useCaseCategory, categoryDataset, availability]
              
    datasets = list((datasets))

    datasets_paginator= Paginator (datasets,12)

    page_num= request.GET.get('page',None)
    page=datasets_paginator.get_page(page_num)
    
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
    """
    laufende_updates = dataset.letztes_update
    
    letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    update_properties = letztes_update
    if (tool.letztes_update == 'laufend'):
        update_properties = laufende_updates

    ratings = Rating.objects.filter(rating_for=id)
    num_ratings = len(ratings)
    print(num_ratings)

    ratings_by_score = [ratings.filter(score=1), ratings.filter(score=2), ratings.filter(score=3), ratings.filter(score=4), ratings.filter(score=5)]
    print(ratings_by_score[4])
    rating_percent_5 = 0 if len(ratings_by_score[4])==0 else len(ratings_by_score[4])/num_ratings*100
    rating_percent_4 = 0 if len(ratings_by_score[3])==0 else len(ratings_by_score[3])/num_ratings*100
    rating_percent_3 = 0 if len(ratings_by_score[2])==0 else len(ratings_by_score[2])/num_ratings*100
    rating_percent_2 = 0 if len(ratings_by_score[1])==0 else len(ratings_by_score[1])/num_ratings*100
    rating_percent_1 = 0 if len(ratings_by_score[0])==0 else len(ratings_by_score[0])/num_ratings*100

    ratings_with_comment = ratings.exclude(comment__exact = '')
    """
    context = {
        'dataset': dataset,
        'useCaseCategory': useCaseCategory,
        'categoryDataset': categoryDataset,
        'name':nameDataset,
        #'letztes_update': update_properties,
        #'letztes_update_class': update_properties.class_name,
        #'letztes_update_color': update_properties.color_class,
        #'letztes_update_label': update_properties.label,
        #'ratings': ratings,
        #'rating_perc_5': "{:,.2f}".format(rating_percent_5),
        #'rating_perc_4': "{:,.2f}".format(rating_percent_4),
        #'rating_perc_3': "{:,.2f}".format(rating_percent_3),
        #'rating_perc_2': "{:,.2f}".format(rating_percent_2),
        #'rating_perc_1': "{:,.2f}".format(rating_percent_1),
        #'ratings_with_comment': ratings_with_comment,
    }


    return render(request, 'datasets_over/dataset-detail.html', context)
"""
def Post_Review(request,id):
    if request.method=="POST":
        User=request.user
        tool=tool = get_object_or_404(collectedDatasets, pk= id)
        comment=request.POST['comment']
        score=request.POST['score']
        rating=Rating.objects.create(rating_from=User,rating_for=tool,score=score,comment=comment)

        return  dataset_view(request,id)
"""