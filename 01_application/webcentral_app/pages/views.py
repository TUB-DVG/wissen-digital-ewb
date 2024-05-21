"""views of pages app."""
from django.shortcuts import render
from django.utils.translation import gettext as _

from component_list.models import EnvironmentalImpact


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


def environmentalIntegrityBox(request, idOfPage):
    context = {
        "focusBorder": "ecological",
        "backLinkText": _("Positive Umweltwirkungen"),
        "backLink": "environmentalIntegrityPositiv",
        "leftColumn": "pages/dataSufficiencyLeftColumn.html",
        "leftColumnHeading": mappingIdHeading[idOfPage],
        "rightColumn": "pages/dataSufficiencyRightColumn.html",
    }
    return render(request, "common/detailsPage.html", context)


def benchmarkingChallenges(request):
    """Call render function for benchmaring challenges page."""
    return render(request, "pages/benchmarkingChallenges.html")


def dataSufficiency(request):
    """Call render function for data sufficiency page."""
    context = {
        "n":
        range(4),
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Datensuffizienz"),
        "explanaitionText":
        _("Sowohl der Materialverbrauch als auch der Energieaufwand für den Betrieb immer größer werdender Rechenkapazitäten stellt eine Herausforderung dar. Der maßhaltige Umgang mit Daten – die Datensuffizienz – gewinnt daher zunehmend an Relevanz. Die Datensuffizienz schaut dabei auf alle Bereiche der Datenverarbeitung: von der Erhebung, der Weiterverarbeitung, Speicherung bis zur Löschung. Gerade die ökologischen Auswirkungen eines (in-)suffizienten Umgangs mit Daten sind derzeit noch wenig untersucht und bleiben in der Praxis oftmals unbeachtet."
          ),
        "pathToBoxTemplates": [
            "pages/dataSufficiencyBox1.html",
            "pages/dataSufficiencyBox2.html",
            "pages/dataSufficiencyBox3.html",
            "pages/dataSufficiencyBox4.html",
        ],
        "focusBorder":
        "ecological",
    }
    return render(request, "pages/dataSufficiency.html", context)


def dataSufficiencyBox(request, idOfPage):
    """Call render function for data sufficiency box page."""
    mappingIdHeading = {
        1: _("Datenerhebung"),
        2: _("Datenverarbeitung"),
        3: _("Datenmanagement "),
        4: _("Datenspeicherung"),
    }
    context = {
        "focusBorder": "ecological",
        "focusName": "ecological",
        "urlName": "dataProcessing",
        "backLinkText": _("Datensuffizienz"),
        "backLink": "dataSufficiency",
        "leftColumn": "pages/dataSufficiencyLeftColumn.html",
        "leftColumnHeading": mappingIdHeading[idOfPage],
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
