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
    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Negative Umweltwirkungen"),
        "showMorePresent":
        False,
        "explanaitionText":
        _("Digitale Anwendungen können dazu beitragen, positive Umweltwirkungen wie bspw. Energieeinsparungen zu realisieren. Die Zielerreichung ist jedoch auch immer mit einem Material- und Ressourcenbedarf verbunden. Um überhaupt digitale Anwendungen nutzen zu können, müssen die entsprechenden Komponenten verbaut werden. Wie bei anderen Produkten auch, fallen Emissionen sowohl bei der Herstellung als auch im Betrieb und zum Lebensende an. Für digitale Anwendungen muss zudem der materielle und energetische Aufwand für die involvierten Prozesse zur effektiven Nutzung der Daten bilanziert werden. Die folgenden Übersichten sollen dabei helfen, einen Überblick über wichtige Teilaspekte bei der Bilanzierung der Umweltlasten zu erhalten. Dabei dient die Betriebsoptimierung von Gebäuden und Quartieren beispielhafte digitale Anwendung. Viele der dargestellten Komponenten und Datennutzungsschritte können aber auch auf andere digitale Anwendungen übertragen werden."
          ),
        "boxes": [
            {
                "pathToTemplate":
                "pages/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage":
                "components",
                "heading":
                _("Aufwände für verwendete Komponenten"),
                "description":
                _("In Analogie zur Daten-Wertschöpfungskette (siehe “Aufwände für Datenverarbeitungsprozesse”) können wichtige Komponenten von der Datenerfassung (Sensoren) bis zur Datennutzung (Aktuatoren) gedacht werden. Abbildung 2 zeigt wichtige Komponenten, die zur Realisierung einer effektiven Nutzung von Daten für die Betriebsoptimierung von Gebäuden und Quartieren notwendig sind. Je nachdem welche dieser – oder weitere – Komponenten zusätzlich für die digitale Anwendung verbaut werden mussten, müssen die entsprechenden Umweltlasten mit in die Bilanz einfließen. Dabei sind alle Lebenszyklusphasen mit zu betrachten. Hier finden Sie wichtige Komponenten und deren Umweltlasten"
                  ),
                "image":
                "img/componentList/negativeEnvironmentalImpactsBox1.svg",
            },
            {
                "pathToTemplate":
                "pages/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage":
                "dataProcessing",
                "heading":
                _("Aufwände für Datenverarbeitungsprozesse"),
                "description":
                _("In Analogie zur Daten-Wertschöpfungskette (siehe “Aufwände für Datenverarbeitungsprozesse”) können wichtige Komponenten von der Datenerfassung (Sensoren) bis zur Datennutzung (Aktuatoren) gedacht werden. Abbildung 2 zeigt wichtige Komponenten, die zur Realisierung einer effektiven Nutzung von Daten für die Betriebsoptimierung von Gebäuden und Quartieren notwendig sind. Je nachdem welche dieser – oder weitere – Komponenten zusätzlich für die digitale Anwendung verbaut werden mussten, müssen die entsprechenden Umweltlasten mit in die Bilanz einfließen. Dabei sind alle Lebenszyklusphasen mit zu betrachten. Hier finden Sie wichtige Komponenten und deren Umweltlasten"
                  ),
                "image":
                "img/componentList/negativeEnvironmentalImpactsBox1.svg",
            },
        ],
        "focusBorder":
        "ecological",
    }
    return render(request, "pages/environmentalIntegrityNegativ.html", context)


def environmentalIntegrityPositiv(request):
    """Call render function for positiv environmental integrity page."""

    # get number of environmentalImpact-objects and render them as boxes:
    environmentalImpacts = EnvironmentalImpact.objects.all()
    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Positive Umweltwirkungen"),
        "showMorePresent":
        False,
        "explanaitionText":
        _("Neben der wissenschaftlichen Entwicklung digitaler Anwendungen, müssen erprobte Technologien auch ökonomisch umgesetzt werden. Hierzu sind Geschäftsmodelle notwendig, sodass das Potenzial der digitalen Anwendung als Produkt oder Service einer möglichst breiten Anwenderschaft zur Verfügung gestellt werden kann. Eine Reihe von Tools kann die Geschäftsmodellentwicklungunterstützen. Einige von diesen werden hier vorgestellt."
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


def showImage(request, idOfEnvironmentalImpactObj):
    """Call render function for show image page."""
    environmentalObjToReturn = EnvironmentalImpact.objects.get(
        id=idOfEnvironmentalImpactObj)
    context = {
        "imageName": environmentalObjToReturn.image,
        "backLink": "environmentalIntegrityBox",
        "backLinkParam": idOfEnvironmentalImpactObj,
        "backLinkText": environmentalObjToReturn.project_name,
    }
    return render(request, "pages/showImage.html", context)
