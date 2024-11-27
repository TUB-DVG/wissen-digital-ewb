from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _

from common.views import createQ
from .models import (
    Norm,
)
from protocols.models import Protocol


class UpdateProperties:

    def __init__(self, className, label, colorClass):
        self.className = className
        self.label = label
        self.colorClass = colorClass


def index(request):
    context = {
        "focusBorder": "technical",
    }
    return render(request, "TechnicalStandards/explanation.html", context)


def norm(request):
    """
    shows the list of all NORMs including some key features
    """
    norms = Norm.objects.all()
    filteredBy = [None] * 2  # 3
    searched = None
    filtering = bool(request.GET.get("filtering", False))

    nameElements = request.GET.get("name-hidden", "")
    nameElementsList = nameElements.split(",")

    sourceElements = request.GET.get("source-hidden", "")
    sourceElementsList = sourceElements.split(",")

    listOfFilters = [
        {
            "filterValues": nameElementsList,
            "filterName": "name__icontains",
        },
        # {
        #     "filterValues": sourceElementsList,
        #     "filterName": "source__icontains",
        # },
    ]
    complexCriterion = createQ(listOfFilters)
    searched = request.GET.get("searched", "")
    if searched != "":
        complexCriterion &= Q(shortDescription__icontains=searched)
    norms = Norm.objects.filter(complexCriterion)  # name__icontains=Name,

    norms = list(sorted(norms, key=lambda obj: obj.name))

    normsPaginator = Paginator(norms, 12)

    pageNum = request.GET.get("page", None)
    page = normsPaginator.get_page(pageNum)

    isAjaxRequest = request.headers.get("x-requested-with") == "XMLHttpRequest"

    context = {
        "page": page,
        "search": searched,
        # "name":
        # filteredBy[0],
        # "source":
        # filteredBy[1],
        "heading": _("Überblick über technische Standards - Normen"),
        "introductionText": _(
            """Auf dieser Seite befinden sich unterschiedlichen technische Normen, die im Herbst 2022 erfasst worden sind. Diese sind durch Recherche in Softwarekatalogen, Normendatenbanken und in Forschungsprojekten der Energiewendebauen Projekte erfasst worden."""
        ),
        "pathToExplanationTemplate": "TechnicalStandards/norm-explanation.html",
        "nameOfTemplate": "norms",
        "focusBorder": "technical",
        "urlName": "TechnicalStandards_norm_list",
        "optionList": [
            {
                "placeholder": _("Bezeichnung"),
                "objects": [
                    "ANSI / ASHRAE Standard 140-2017 - Standard Method of Test for the Evaluation of Building Energy Analysis Computer Programs",
                    "Arbeitsstättenrichtllinie ASR A4.1",
                    "BISKO",
                    "DIN 14095",
                    "DIN 14675",
                    "DIN 18017-3",
                    "DIN 18599",
                    "DIN 1946-6",
                    "DIN 1986-100",
                    "DIN 1988",
                    "DIN 1988-300",
                    "DIN 2000",
                    "DIN 276",
                    "DIN 4108",
                    "DIN 4108 Beiblatt 2",
                    "DIN 4108-2",
                    "DIN 4108-3",
                    "DIN 4108-6",
                    "DIN 4109-1",
                    "DIN 4701-10/12",
                    "DIN 4708",
                    "DIN 4753",
                    "DIN EN 12056-2",
                    "DIN EN 12056-3",
                    "DIN EN 12502 1-5",
                    "DIN EN 1264-1",
                    "DIN EN 12831-1",
                    "DIN EN 12831-Beiblatt 2",
                    "DIN EN 15450",
                    "DIN EN 16798-1",
                    "DIN EN 1717",
                    "DIN EN 442-1",
                    "DIN EN 442-2",
                    "DIN EN ISO 10077-02",
                    "DIN EN ISO 10211",
                    "DIN SPEC 15240",
                    "DIN V 18599-9",
                    "DIN/TS 12831-1:2020-04",
                    "DVGW W 291",
                    "DVGW W 293",
                    "DVGW W 294",
                    "DVGW W551",
                    "DVGW W553",
                    "DVGW-TRGI 2018",
                    "DVGW-VP 670",
                    "EN 1264-1",
                    "EN 1264-2",
                    "EN 13384-1",
                    "EN 13384-2",
                    "EN 13384-3",
                    "EN 806 Teil 1 und 2",
                    "EN ISO 13788",
                    "EN ISO 6946",
                    "GPC",
                    "ISO 14.064",
                    "ISO 50.001",
                    "ISO 50.006",
                    "OENORM H 7500-1",
                    "TrinkwV",
                    "VDI 2078",
                    "VDI 2081",
                    "VDI 3805",
                    "VDI 4650",
                    "VDI 6007 Blatt 1",
                    "VDI 6007 Blatt 2",
                    "VDI 6023",
                    "ÖNORM EN 12831-1",
                    "ÖNORM EN 12831-3",
                ],
                # "filter":
                # filteredBy[0],
                "fieldName": "name",
            },
            # {
            #     "placeholder": _("Quelle"),
            #     "objects": [
            #         "https://ghgprotocol.org/",
            #         "Leitfaden Trinkwassererwärmung - Bundesverband Wärmepumpe",
            #         "ENEKA - Energiekartenkartografie",
            #         "Hottgenroth Software Katalog",
            #     ],
            #     "fieldName": "source",
            #     # "filter":
            #     # filteredBy[1],
            # },
        ],
        "urlDetailsPage": "TechnicalStandards_norm_details",
        "subHeading1": _("Anbieter"),
        "subHeadingAttr1": "provider",
        "subHeading2": _("Lizenz"),
        "subHeadingAttr2": _("license__license"),
    }
    if filtering:
        return render(
            request,
            "partials/listing_results.html",
            context,
        )
    if isAjaxRequest:
        html = render_to_string(
            template_name="TechnicalStandards/norm-listings-results.html",
            context=context,
        )

        dataDict = {"html_from_view": html}
        return JsonResponse(data=dataDict, safe=False)

    return render(request, "pages/grid_listing.html", context)


def normDetailView(request, id):
    """
    shows of the key features of one norm
    """
    norms = get_object_or_404(Norm, pk=id)
    # bezeichnung (DIN etc), titel, kurzbeschreibung,quelle, link
    name = norms.name  # .split(", ") ### to check if split is needed
    title = norms.title
    # shortDescription = norms.shortDescription
    # source = norms.source  # .split(", ")
    # link = norms.link
    context = {
        "technicalStandards": norms,
        "name": name,
        # "shortDescription": shortDescription,
        "title": title,
        # "source": source,
        # "link": link,
        "focusBorder": "technical",
        "imageInBackButton": "assets/images/backArrowTechnical.svg",
        "backLinkText": _("Normen"),
        "backLink": "TechnicalStandards_norm_list",
    }
    context["boxObject"] = norms
    context["leftColumn"] = (
        "partials/left_column_details_page_technical_focus.html"
    )
    context["rightColumn"] = "TechnicalStandards/details_right_column.html"
    return render(request, "pages/detailsPage.html", context)


def protocolComparison(request):
    ids = request.GET.getlist("id")  # Retrieve list of ids from GET parameters
    protocols = []
    for id in ids:
        protocol = get_object_or_404(Protocol, pk=id)
        protocols.append(protocol)

    context = {
        "protocols": protocols,
        "focusBorder": "technical",
    }

    return render(
        request, "TechnicalStandards/protocol-comparison.html", context
    )
