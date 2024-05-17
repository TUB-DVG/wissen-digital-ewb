"""views of pages app."""
from django.shortcuts import render
from django.utils.translation import gettext as _


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
    context = {
        "n":
        range(4),
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Positive Umweltwirkungen"),
        "explanaitionText":
        _("Die folgenden vier Kriterien beschreiben die positiven Umweltwirkungen, die durch die Nutzung des Produkts entstehen."
          ),
    }

    return render(request, "pages/environmentalIntegrityPositiv.html", context)


def benchmarkingChallenges(request):
    """Call render function for benchmaring challenges page."""
    return render(request, "pages/benchmarkingChallenges.html")


def dataSufficiency(request):
    """Call render function for data sufficiency page."""
    return render(request, "pages/dataSufficiency.html")


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
