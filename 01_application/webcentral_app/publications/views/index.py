from django.shortcuts import render
from publications.models import Publication, CustomLink, CustomFile
from publications.utils import populate
from django.core.paginator import Paginator


def index(request):
    years = []
    searched=None
    publications = Publication.objects.all()
    if (request.GET.get("searched") != None):
        searched=request.GET.get('searched')
        publications=Publication.objects.filter(title__icontains=searched)
    """
    if year:
        publications = publications.filter(year=year, external=False)
    else:
        publications = publications.filter(external=False)
    publications = publications.order_by('-year', '-month', '-id')

    for publication in publications:
        if publication.type.hidden:
            continue
        if not years or (years[-1][0] != publication.year):
            years.append((publication.year, []))
        years[-1][1].append(publication)
    """   
    publications = list(sorted(publications, key=lambda obj:obj.title))
    publicationssPaginator= Paginator(publications,12)
    pageNum= request.GET.get('page',None)
    page=publicationssPaginator.get_page(pageNum)

    populate(publications)

    context = {
        'page': page,
        'search':searched,

    }
    return render(request, 'publications/publications-listings.html', context)
