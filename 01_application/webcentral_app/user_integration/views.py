from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template import Template, Context

from .models import UserEngagement


# Create your views here.
def userEngagementDetails(request, engagementId):
    """Serve the user engagement details page."""
    userEngagementObj = UserEngagement.objects.get(id=engagementId)
    context = {
        "imageInBackButton": "assets/images/backArrowOperational.svg",
        "focusBorder": "operational",
        "boxObject": userEngagementObj,
        "backLinkText": _("Übersicht Methoden Nutzendenintegration"),
        "backLink": "userEngagement",
        "leftColumn": "user_integration/userEngagementDetailsLeftColumn.html",
        "rightColumn":
        "user_integration/userEngagementDetailsRightColumn.html",
        "imageQuickLinks": False,
        "idOfSelectedObj": engagementId,
        # "allObjectsForQuickLinks":
        # UserEngagement.objects.all(),
        # "showInputsInImageQuickLinkBar":
        # False,
        # "showSelect":
        # False,
        # "tags": [
        #     currentUserEnagementObj.category
        #     for currentUserEnagementObj in UserEngagement.objects.all()
        # ],
        "quickLinkName": "user_integration/userEngagement",
        "javascriptFilePath": "js/user_integration_functions.js",
    }

    return render(request, "pages/detailsPage.html", context)


def userEngagementDetailsTitle(request, engagmentTitle):
    userEngagementObj = UserEngagement.objects.get(category=engagmentTitle)
    engagementId = userEngagementObj.id
    context = {
        "imageInBackButton":
        "assets/images/backArrowOperational.svg",
        "focusBorder":
        "operational",
        "boxObject":
        userEngagementObj,
        "backLinkText":
        _("Nutzendenintegration"),
        "backLink":
        "userEngagement",
        "leftColumn":
        "user_integration/userEngagementDetailsLeftColumn.html",
        "rightColumn":
        "user_integration/userEngagementDetailsRightColumn.html",
        "imageQuickLinks":
        True,
        "idOfSelectedObj":
        engagementId,
        "allObjectsForQuickLinks":
        UserEngagement.objects.all(),
        "showInputsInImageQuickLinkBar":
        False,
        "showSelect":
        True,
        "tags": [
            currentUserEnagementObj.category
            for currentUserEnagementObj in UserEngagement.objects.all()
        ],
        "quickLinkName":
        "user_integration/userEngagement",
        "javascriptFilePath":
        "js/user_integration_functions.js",
    }

    return render(request, "pages/detailsPage.html", context)
