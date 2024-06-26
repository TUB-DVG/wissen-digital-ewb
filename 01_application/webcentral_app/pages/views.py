"""views of pages app."""
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template import Template, Context

from component_list.models import (
    EnvironmentalImpact,
    DataSufficiency,
)
from businessModel.models import UserEngagement
from criteriaCatalog.models import CriteriaCatalog


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


def businessModelsPractice(request):
    """Call render function for business models best practice page."""
    return render(request, "pages/businessModelsPractice.html")


def businessModels(request):
    """Call render function for business models best practice page."""
    context = {
        "focusBorder":
        "operational",
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Geschäftsmodelle"),
        "showMorePresent":
        False,
        "explanaitionText":
        _("Der Fokus in einem Forschungsprojekt liegt häufig in einem innovativen Produkt, einer digitalen Anwendung oder auch einer neuen Software. Bei der Erstellung des Prototyps endet in den meisten Fällen die Entwicklung im Forschungsprojekt. Bei einer erfolgreichen Entwicklung ist die Übersetzung in ein Geschäftsmodell jedoch wünschenswert. Die hier aufzufindenden Informationen sollen dabei helfen, die Entwicklung von Geschäftsmodellen zu unterstützen und auftretende Herausforderungen zu meistern. Dafür wurden aus bisherigen Forschungsprojekte in Interviews und Workshops Herausforderungen gesammelt, geclustert und erste Lösungsansätze diskutiert. Daneben wurde auch eine Sammlung von Tools erstellt, die bei der Entwicklung vom Prototyp zum Geschäftsmodell unterstützen."
          ),
        "boxes": [
            {
                "boxId": 1,
                "pathToTemplate": "partials/businessModelsBox.html",
                "objectToRender": {
                    "image":
                    "img/businessModelsOverviewImg.svg",
                    "linkToDetailsPage":
                    "businessModelsChallenge",
                    "heading":
                    _("Herausforderungen bei der Entwicklung und Umsetzung"),
                    "description":
                    _("Bei der Umsetzung von Prototypen digitaler Anwendungen in ein funktionierendes Geschäftsmodell gibt es zahlreiche Herausforderungen. Diese ergeben sich durch strukturelle Faktoren wie die Förderbedingungen, durch technische oder organisatorische Faktoren wie die Übertragbarkeit sowie durch ökonomische und soziale Faktoren wie schwierige Finanzierungsmodelle. Ein Überblick über Hürden und mögliche Lösungen bietet hier eine Hilfestellung."
                      ),
                },
            },
            {
                "boxId": 2,
                "pathToTemplate": "partials/businessModelsBox.html",
                "objectToRender": {
                    "image":
                    "img/componentList/negativeEnvironmentalImpactsBox1.svg",
                    "linkToDetailsPage":
                    "businessModelApplication",
                    "heading":
                    _("Anwendungen zur Entwicklung von Geschäftsmodellen"),
                    "description":
                    _("Die Entwicklung erfolgreicher Geschäftsmodelle erfordert die Berücksichtigung einer Vielzahl von Akteuren und Rahmenbedingungen. Dabei kann es hilfreich sein, sich mithilfe eines Leitfadens oder einer Struktur alle Faktoren vorzunehmen, die für eine erfolgreiche Umsetzung berücksichtigt werden sollten. Ein Überblick über unterstützende Tools bei der Entwicklung oder Verbesserung von Geschäftsmodellen bietet hier eine Hilfestellung."
                      ),
                },
            },
        ],
    }
    return render(request, "pages/businessModels.html", context)


def userIntegrationPractice(request):
    """Call render function for user integration best practice page."""
    return render(request, "pages/userIntegrationPractice.html")


def userIntegrationMethod(request):
    """Call render function for user integration method page."""
    return render(request, "pages/userIntegrationMethod.html")


def userEngagement(request):
    """Call render function for user engagement page."""
    userEngagementObjs = UserEngagement.objects.all()
    context = {
        "focusBorder":
        "operational",
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Nutzendenintegration"),
        "showMorePresent":
        False,
        "explanaitionText":
        _("Entscheidender Erfolgsfaktor für Nutzen und Nutzung digitaler Produkte ist deren Usability. Um diese sicherzustellen beziehungsweise zu erhöhen, ist die Nutzendenintegration in sämtlichen Phasen des Entwicklungsprozesses eines digitalen Produktes sinnvoll, das heißt sowohl in der Analysephase, Konzeptionsphase als auch in der Umsetzungs- und Evaluationsphase. Als Methoden für die Analysephase eignen sich besonders Einzelinterviews, Gruppeninterviews / Fokusgruppen, teilnehmende Beobachtungen und Personas."
          ),
        "boxes": [{
            "pathToTemplate":
            "businessModel/userEngagementBox.html",
            "objectToRender":
            userEngagementObj,
            "linkToDetailsPage":
            "userIntegrationMethod",
            "heading":
            _("Methoden zur Nutzendenintegration"),
            "description":
            _("Entscheidender Erfolgsfaktor für Nutzen und Nutzung digitaler Produkte ist deren Usability. Um diese sicherzustellen beziehungsweise zu erhöhen, ist die Nutzendenintegration in sämtlichen Phasen des Entwicklungsprozesses eines digitalen Produktes sinnvoll, das heißt sowohl in der Analysephase, Konzeptionsphase als auch in der Umsetzungs- und Evaluationsphase. Als Methoden für die Analysephase eignen sich besonders Einzelinterviews, Gruppeninterviews / Fokusgruppen, teilnehmende Beobachtungen und Personas."
              ),
            "image":
            "img/componentList/negativeEnvironmentalImpactsBox1.svg",
        } for userEngagementObj in userEngagementObjs],
    }
    return render(request, "pages/userEngagement.html", context)


def environmentalIntegrityNegativ(request):
    """Call render function for negativ environmental integrity page."""

    linkToDynamicallyRender = '<a class="ecological-font-color" href="{% url \'environmentalIntegrityNegativ\' %}">positive Umweltwirkungen</a>'
    templateObj = Template(linkToDynamicallyRender)
    renderedTemplate = templateObj.render(Context({}))

    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Negative Umweltwirkungen"),
        "showMorePresent":
        False,
        "explanaitionText":
        _(f"""Digitale Anwendungen zeichnen sich oftmals durch {renderedTemplate} aus. Sie können sich jedoch auch negativ auf die Umwelt auswirken bzw. sie belasten. Ausgehend vom Lebenszyklus der verwendeten Produkte und Services ergeben sich Umweltlasten von der Rohstoffgewinnung, über den Energieverbrauch im Betrieb bis zur Entsorgung der Technologie. Die Umweltlasten digitaler Anwendungen lassen sich dabei grob in zwei Bereiche unterscheiden. Zum einen werden bei der Nutzung digitaler Technologien in Gebäuden unterschiedliche Datenverarbeitungsprozesse durchlaufen und dabei die digitale Infrastruktur in Anspruch genommen (z. B. Rechenzentren). Zum anderen müssen für die Nutzung der Daten oftmals zusätzliche Hardwarekomponenten in den Gebäuden installiert werden. Aus der Summe dieser Aufwände lassen sich so die Umweltlasten, hervorgerufen durch die digitale Anwendung, abschätzen.
        \nZur Bestimmung der Umweltlasten sind Hinweise zur Abschätzung daher hier in die Bereiche „Aufwände für Datenverarbeitungsprozesse“ und „Aufwände für häufig verwendete Komponenten“ unterteilt."""
          .replace("\n", "<br>")),
        "boxes": [
            {
                "boxId":
                1,
                "pathToTemplate":
                "partials/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage":
                "components",
                "heading":
                _("Aufwände für verwendete Komponenten"),
                "description":
                _("Die Implementierung einer digitalen Anwendung in bspw. Gebäuden ist in der Regel mit einem Energie- und Ressourcenaufwand für die Hardwarekomponenten verbunden. Das sind alle Komponenten, die einen zweckmäßigen Betrieb der digitalen Anwendung sicherstellen. Je nachdem, welche dieser Komponenten zusätzlich für die digitale Anwendung verbaut werden, müssen die entsprechenden Umweltlasten mitbilanziert werden (inkl. aller Lebensphasen). Werden bestehende Komponenten genutzt, können die Lasten durch die anteilige Nutzung in die Bilanz einfließen. Die hier dargestellte Übersicht zu häufig verwendeten Komponenten (Fokus Betriebsoptimierung von Gebäuden) soll einen einfachen Überblick zu den Hardware-bezogenen Umweltlasten bieten."
                  ),
                "image":
                "img/componentList/backBoneOverviewImg.svg",
                "headingOfImage":
                _("Backbone der Daten-Wertschöpfungskette (Fokus Betriebsoptimierung)"
                  ),
            },
            {
                "boxId":
                2,
                "pathToTemplate":
                "partials/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage":
                "dataProcessing",
                "heading":
                _("Aufwände für Datenverarbeitungsprozesse"),
                "description":
                _("Bei der Nutzung digitaler Technologien für den Einsatz in Gebäuden und Quartieren werden unterschiedliche Datenverarbeitungsprozesse durchlaufen, die sich in der Regel ständig wiederholen. Dadurch kommt es ununterbrochen zur Generierung von Daten, was mit einem entsprechenden Energie- und Ressourcenverbrauch verbunden ist. Die Aufwände, die für die Nutzung der entsprechenden Dateninfrastruktur entstehen, werden hier näher erläutert. Einfache Abschätzungen anhand des Datenaufkommens werden ebenfalls vorgenommen."
                  ),
                "image":
                "img/componentList/dataPipelineOverviewImg.svg",
                "headingOfImage":
                _("Die Daten-Wertschöpfungkette"),
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
        "imageInBackButton": "img/componentList/caret-left.svg",
        "boxObject": environmentalImpactObj,
        "focusBorder": "ecological",
        "backLinkText": _("Positive Umweltwirkungen"),
        "backLink": "environmentalIntegrityPositiv",
        "leftColumn": "pages/environmentalIntegrityLeftColumn.html",
        "rightColumn": "pages/environmentalIntegrityRightColumn.html",
    }
    return render(request, "pages/detailsPage.html", context)


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
        "imageInBackButton": "img/componentList/caret-left.svg",
        "boxObject": dataSufficiencyObj,
        "focusBorder": "ecological",
        "focusName": "ecological",
        "urlName": "dataProcessing",
        "backLinkText": _("Datensuffizienz"),
        "backLink": "dataSufficiency",
        "leftColumn": "pages/dataSufficiencyLeftColumn.html",
        "rightColumn": "pages/dataSufficiencyRightColumn.html",
    }
    return render(request, "pages/detailsPage.html", context)


def dataSecurity(request):
    """Call render function for data security page."""
    return render(request, "pages/dataSecurity.html")


def iconsAndVis(request):
    """Call render function for icons and Visualization page."""
    return render(request, "pages/iconsAndVis.html")


def criteriaCatalog(request):
    """Call render function for criteria catalog page."""
    criteriaCatalogObjs = CriteriaCatalog.objects.all()
    context = {
        "pathToImage":
        "img/componentList/circle-icon.svg",
        "heading":
        _("Kriterienkatalog"),
        "showMorePresent":
        False,
        "explanaitionText":
        _("Text (Generelle Erläuterungen) Hier steht ein Platzhaltertext: Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."),
        "boxes": [{
            "pathToTemplate":
            "criteriaCatalog/criteriaCatalogOverviewBox.html",
            "objectToRender": criteriaCatalogObj,
        } for criteriaCatalogObj in criteriaCatalogObjs],
        "focusBorder":
        "legal",
    }

    return render(request, "pages/criteriaCatalog.html", context)


def impressum(request):
    """Call render function for impressum page."""
    return render(request, "pages/impressum.html")


def showImage(request, idOfEnvironmentalImpactObj):
    """Call render function for show image page."""
    environmentalObjToReturn = EnvironmentalImpact.objects.get(
        id=idOfEnvironmentalImpactObj)
    context = {
        "imageInBackButton": "img/componentList/caret-left.svg",
        "imageName": environmentalObjToReturn.image,
        "backLink": "environmentalIntegrityBox",
        "backLinkParam": idOfEnvironmentalImpactObj,
        "backLinkText": environmentalObjToReturn.project_name,
        "focusBorder": "ecological",
    }
    return render(request, "pages/showImage.html", context)
