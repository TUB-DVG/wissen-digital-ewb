"""Definitions of the views of the tools overview app."""

from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages 
from publications.models import Publication
from django.db.models import Q          # used this to be able to search over many parameters
from tools_over.models import Focus

from common.views import (
    getFocusObjectFromGetRequest,
    getFocusNameIndependentOfLanguage,
)


def index(request):
    focus_queryset = Focus.objects.all()
    publications = Publication.objects.all()
    query_filters = Q()
    filteredBy = [None]*3
    
    searched = request.GET.get('searched')
    focus = request.GET.get('Fokus')
    focusObjectFromGetRequest = getFocusObjectFromGetRequest(focus)
    focusOptions = Focus.objects.all()
    
    if searched:
        query_filters |= Q(title__icontains=searched)
        query_filters |= Q(abstract__icontains=searched)
        query_filters |= Q(authors__icontains=searched)
        query_filters |= Q(keywords__icontains=searched)  
    if focus:
        query_filters &= Q(focus=focusObjectFromGetRequest)
    if query_filters:
        publications = publications.filter(query_filters).distinct()

    publications = list(sorted(publications, key=lambda obj: obj.title))

    paginator = Paginator(publications, 12)

    page_number = request.GET.get('page')

    page = paginator.get_page(page_number)
    
    focusName = getFocusNameIndependentOfLanguage(focus, focusObjectFromGetRequest)

    context = {
        'page': page,
        'search': searched,
        'focus': focus,
        'focus_options': focusOptions,
        "nameOfTemplate": "publication",
        "urlName": "publicationPage",
        "optionList": [
            {
                "placeholder": "Fokus", 
                "objects": focusOptions,
                "fieldName": "focus",
            },
        ],
        "focusBorder": focusName,
    }
    
    return render(request, 'publications/publications-listings.html', context)


def publicationView(request, id):
    """Shows of the key features one project"""
    publication = get_object_or_404(Publication, pk= id)
    title = publication.title,
    type = publication.type,
    keywords = publication.keywords.split(',') if publication.keywords else []
    focus_options = Focus.objects.all()

    firstElementOfPublicationFocus = publication.focus.first().focus  
    context = {
        'publication': publication,
        'title': title,
        'type': type,
        'keywords': keywords,
        'focus_options': focus_options,
        "focusBorder": _translateFocusStr(firstElementOfPublicationFocus),
    }

    return render(request, 'publications/publications-detail.html', context)


def download_pdf(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    try:
        return FileResponse(open(publication.pdf.path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404("PDF not found.")

def _translateFocusStr(focusStr: str) -> str:
    """Return the english translataion for the focus string

    """
    if focusStr == "technisch":
        focusBorder = "technical"
    elif focusStr == "betrieblich":
        focusBorder = "operational"
    elif focusStr == "ökologisch":
        focusBorder = "ecological"
    elif focusStr == "rechtlich":
        focusBorder = "legal"
    else:
        focusBorder = "neutral"
    
    return focusBorder
