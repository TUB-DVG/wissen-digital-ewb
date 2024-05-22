"""views of pages app."""
from django.shortcuts import render
from django.utils.translation import gettext as _

from component_list.models import (
    EnvironmentalImpact,
    DataSufficiency,
)


def index(request):
    """Call render function for index page."""
    return render(request, "pages/index.html")


def Datenschutzhinweis(request):
    """Call render function for datenschutzhinweis page."""
    return render(request, "pages/Datenschutzhinweis.html")


def about(request):
    """Call render function for about page."""
    return render(request, "pages/about.html")


def coming(request):
    """Call render function for coming soon page."""
    return render(request, "pages/coming.html")


def businessModelsChallenge(request):
    """Call render function for business models challenge page."""
    return render(request, "pages/businessModelsChallenge.html")


def businessModelsPractice(request):
    """Call render function for business models best practice page."""
    return render(request, "pages/businessModelsPractice.html")


def userIntegrationPractice(request):
    """Call render function for user integration best practice page."""
    return render(request, "pages/userIntegrationPractice.html")


def userIntegrationMethod(request):
    """Call render function for user integration method page."""
    return render(request, "pages/userIntegrationMethod.html")


def environmentalIntegrityNegativ(request):
    """Call render function for negativ environmental integrity page."""
    return render(request, "pages/environmentalIntegrityNegativ.html")


def environmentalIntegrityPositiv(request):
    """Call render function for positiv environmental integrity page."""

    # get number of environmentalImpact-objects and render them as boxes:
    environmentalImpacts = EnvironmentalImpact.objects.all()
    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Positive Umweltwirkungen"),
        "explanaitionText":
        _("Die folgenden vier Kriterien beschreiben die positiven Umweltwirkungen, die durch die Nutzung des Produkts entstehen."
          ),
        "boxes": [{
            "pathToTemplate": "pages/environmentalIntegrityBox.html",
            "objectToRender": environmentalImpact,
        } for environmentalImpact in environmentalImpacts],
        "focusBorder":
        "ecological",
    }

    return render(request, "pages/environmentalIntegrityPositiv.html", context)


def environmentalIntegrityBox(request, idOfEnvironmentalImpactObj):
    """Call render function for environmental integrity box page."""
    environmentalImpactObj = EnvironmentalImpact.objects.get(
        id=idOfEnvironmentalImpactObj)
    context = {
        "boxObject": environmentalImpactObj,
        "focusBorder": "ecological",
        "backLinkText": _("Positive Umweltwirkungen"),
        "backLink": "environmentalIntegrityPositiv",
        "leftColumn": "pages/environmentalIntegrityLeftColumn.html",
        "rightColumn": "pages/environmentalIntegrityRightColumn.html",
    }
    return render(request, "common/detailsPage.html", context)


def benchmarkingChallenges(request):
    """Call render function for benchmaring challenges page."""
    return render(request, "pages/benchmarkingChallenges.html")


def dataSufficiency(request):
    """Call render function for data sufficiency page."""
    dataSufficiencyObjs = DataSufficiency.objects.all()
    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Datensuffizienz"),
        "explanaitionText":
        _("Sowohl der Materialverbrauch als auch der Energieaufwand für den Betrieb immer größer werdender Rechenkapazitäten stellt eine Herausforderung dar. Der maßhaltige Umgang mit Daten – die Datensuffizienz – gewinnt daher zunehmend an Relevanz. Die Datensuffizienz schaut dabei auf alle Bereiche der Datenverarbeitung: von der Erhebung, der Weiterverarbeitung, Speicherung bis zur Löschung. Gerade die ökologischen Auswirkungen eines (in-)suffizienten Umgangs mit Daten sind derzeit noch wenig untersucht und bleiben in der Praxis oftmals unbeachtet."
          ),
        "boxes": [{
            "pathToTemplate": "pages/dataSufficiencyBox.html",
            "objectToRender": dataSufficiencyObj,
        } for dataSufficiencyObj in dataSufficiencyObjs],
        "focusBorder":
        "ecological",
    }
    return render(request, "pages/dataSufficiency.html", context)


def dataSufficiencyBox(request, idOfObject):
    """Call render function for data sufficiency box page."""
    dataSufficiencyObj = DataSufficiency.objects.get(id=idOfObject)
    context = {
        "boxObject": dataSufficiencyObj,
        "focusBorder": "ecological",
        "focusName": "ecological",
        "urlName": "dataProcessing",
        "backLinkText": _("Datensuffizienz"),
        "backLink": "dataSufficiency",
        "leftColumn": "pages/dataSufficiencyLeftColumn.html",
        "rightColumn": "pages/dataSufficiencyRightColumn.html",
    }
    return render(request, "common/detailsPage.html", context)


def dataSecurity(request):
    """Call render function for data security page."""
    return render(request, "pages/dataSecurity.html")


def iconsAndVis(request):
    """Call render function for icons and Visualization page."""
    return render(request, "pages/iconsAndVis.html")


def criteriaCatalog(request):
    """Call render function for criteria catalog page."""
    return render(request, "pages/criteriaCatalog.html")


def impressum(request):
    """Call render function for impressum page."""
    return render(request, "pages/impressum.html")
