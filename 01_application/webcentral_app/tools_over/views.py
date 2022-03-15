#from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import  Tools # maybe I need also the other models#

from django.contrib.auth.decorators import login_required
from django.db.models import Avg


# Create your views here.


@login_required(login_url='login')
def Tools_view(request):
    """
    shows the list of all projects including some key features
    """
    tools = Tools.objects.all() # reads all data from table Teilprojekt
 
    
    tools_paginator= Paginator (tools,12)

    page_num= request.GET.get('page',None)
    page=tools_paginator.get_page(page_num)



    if (request.method=='GET' and ((request.GET.get("1") != None) |(request.GET.get("2") != None)| (request.GET.get("3") != None)) ):
        
        Category=request.GET.get('1')
        Lizenz=request.GET.get('2')
        Lebenszyklusphase=request.GET.get('3')
        results=Tools.objects.filter(kategorie__contains=Category,lebenszyklusphase__contains=Lebenszyklusphase,lizenz__contains=Lizenz)
        tools_paginator= Paginator (results,12)
        page_num= request.GET.get('page')
        page=tools_paginator.get_page(page_num)
       
    context = {
        'page': page,
        
    }

    return render(request, 'tools_listing/course-grid-2.html', context)
    

   
