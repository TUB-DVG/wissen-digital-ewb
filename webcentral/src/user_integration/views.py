from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template import Template, Context

from .models import UserEngagement


# Create your views here.
def userEngagementDetails(request, engagementId):
    """Serve the user engagement details page."""
    userEngagementObj = UserEngagement.objects.get(id=engagementId)
    context = _defineContextForView()
    context["boxObject"] = userEngagementObj
    context["idOfSelectedObj"] = engagementId

    return render(request, "pages/detailsPage.html", context)


def userEngagementDetailsTitle(request, engagmentTitle):
    try:
        userEngagementObj = UserEngagement.objects.get(category_de=engagmentTitle)
    except:
        userEngagementObj = UserEngagement.objects.get(category_en=engagmentTitle)

    engagementId = userEngagementObj.id
    context = _defineContextForView()
    context["boxObject"] = userEngagementObj
    context["idOfSelectedObj"] = engagementId
    context["pageTitle"] = userEngagementObj.category
    return render(request, "pages/detailsPage.html", context)


def _defineContextForView():
    """Define the base context, which is modified in the 2 different view functions."""
    return {
        "imageInBackButton": "assets/images/backArrowOperational.svg",
        "focusBorder": "operational",
        "backLinkText": _("Übersicht Methoden Nutzendenintegration"),
        "backLink": "userEngagement",
        "leftColumn": "user_integration/userEngagementDetailsLeftColumn.html",
        "rightColumn":
        "user_integration/userEngagementDetailsRightColumn.html",
        "imageQuickLinks": False,
    }
