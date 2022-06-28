from contextlib import nullcontext
from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Tools, Rating # maybe I need also the other models

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
    tools = Tools.objects.all() # reads all data from table Teilprojekt
    filtered_by = [None]*3
    searched=None


 
    if ((request.GET.get("1") != None) |(request.GET.get("2") != None)| (request.GET.get("3") != None) |(request.GET.get("searched") != None)):
        Kategorie=request.GET.get('1')
        Lizenz=request.GET.get('2')
        Lebenszyklusphase=request.GET.get('3')
        searched=request.GET.get('searched')
        tools=Tools.objects.filter(kategorie__icontains=Kategorie,lebenszyklusphase__icontains=Lebenszyklusphase,lizenz__icontains=Lizenz,bezeichnung__icontains=searched)
        filtered_by = [Kategorie, Lizenz, Lebenszyklusphase]
              

    tools_paginator= Paginator (tools,12)

    page_num= request.GET.get('page',None)
    page=tools_paginator.get_page(page_num)
       
    context = {
        'page': page,
        'search':searched,
        'kategorie': filtered_by[0],
        'lizenz': filtered_by[1],
        'lebenszyklusphase': filtered_by[2]
    }

    return render(request, 'tools_over/tool-listings.html', context)
    

   
def tool_view(request, id):
    """
    shows of the key features one project
    """
    tool = get_object_or_404(Tools, pk= id)
    kategorien = tool.kategorie.split(", ")
    lebenszyklusphasen = tool.lebenszyklusphase.split(", ")
    laufende_updates = tool.letztes_update
    
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

    context = {
        'tool': tool,
        'kategorien': kategorien,
        'lebenszyklusphasen': lebenszyklusphasen,
        'letztes_update': update_properties,
        'letztes_update_class': update_properties.class_name,
        'letztes_update_color': update_properties.color_class,
        'letztes_update_label': update_properties.label,
        'ratings': ratings,
        'rating_perc_5': "{:,.2f}".format(rating_percent_5),
        'rating_perc_4': "{:,.2f}".format(rating_percent_4),
        'rating_perc_3': "{:,.2f}".format(rating_percent_3),
        'rating_perc_2': "{:,.2f}".format(rating_percent_2),
        'rating_perc_1': "{:,.2f}".format(rating_percent_1),
        'ratings_with_comment': ratings_with_comment,
    }


    return render(request, 'tools_over/tool-detail.html', context)

def Post_Review(request,id):
    if request.method=="POST":
        User=request.user
        tool=tool = get_object_or_404(Tools, pk= id)
        comment=request.POST['comment']
        score=request.POST['score']
        rating=Rating.objects.create(rating_from=User,rating_for=tool,score=score,comment=comment)

        return  tool_view(request,id)

        
 
