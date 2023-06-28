#from django.shortcuts import render

from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from turtle import up
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import TechnicalStandards

class UpdateProperties:
    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass

def index(request):
    """
    shows the list of all projects including some key features
    """
    technicalStandards = TechnicalStandards.objects.all() # reads all data from table Teilprojekt
    filteredBy = [None]*2 #3
    searched=None

    
    if ((request.GET.get("n") != None)| (request.GET.get("s") != None) |(request.GET.get("searched") != None)): #(request.GET.get("n") != None) |
        name=request.GET.get('n')
        source=request.GET.get('s')
        #link=request.GET.get('l')
        searched=request.GET.get('searched')
        technicalStandards=TechnicalStandards.objects.filter(source__icontains=source,name__icontains=name,shortDescription__icontains=searched) #name__icontains=Name,
        filteredBy = [name,source]
              
    technicalStandards = list(sorted(technicalStandards, key=lambda obj:obj.name))

    technicalStandardsPaginator= Paginator (technicalStandards,12)

    pageNum= request.GET.get('page',None)
    page=technicalStandardsPaginator.get_page(pageNum)

    #isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json
    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    

    if isAjaxRequest:
        html = render_to_string(
            template_name="norms_over/norm-listings-results.html", 
            context = {
                'page': page,
                'search':searched,
                'name': filteredBy[0],
                'source': filteredBy[1],
                #'link': filteredBy[1]
            }

        )

        dataDict = {"html_from_view": html}

        return JsonResponse(data=dataDict, safe=False)

       
    context = {
        'page': page,
        'search':searched,
        'name': filteredBy[0],
        'source': filteredBy[1],
        #'link': filteredBy[1]
    }

    return render(request, 'norms_over/norm-listings.html', context)
    

   
def normView(request, id):
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
     
    context = {
        'technicalStandards': technicalStandards,
        'name': name,
        'shortDescription': shortDescription, 
        'title': title,
        'source': source,
        'link': link
    }


    return render(request, 'norms_over/norm-detail.html', context)

def postReview(request,id):
    if request.method=="POST":
        User=request.user
        technicalStandards = get_object_or_404(TechnicalStandards, pk= id) ####  tool=tool=...
        #comment=request.POST['comment']
        #score=request.POST['score']
        #rating=Rating.objects.create(rating_from=User,rating_for=tool,score=score,comment=comment)

        return  normView(request,id)

        
 
