"""Definitions of the views of the tools overview app."""
# from contextlib import nullcontext
# from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
# from turtle import up
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# maybe I need also the other models
from tools_over.models import Tools, Rating


class UpdateProperties:
    """It shoud be needed to update the icons for the function tool view."""

    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass


@login_required(login_url='login')
def index(request):
    """Shows the list of all projects including some key features."""
    tools = Tools.objects.all() # reads all data from table Teilprojekt
    filteredBy = [None]*3
    searched=None
 
    if ((request.GET.get("u") != None) |(request.GET.get("l") != None)| 
        (request.GET.get("lcp") != None) |(request.GET.get("searched") != None)):
        usage=request.GET.get('u')
        licence=request.GET.get('l')
        lifeCyclePhase=request.GET.get('lcp')
        searched=request.GET.get('searched')
        tools=Tools.objects.filter(usage__icontains=usage,lifeCyclePhase__icontains=lifeCyclePhase,licence__icontains=licence,name__icontains=searched)
        filteredBy = [usage, licence, lifeCyclePhase]
              
    tools = list(sorted(tools, key=lambda obj:obj.name))
    toolsPaginator= Paginator(tools,12)
    pageNum= request.GET.get('page',None)
    page=toolsPaginator.get_page(pageNum)

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"
    

    if isAjaxRequest:
        html = render_to_string(
            template_name="tools_over/tool-listings-results.html",
            context={
                'page': page,
                'search':searched,
                'usage': filteredBy[0],
                'licence': filteredBy[1],
                'lifeCyclePhase': filteredBy[2]
            }
        )

        dataDict = {"html_from_view": html}

        return JsonResponse(data=dataDict, safe=False)

    context = {
        'page': page,
        'search':searched,
        'usage': filteredBy[0],
        'licence': filteredBy[1],
        'lifeCyclePhase': filteredBy[2]
    }

    return render(request, 'tools_over/tool-listings.html', context)


def toolView(request, id):
    """Shows of the key features one project"""
    tool = get_object_or_404(Tools, pk= id)
    usages = tool.usage.split(", ")
    lifeCyclePhases = tool.lifeCyclePhase.split(", ")
    continuousUpdates = tool.lastUpdate
    
    lastUpdate = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
    continuousUpdates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')

    #changing labels and icon
    updateProperties = lastUpdate
    if (tool.lastUpdate == 'laufend'): # continuous
        updateProperties = continuousUpdates

    ratings = Rating.objects.filter(ratingFor=id)
    numRatings = len(ratings)
    print(numRatings)

    ratingsByScore = [ratings.filter(score=1), ratings.filter(score=2), ratings.filter(score=3),
                      ratings.filter(score=4), ratings.filter(score=5)]
    print(ratingsByScore[4])
    ratingPercent5 = 0 if len(ratingsByScore[4])==0 else len(ratingsByScore[4])/numRatings*100
    ratingPercent4 = 0 if len(ratingsByScore[3])==0 else len(ratingsByScore[3])/numRatings*100
    ratingPercent3 = 0 if len(ratingsByScore[2])==0 else len(ratingsByScore[2])/numRatings*100
    ratingPercent2 = 0 if len(ratingsByScore[1])==0 else len(ratingsByScore[1])/numRatings*100
    ratingPercent1 = 0 if len(ratingsByScore[0])==0 else len(ratingsByScore[0])/numRatings*100

    ratingsWithComment = ratings.exclude(comment__exact = '')

    context = {
        'tool': tool,
        'usages': usages,
        'lifeCyclePhases': lifeCyclePhases,
        'lastUpdate': updateProperties,
        'lastUpdateClass': updateProperties.className,
        'lastUpdateColor': updateProperties.colorClass,
        'lastUpdateLabel': updateProperties.label,
        'ratings': ratings,
        'ratingPercent5': "{:,.2f}".format(ratingPercent5),
        'ratingPercent4': "{:,.2f}".format(ratingPercent4),
        'ratingPercent3': "{:,.2f}".format(ratingPercent3),
        'ratingPercent2': "{:,.2f}".format(ratingPercent2),
        'ratingPercent1': "{:,.2f}".format(ratingPercent1),
        'ratingsWithComment': ratingsWithComment,
    }

    return render(request, 'tools_over/tool-detail.html', context)


def postReview(request, id):
    """Return to tools overwiew after submit review.

    remove?, in next version not used, maybe include at the end of 2023 if
    there is time to implement a user space, without user space no rating
    possible
    """
    if request.method == "POST":
        User = request.user
        tool = get_object_or_404(Tools, pk=id)
        comment = request.POST['comment']
        score = request.POST['score']
        rating = Rating.objects.create(ratingFrom=User, ratingFor=tool,
                                       score=score, comment=comment)

        return toolView(request, id)
