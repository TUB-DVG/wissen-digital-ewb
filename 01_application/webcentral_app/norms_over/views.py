#from django.shortcuts import render

from contextlib import nullcontext
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import TechnicalStandards

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
    technicalStandards = TechnicalStandards.objects.all() # reads all data from table Teilprojekt
    filtered_by = [None]*2 #3
    searched=None

    
    if ((request.GET.get("n") != None)| (request.GET.get("s") != None) |(request.GET.get("searched") != None)): #(request.GET.get("n") != None) |
        name=request.GET.get('n')
        source=request.GET.get('s')
        #link=request.GET.get('l')
        searched=request.GET.get('searched')
        technicalStandards=TechnicalStandards.objects.filter(source__icontains=source,name__icontains=name,shortDescription__icontains=searched) #name__icontains=Name,
        filtered_by = [name,source]
              
    technicalStandards = list(sorted(technicalStandards, key=lambda obj:obj.name))

    technicalStandards_paginator= Paginator (technicalStandards,12)

    page_num= request.GET.get('page',None)
    page=technicalStandards_paginator.get_page(page_num)

    #is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
    

    if is_ajax_request:
        html = render_to_string(
            template_name="norms_over/norm-listings-results.html", 
            context = {
                'page': page,
                'search':searched,
                'name': filtered_by[0],
                'source': filtered_by[1],
                #'link': filtered_by[1]
            }

        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

       
    context = {
        'page': page,
        'search':searched,
        'name': filtered_by[0],
        'source': filtered_by[1],
        #'link': filtered_by[1]
    }

    return render(request, 'norms_over/norm-listings.html', context)
    

   
def norm_view(request, id):
    """
    shows of the key features of one norm
    """
    technicalStandards = get_object_or_404(TechnicalStandards, pk= id)
    # bezeichnung (DIN etc), titel, kurzbeschreibung,quelle, link
    name = technicalStandards.name #.split(", ") ### to check if split is needed
    title = technicalStandards.title
    shortDescription = technicalStandards.shortDescription
    source = technicalStandards.source #.split(", ")
    link = technicalStandards.link
    
    """ # check if last update needed as info for TechnicalStandards # 
    letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    update_properties = letztes_update
    if (technicalStandards.letztes_update == 'laufend'):
        update_properties = laufende_updates
    """
     
    context = {
        'technicalStandards': technicalStandards,
        'name': name,
        'shortDescription': shortDescription, 
        'title': title,
        'source': source,
        'link': link
        #'letztes_update': update_properties,
        #'letztes_update_class': update_properties.class_name,
        #'letztes_update_color': update_properties.color_class,
        #'letztes_update_label': update_properties.label,
    }


    return render(request, 'norms_over/norm-detail.html', context)

def Post_Review(request,id):
    if request.method=="POST":
        User=request.user
        technicalStandards = get_object_or_404(TechnicalStandards, pk= id) ####  tool=tool=...
        #comment=request.POST['comment']
        #score=request.POST['score']
        #rating=Rating.objects.create(rating_from=User,rating_for=tool,score=score,comment=comment)

        return  norm_view(request,id)

        
 
