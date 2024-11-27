from django.shortcuts import render
from django.utils.translation import gettext as _

from .models import BusinessModel


def businessModelsChallenge(request):
    """Call render function for business models challenge page."""
    businessModelObjs = BusinessModel.objects.all()
    context = {
        "imageInBackButton": "assets/images/backArrowOperational.svg",
        "focusBorder": "operational",
        "backLink": "businessModels",
        "backLinkText": _("Geschäftsmodelle"),
        "heading": _("Geschäftsmodelle – Herausforderungen"),
        "showMorePresent": False,
        "explanaitionText": _(
            "Die digitale Anwendung wurde erfolgreich in einem Prototyp getestet? Dem Einsatz als fertiges Produkt steht nichts mehr im Wege und die digitale Anwendung kann bald großflächig zum Einsatz kommen? Oftmals ist der Weg zu einem funktionierenden Geschäftsmodell lang. Gerade bei digitalen Anwendungen treten entlang der Technologieentwicklungsstufen immer wieder Herausforderungen auf. So auch beim Übergang von der technologischen Entwicklung zur wirtschaftlichen Verwertung. Die mit der Geschäftsmodellentwicklung einhergehenden Herausforderungen, mit der sich Projekte der Forschungsinitiative Energiewendebauen konfrontiert sehen, wurden systematisch aufgearbeitet und werden hier vorgestellt. "
        ),
        "boxes": [
            {
                "pathToTemplate": "businessModel/businessModelBox.html",
                "objectToRender": businessModelObj,
            }
            for businessModelObj in businessModelObjs
        ],
        "imageDe": "assets/images/geschaeftsmodelle_de.svg",
        "imageEn": "assets/images/geschaeftsmodelle_en.svg",
    }
    return render(
        request, "businessModel/businessModelsChallenges.html", context
    )


def businessModelsChallengeDetails(request, challengeId):
    """Call render function for buseinessModel details page."""
    businessModelObj = BusinessModel.objects.get(id=challengeId)
    allBusinessModellObjs = BusinessModel.objects.all()
    context = {
        "pageTitle": _("Geschäftsmodelle") + " - " + businessModelObj.challenge,
        "imageInBackButton": "assets/images/backArrowOperational.svg",
        "boxObject": businessModelObj,
        "focusBorder": "operational",
        "backLinkText": _("Geschäftsmodelle – Herausforderungen"),
        "backLink": "businessModelsChallenge",
        "leftColumn": "businessModel/businessModelsDetailsLeftColumn.html",
        "rightColumn": "businessModel/businessModelsDetailsRightColumn.html",
        "imageQuickLinks": True,
        "idOfSelectedObj": challengeId,
        "allObjectsForQuickLinks": allBusinessModellObjs,
        "showInputsInImageQuickLinkBar": False,
        "quickLinkName": "businessModels/challenges",
    }
    return render(request, "pages/details_page.html", context)
