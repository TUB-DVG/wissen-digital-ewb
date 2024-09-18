"""views of pages app."""

from django.shortcuts import render
from django.utils.translation import gettext as _
from django.template import Template, Context

from positive_environmental_impact.models import (
    EnvironmentalImpact,
)
from data_sufficiency.models import (
    DataSufficiency,
)
from user_integration.models import UserEngagement
from criteria_catalog.models import CriteriaCatalog


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
        "focusBorder": "operational",
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Geschäftsmodelle"),
        "showMorePresent": False,
        "explanaitionText": _(
            "Der Fokus in einem Forschungsprojekt liegt häufig in einem innovativen Produkt, einer digitalen Anwendung oder auch einer neuen Software. Bei der Erstellung des Prototyps endet in den meisten Fällen die Entwicklung im Forschungsprojekt. Bei einer erfolgreichen Entwicklung ist die Übersetzung in ein Geschäftsmodell jedoch wünschenswert. Die hier aufzufindenden Informationen sollen dabei helfen, die Entwicklung von Geschäftsmodellen zu unterstützen und auftretende Herausforderungen zu meistern. Dafür wurden aus bisherigen Forschungsprojekte in Interviews und Workshops Herausforderungen gesammelt, geclustert und erste Lösungsansätze diskutiert. Daneben wurde auch eine Sammlung von Tools erstellt, die bei der Entwicklung vom Prototyp zum Geschäftsmodell unterstützen."
        ),
        "boxes": [
            {
                "boxId": 1,
                "pathToTemplate": "partials/businessModelsBox.html",
                "objectToRender": {
                    "imageDe": "assets/images/geschaeftsmodelle_de_small.svg",
                    "imageEn": "assets/images/geschaeftsmodelle_en_small.svg",
                    "linkToDetailsPage": "businessModelsChallenge",
                    "heading": _(
                        "Herausforderungen bei der Entwicklung und Umsetzung"
                    ),
                    "description": _(
                        "Bei der Umsetzung von Prototypen digitaler Anwendungen in ein funktionierendes Geschäftsmodell gibt es zahlreiche Herausforderungen. Diese ergeben sich durch strukturelle Faktoren wie die Förderbedingungen, durch technische oder organisatorische Faktoren wie die Übertragbarkeit sowie durch ökonomische und soziale Faktoren wie schwierige Finanzierungsmodelle. Ein Überblick über Hürden und mögliche Lösungen bietet hier eine Hilfestellung."
                    ),
                },
            },
            {
                "boxId": 2,
                "pathToTemplate": "partials/businessModelsBox.html",
                "objectToRender": {
                    "imageEn": "assets/images/anwendungen_en_small.svg",
                    "imageDe": "assets/images/anwendungen_de_small.svg",
                    "linkToDetailsPage": "businessModelApplication",
                    "heading": _(
                        "Anwendungen zur Entwicklung von Geschäftsmodellen"
                    ),
                    "description": _(
                        "Die Entwicklung erfolgreicher Geschäftsmodelle erfordert die Berücksichtigung einer Vielzahl von Akteuren und Rahmenbedingungen. Dabei kann es hilfreich sein, sich mithilfe eines Leitfadens oder einer Struktur alle Faktoren vorzunehmen, die für eine erfolgreiche Umsetzung berücksichtigt werden sollten. Ein Überblick über unterstützende Tools bei der Entwicklung oder Verbesserung von Geschäftsmodellen bietet hier eine Hilfestellung."
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
    explanationTextParagraphOne = _(
        "<p>Die Nutzendenintegration beschreibt die direkte oder indirekte Integration von Nutzenden und ihren Perspektiven in die Entwicklung digitaler Anwendungen. Die direkte Beteiligung geschieht über Methoden wie Beobachtungen, Befragungen oder Usability-Tests von Nutzenden. Indirekte Nutzendenintegration findet mit Methoden wie Cognitive Walkthrough oder Heuristische Evaluation statt, in denen Usability-Expert*innen eingebunden werden, die über fundiertes Wissen über Nutzende digitaler Anwendungen verfügen.</p>"
    )
    explanationTextParagraphTwo = _(
        "<p>Nutzendenintegration <b>erhöht die Gebrauchstauglichkeit bzw. Nutzendenfreundlichkeit – oder kurz: die Usability – digitaler Anwendungen</b>, indem sie Wissen zu geeigneten Zielgruppen der Anwendungen sowie zu den Bedürfnissen, Nutzungsgewohnheiten und dem Vorwissen von diesen Zielgruppen generiert. Auf dieser Basis können die digitalen Anwendungen zielgruppenorientiert (weiter-)entwickelt werden.</p>"
    )
    explanationTextPart3 = _(
        "<p>Maßnahmen wie die Nutzendenintegration, die für eine gute Usability vor der Markteinführung einer digitalen Anwendung sorgen, erhöhen die Zufriedenheit der Nutzenden, reduzieren den Aufwand für die Pflege oder Instandhaltung der Anwendung und sparen so Kosten in erheblichem Ausmaß.</p>"
    )
    explanationPart4 = _(
        "<p>Die Methoden der Nutzendenintegration können nach <b>Methoden der Analysephase, Methoden der Konzeptionsphase sowie Methoden der Umsetzung- und Evaluierungsphase</b> unterschieden werden. Hierbei werden qualitative Methoden (z. B. Interviews oder teilnehmende Beobachtung) vor allem in früheren Phasen der Entwicklung digitaler Anwendungen eingesetzt, während quantitative Methoden (z. B. Usability-Befragung) eher in späteren Phasen umgesetzt werden. Dies beruht darauf, dass es in früheren Phasen der Entwicklung digitaler Anwendungen vor allem um die Exploration von Bedürfnissen, Vorwissen und Nutzungsgewohnheiten von Nutzenden geht. Für diese Exploration sind qualitative Methoden besonders geeignet. In späteren Phasen der Anwendungsentwicklung geht es vor allem um die Testung, wie gut die entwickelte digitale Anwendung den Bedürfnissen, dem Vorwissen und den Nutzungsgewohnheiten von Nutzenden entspricht. Hier haben quantitative Methoden ihre Stärken, da sie hierzu repräsentative Aussagen ermöglichen.</p>"
    )
    explanationPart5 = _(
        "<p>Auf dieser Wissensplattform werden <b>12 bewährte Methoden der Nutzendenintegration</b> mit ihren jeweiligen Zielstellungen, Abläufen sowie Vor- und Nachteilen dargestellt. Dabei werden sie jeweils einer der drei Phasen der Entwicklung einer digitalen Anwendung zugeordnet (Analysephase, Konzeptionsphase sowie Umsetzungs- und Evaluationsphase). Sie sind aber nicht nur in dieser Phase einsetzbar, sondern lassen sich oft ebenso gut in anderen Phasen sinnvoll nutzen.</p>"
    )
    explanationPart6 = _(
        '<h6 style="font-size: 22px">Methoden der Nutzendenintegration für die Analysephase vor Beginn der Anwendungsentwicklung</h6>'
    )
    translationObserver = _("Teilnehmende Beobachtung")
    translationIndividualInterview = _("Einzel-Interview")
    explanationText = (
        explanationTextParagraphOne
        + explanationTextParagraphTwo
        + explanationTextPart3
        + explanationPart4
        + explanationPart5
        + explanationPart6
        + f"<ul>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Teilnehmende Beobachtung' %}\">"
        + translationObserver
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Einzel-Interview' %}\">"
        + translationIndividualInterview
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Gruppen-Interview/Fokusgruppe' %}\">"
        + _("Gruppen-Interview/Fokusgruppe")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Personas' %}\">"
        + _("Personas")
        + "</a></li>"
    )
    explanationText += "</ul>"
    explanationText += (
        '<h6 style="font-size: 22px">'
        + _(
            "Methoden der Nutzendenintegration für die Konzeptionsphase zu Beginn der Anwendungsentwicklung"
        )
        + "</h2>"
    )
    explanationText += "<ul>"
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'A/B-Test' %}\">"
        + _("A/B-Test")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Prototyping' %}\">"
        + _("Prototyping")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Cognitive Walkthrough' %}\">"
        + "Cognitive Walkthrough"
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Styleguide' %}\">"
        + _("Styleguide")
        + "</a></li>"
    )
    explanationText += "</ul>"
    explanationText += (
        '<h6 style="font-size: 22px">'
        + _(
            "Methoden der Nutzendenintegration für die Umsetzungs- und Evaluationsphase während bzw. nach der Anwendungsentwicklung"
        )
        + "</h6>"
    )
    explanationText += "<ul>"
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Lautes Denken' %}\">"
        + _("Lautes Denken")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Eyetracking' %}\">"
        + _("Eyetracking")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Heuristische Evaluation' %}\">"
        + _("Heuristische Evaluation")
        + "</a></li>"
    )
    explanationText += (
        "<li><a href=\"{% url 'userEngagementDetailsTitle' 'Usability-Befragung' %}\">"
        + _("Usability-Befragung")
        + "</a></li>"
    )
    explanationText += "</ul>"
    explanationText.replace("\n", "")
    templateObj = Template(explanationText)
    contextObj = Context({})

    userEngagementObjs = UserEngagement.objects.all()
    context = {
        "focusBorder": "operational",
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Methoden der Nutzendenintegration"),
        # "showMorePresent":
        # True,
        "explanaitionText": templateObj.render(contextObj),
        "boxes": [
            {
                "pathToTemplate": "user_integration/userEngagementBox.html",
                "objectToRender": userEngagementObj,
                "linkToDetailsPage": "userIntegrationMethod",
                "heading": _("Methoden zur Nutzendenintegration"),
                "description": _(
                    "Entscheidender Erfolgsfaktor für Nutzen und Nutzung digitaler Produkte ist deren Usability. Um diese sicherzustellen beziehungsweise zu erhöhen, ist die Nutzendenintegration in sämtlichen Phasen des Entwicklungsprozesses eines digitalen Produktes sinnvoll, das heißt sowohl in der Analysephase, Konzeptionsphase als auch in der Umsetzungs- und Evaluationsphase. Als Methoden für die Analysephase eignen sich besonders Einzelinterviews, Gruppeninterviews / Fokusgruppen, teilnehmende Beobachtungen und Personas."
                ),
                "image": "img/componentList/negativeEnvironmentalImpactsBox1.svg",
            }
            for userEngagementObj in userEngagementObjs
        ],
        # "charNumberToShowCollapsed":
        # 629,
    }
    return render(request, "pages/userEngagement.html", context)


def environmentalIntegrityNegativ(request):
    """Call render function for negativ environmental integrity page."""

    if request.LANGUAGE_CODE == "de":
        environmentalPositiveLinkText = "positive Umweltwirkungen"
    else:
        environmentalPositiveLinkText = "positive environmental impacts"

    explanationPartOne = _("Digitale Anwendungen zeichnen sich oftmals durch")
    linkToDynamicallyRender = (
        ' <a class="ecological-font-color" href="{% url \'environmentalIntegrityPositiv\' %}">'
        + environmentalPositiveLinkText
        + "</a>"
    )
    templateObj = Template(linkToDynamicallyRender)
    renderedTemplate = templateObj.render(Context({}))
    explanationPartTwo = _(
        """ aus. Sie können sich jedoch auch negativ auf die Umwelt auswirken bzw. sie belasten. Ausgehend vom Lebenszyklus der verwendeten Produkte und Services ergeben sich Umweltlasten von der Rohstoffgewinnung, über den Energieverbrauch im Betrieb bis zur Entsorgung der Technologie. Die Umweltlasten digitaler Anwendungen lassen sich dabei grob in zwei Bereiche unterscheiden. Zum einen werden bei der Nutzung digitaler Technologien in Gebäuden unterschiedliche Datenverarbeitungsprozesse durchlaufen und dabei die digitale Infrastruktur in Anspruch genommen (z. B. Rechenzentren). Zum anderen müssen für die Nutzung der Daten oftmals zusätzliche Hardwarekomponenten in den Gebäuden installiert werden. Aus der Summe dieser Aufwände lassen sich so die Umweltlasten, hervorgerufen durch die digitale Anwendung, abschätzen.
        \nZur Bestimmung der Umweltlasten sind Hinweise zur Abschätzung daher hier in die Bereiche „Aufwände für Datenverarbeitungsprozesse“ und „Aufwände für häufig verwendete Komponenten“ unterteilt."""
    ).replace("\n", "<br>")
    context = {
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Negative Umweltwirkungen"),
        "showMorePresent": False,
        "explanaitionText": explanationPartOne
        + renderedTemplate
        + explanationPartTwo,
        "boxes": [
            {
                "boxId": 1,
                "pathToTemplate": "partials/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage": "components",
                "heading": _("Aufwände für verwendete Komponenten"),
                "description": _(
                    "Die Implementierung einer digitalen Anwendung in bspw. Gebäuden ist in der Regel mit einem Energie- und Ressourcenaufwand für die Hardwarekomponenten verbunden. Das sind alle Komponenten, die einen zweckmäßigen Betrieb der digitalen Anwendung sicherstellen. Je nachdem, welche dieser Komponenten zusätzlich für die digitale Anwendung verbaut werden, müssen die entsprechenden Umweltlasten mitbilanziert werden (inkl. aller Lebensphasen). Werden bestehende Komponenten genutzt, können die Lasten durch die anteilige Nutzung in die Bilanz einfließen. Die hier dargestellte Übersicht zu häufig verwendeten Komponenten (Fokus Betriebsoptimierung von Gebäuden) soll einen einfachen Überblick zu den Hardware-bezogenen Umweltlasten bieten."
                ),
                "image": "img/componentList/backBoneOverviewImg.svg",
                "headingOfImage": _(
                    "Backbone der Daten-Wertschöpfungskette (Fokus Betriebsoptimierung)"
                ),
            },
            {
                "boxId": 2,
                "pathToTemplate": "partials/environmentalIntegrityNegativeBox.html",
                "linkToDetailsPage": "dataProcessing",
                "heading": _("Aufwände für Datenverarbeitungsprozesse"),
                "description": _(
                    "Bei der Nutzung digitaler Technologien für den Einsatz in Gebäuden und Quartieren werden unterschiedliche Datenverarbeitungsprozesse durchlaufen, die sich in der Regel ständig wiederholen. Dadurch kommt es ununterbrochen zur Generierung von Daten, was mit einem entsprechenden Energie- und Ressourcenverbrauch verbunden ist. Die Aufwände, die für die Nutzung der entsprechenden Dateninfrastruktur entstehen, werden hier näher erläutert. Einfache Abschätzungen anhand des Datenaufkommens werden ebenfalls vorgenommen."
                ),
                "image": "img/componentList/dataPipelineOverviewImg.svg",
                "headingOfImage": _("Die Daten-Wertschöpfungkette"),
            },
        ],
        "focusBorder": "ecological",
    }
    return render(request, "pages/environmentalIntegrityNegativ.html", context)


def environmentalIntegrityPositiv(request):
    """Call render function for positiv environmental integrity page."""

    # get number of environmentalImpact-objects and render them as boxes:
    environmentalImpacts = EnvironmentalImpact.objects.all()
    context = {
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Positive Umweltwirkungen"),
        "showMorePresent": False,
        "explanaitionText": _(
            "Die Reduktion des Energiebedarfs und der CO<sub>2</sub>-Emissionen von Gebäuden und Quartieren steht im derzeitigen Fokus der Forschung. Gleichzeitig stellt dieses Ziel nur eine der möglichen positiven Umweltwirkungen dar, die mittels digitaler Anwendungen ermöglicht werden. Auch in Projekten der Forschungsinitiative Energiewendebauen kommen eine Vielzahl digitaler Anwendungen zum Einsatz oder werden entwickelt, mit denen sich positive Umweltwirkungen erzielen lassen. Auch wenn die Effekte oftmals schwer auf andere Gebäude/Quartiere zu übertragen sind, gibt es doch immer Forschungsprojekte an denen die Potenziale bestimmter digitaler Anwendungen gut verdeutlicht werden können. Diese sollen im Folgenden kurz vorgestellt werden. Dazu wird die eingesetzte digitale Anwendung beschrieben und die gefundenen positiven Umweltwirkungen erörtert. Das Ziel dieser Übersicht ist das Aufzeigen von derzeitigen Möglichkeiten digitaler Anwendungen, positive Umweltwirkungen zu erzielen. Der dadurch geschaffene Anreiz soll Interessierte animieren, sich eingehender mit den Möglichkeiten digitaler Anwendungen zu beschäftigen, um so für eigene Vorhaben fundierte Entscheidungen treffen zu können."
        ),
        "boxes": [
            {
                "pathToTemplate": "pages/environmentalIntegrityBox.html",
                "objectToRender": environmentalImpact,
            }
            for environmentalImpact in environmentalImpacts
        ],
        "focusBorder": "ecological",
    }

    return render(request, "pages/environmentalIntegrityPositiv.html", context)


def environmentalIntegrityBox(request, idOfEnvironmentalImpactObj):
    """Call render function for environmental integrity box page."""
    environmentalImpactObj = EnvironmentalImpact.objects.get(
        id=idOfEnvironmentalImpactObj
    )
    context = {
        "pageTitle": environmentalImpactObj.project_name,
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

    dataSufficencyIntroductionText = _(
        """Sowohl die Materialisierung als auch der Energieaufwand für den Betrieb immer größer werdender Rechenkapazitäten sind mit negativen Umweltwirkungen verbunden. Der sparsame Umgang mit Daten – die Datensuffizienz – gewinnt daher zunehmend an Relevanz, um das Datenvolumen insgesamt möglichst klein zu halten. Die Datensuffizienz schaut dabei auf alle Bereiche der Datenverarbeitung: von der Erhebung, der Weiterverarbeitung, der Speicherung bis zur Löschung. Gerade die ökologischen Auswirkungen eines (in-)suffizienten Umgangs mit Daten sind derzeit noch wenig untersucht und bleiben in der Praxis oftmals unbeachtet.

Unter dem Grundsatz „Datensuffizienz“ verstehen wir, dass Daten nur in dem notwendigen Maße erhoben, übermittelt, verarbeitet und gespeichert werden, wie damit ein Nutzen für einen energieeffizienten und -sparsamen Betrieb verbunden ist. Dieser Begriff ordnet unter sich unter „Software-Suffizienz“ ein als Teil der Digitalen Suffizienz aus Santarius et al. (2023). Gleichzeitig soll bei der Datenerhebung, -übermittlung, -verarbeitung und -speicherung Hardware mit ressourcenschonendem Materialeinsatz und ressourcenschonende Übermittlungswege gewählt werden. Damit sollen die negativen ökologischen Wirkungen, die mit der Implementierung digitaler Anwendungen einhergehen, möglichst reduziert werden, während ein möglichst großer Nutzen erzielt werden soll.  

Damit grenzt sich die Datensuffizienz von dem juristischen Begriff der Datenminimierung ab. Dieser ist ein Datenschutz-Grundsatz, der in Art. 5 Abs. 1c der Datenschutz-Grundverordnung (DSGVO) für personenbezogene Daten definiert ist, und darauf abzielt, das Risiko für die Rechte und Freiheiten natürlicher Personen zu reduzieren. Der Begriff Datenminimierung aus der DSGVO ersetzt die Begriffe Datensparsamkeit und -vermeidung, die im Bundesdatenschutzgesetz (§3a BDSG) verwendet wurden.

Während die Datenminimierung also Grundrechtsrisiken durch extensive, nicht erforderliche Datenverarbeitung verhindert, zielt die Datensuffizienz darauf ab, die ökologischen Wirkungen durch die Erhebung, Verarbeitung und Speicherung von extensiven, nicht erforderlichen Daten zu minimieren. Um eine Abgrenzung zu dem juristischen Begriff zu verdeutlichen, werden unterschiedliche Begriffe verwendet.

Forschungsprojekte sind von Natur aus so konzipiert, dass zunächst Daten generiert werden, von denen im Vorfeld nicht immer absehbar ist, welchen Zweck sie im weiteren Verlauf erfüllen werden und ob den Erwartungen an eine Forschungsarbeit auch entsprochen wird. Diese Maxime wissenschaftlichen Arbeitens soll auch mit diesem Ansatz nicht in Frage gestellt werden, jedoch sollte Datensuffizienz bei der Entwicklung im Hinblick auf die spätere Nutzungsphase mitgedacht werden. Denn werden die in Forschungsprojekten entwickelten digitalen Lösungen auf den Markt gebracht, können bei der Verbreitung datensparsamer Technologien durch die Mengeneffekte ökologische Wirkungen erzielt werden.   

Im Folgenden werden Strategien für einen suffizienten Umgang mit vorgestellt und auf die ökologischen Wirkungen beim Umgang mit Daten hingewiesen.

Literatur

Santarius, Tilman, Bieser, Jan C.T., Frick, Vivian, Höjer, Mattias, Gossen, Maike, Hilty, Lorenz M., Kern, Eva, Pohl, Johanna, Rohde, Friederike, Lange, Steffen (2023): Digitale Suffizienz: konzeptionelle Überlegungen für IKT auf einem endlichen Planeten. Annals of Telekommunikation. 78, 277–295 (2023). https://doi.org/10.1007/s12243-022-00914-x
    """.replace(
            "\n", "<br>"
        )
    )

    context = {
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Datensuffizienz"),
        "explanaitionText": dataSufficencyIntroductionText,
        "boxes": [
            {
                "pathToTemplate": "pages/dataSufficiencyBox.html",
                "objectToRender": dataSufficiencyObj,
            }
            for dataSufficiencyObj in dataSufficiencyObjs
        ],
        "focusBorder": "ecological",
        "showMorePresent": True,
        "charNumberToShowCollapsed": 616,
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
        "leftColumn": "data_sufficiency/dataSufficiencyLeftColumn.html",
        "rightColumn": "data_sufficiency/dataSufficiencyRightColumn.html",
    }
    return render(request, "pages/detailsPage.html", context)


def dataSecurity(request):
    """Call render function for data security page."""

    explanText = _(
        """Beim Einsatz digitaler Anwendungen im Gebäude- und Quartierssektor
          lassen verschiedene Datenquellen zum Raumklima, Energieverbrauch oder
          bloße Gebäudeinformationen häufig Rückschlüsse auf das Verhalten von
          Einzelpersonen oder Personengruppen zu. Beziehen sich diese Daten auf
          eine identifizierte oder identifizierbare Person, findet das nationale
          bzw. europäische Datenschutzrecht Anwendung und mit ihm die gesamte
          Bandbreite rechtlicher Verpflichtungen für den Verantwortlichen der
          Datenverarbeitung. Ziel des Datenschutzrechts ist es dabei, die
          Betroffenen vor Risiken zu schützen, die durch die Datenverarbeitung
          verursacht werden und ihnen damit grundsätzlich die Entscheidung über
          das Maß und den Umgang mit diesen Risiken zu gewähren. Schon die
          Frage, ob eine Datenverarbeitung überhaupt in den Anwendungsbereich
          des Datenschutzrechts fällt, kann aber zur Herausforderung werden. Das
          dafür zentrale europäische Regelwerk - die Datenschutz-Grundverordnung
          (DSGVO) - ist nämlich an den sehr unbestimmten Begriff der
          personenbezogenen Daten geknüpft. Der Anwendungsbereich wurde dabei
          durch den Gesetzgeber bewusst weit gefasst und wird durch die Gerichte
          weit ausgelegt, um einen möglichst umfassenden Schutz der Betroffenen
          vor den Risiken verschiedener Datenverarbeitungen zu gewährleisten.
          Das liegt daran, dass sogar vermeintlich rein technische Daten wie
          Maschinen-Daten, Geo-Daten oder Gebäude-Daten Rückschlüsse über
          Personen zulassen können, wenn sie mit anderen Datensätzen verknüpft
          werden. Zur Erläuterung, wie Datenschutzrisiken bei der Verarbeitung
          von gebäudebezogenen Daten entstehen können und wann dadurch der
          Anwendungsbereich der DSGVO eröffnet wird, ist im Rahmen von Modul 4
          der Wissenschaftlichen Begleitforschung Energiewendebauen eine
          Datenschutzübersicht entstanden. Anhand verschiedener Use-Cases wird
          hier erklärt wann Datenschutzrisiken entstehen und wie diese durch den
          richtigen Einsatz technisch-organisatorischer Schutzmaßnahmen
          kontrolliert werden müssen.
    """
    ).replace("\n", "")
    explanToRender = """<p>
            <a href="https://www.energiewendebauen.de/lw_resource/datapool/systemfiles/agent/ewbpublications/E529BF584385483EE0537E695E86DD55/live/document/Effiziente_Datenminimierung_im_Geb%C3%A4ude-_und_Quartierssektor.pdf">"""
    explanToRender += _(
        "Effiziente Datenminimierung im Gebäude- und Quartierssektor"
    )
    explanToRender += """</a>
          </p>
          <p>
            <a href="{% url 'coming' %}">"""

    explanToRender += _(
        "Sammlung von Leitfäden, Literatur und Gerichtsentscheidungen"
    )
    explanToRender += "</a></p>"
    explanRendered = Template(explanToRender).render(Context({}))
    explanText += explanRendered
    context = {
        "focusBorder": "legal",
        "heading": _("Datenschutzübersicht"),
        "explanaitionText": explanText.replace("\n", ""),
        "pathToImage": "img/componentList/circle-icon.svg",
        "leftColumn": "partials/privacy_overview_left_column.html",
        "rightColumn": "partials/privacy_overview_right_column.html",
    }

    return render(request, "pages/detailsPage.html", context)


def iconsAndVis(request):
    """Call render function for icons and Visualization page."""

    explanationText = _(
        """Icons können auch im Gebäude- und Quartiersbereich die grafische
          Aufbereitung komplexer Sachverhalte unterstützen und dabei sowohl für
          die Informationsvermittlung an professionelle, wie auch fachfremde
          Adressat*innenkreise genutzt werden. Im Modul 4 der Begleitforschung,
          in Zusammenarbeit mit dem Projekt “Privacy Icons” der Forschungsgruppe
          Digitale Selbstbestimmung, wurde zu diesem Zweck ein Open-Source
          Iconset entwickelt, das zur freien Nutzung und Abänderung freigegeben
          wurde. Das Iconset richtet sich an unterschiedlichste Akteure.
          Einerseits können datenschutzrechtliche Informationspflichten mithilfe
          der Icons effektiv umgesetzt werden und damit dem Transparenzprinzip
          Rechnung tragen. Darüber hinaus ist eine Nutzung der Icons zur
          Visualisierung verschiedenster Sachverhalte im Gebäude- und Quartiers
          Bereich denkbar, etwa zur verständlichen Aufbereitung von
          Forschungsergebnissen oder Erklärung digitaler Anwendungen. Das
          Iconset besteht aus über 150 Icons verschiedener Kategorien (z.B. Data
          and Identifiers, Purposes, Actors and Technical Means). Es wird
          ergänzt durch ein Set von Gebäudegrafiken und anderen
          Visualisierungskomponenten, die gemeinsam einen Baukasten ergeben, der
          eine Betrachtung aus rechtlicher, ökonomisch-ökologischer sowie
          technischer Perspektive erlaubt und von der Visualisierung eines
          ganzen Projekts bis hin zur konkreten Anwendung, etwa auf einem
          User-Interface verwendet werden kann."""
    )
    explanTextToRender = """<p>
            <a href="https://github.com/Privacy-Icons/Privacy-Icons">Icons</a>
          </p>
          <div class="row">
        <div class="col-lg-9">
          {% load static%}<img src="{% static 'img/iconsOverview.png' %}" alt="image_icons">
          </div>
        </div>
      """

    explanationText += Template(explanTextToRender).render(Context({}))

    context = {
        "focusBorder": "legal",
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Icons und Visualisierung"),
        "explanaitionText": explanationText.replace("\n", ""),
        "leftColumn": "partials/icons_left_column.html",
        "rightColumn": "partials/icons_right_column.html",
    }

    return render(request, "pages/detailsPage.html", context)


def criteriaCatalog(request):
    """Call render function for criteria catalog page."""
    criteriaCatalogObjs = CriteriaCatalog.objects.all().order_by("id")
    explanText = _("Worum geht es?<br><br>")
    explanText += _(
        "Aufgrund der engen Verknüpfung von Gebäude und Gebäudenutzenden gehen Digitalisierungsprozesse oft Hand in Hand mit der Verarbeitung personenbezogener Daten. Für die Verarbeitung personenbezogener Daten sieht die Datenschutzgrundverordnung (DSGVO) strenge Vorgaben vor, die für die Verarbeitung Verantwortliche zu beachten haben. Darunter fallen insbesondere Transparenz- und Rechenschaftspflichten, sowie das grundsätzliche Erfordernis einer Rechtsgrundlage.<br><br>"
    )
    explanText += _("Wie funktioniert das?<br><br>")
    explanText += _(
        "<p>Der folgende Kriterienkatalog umfasst sämtliche Pflichten aus der DSGVO in Form von “Kriterien” und “Anforderungen”, die für die jeweilige Zweckkategorie konkretisiert werden. Der Katalog teilt die Anforderungen der DSGVO in 14 “Themen” auf und lässt sich über ein Klappsystem sowie über das Suchfeld gezielt durchsuchen.</p>"
    )
    explanText += _(
        "<ul><li>Er dient einerseits dazu, Datenschutzrecht und die dahinter liegenden Ziele und Wertungen für die LeserInnen verständlich zu machen.</li><li>Andererseits können die “Anforderungen” als Checkliste begriffen werden, die Verantwortliche vor der Verarbeitung personenbezogener Daten beachten sollten.</li></ul><br>"
    )
    explanText += _(
        "<p>Anmerkung: Der Kriterienkatalog wird aktuell noch laufend ergänzt und bearbeitet. Bei allen Empfehlungen handelt es sich um typisierte Beispiele, die im Lichte des konkreten Anwendungsfalls betrachtet und umgesetzt werden müssen.</p>"
    )
    # explanTextRendered = Template(explanText).render(Context({}))
    context = {
        "pathToImage": "img/componentList/circle-icon.svg",
        "heading": _("Kriterienkatalog"),
        "showMorePresent": False,
        "explanaitionText": explanText,
        "boxes": [
            {
                "pathToTemplate": "criteria_catalog/criteria_catalog_overview_box.html",
                "objectToRender": criteriaCatalogObj,
            }
            for criteriaCatalogObj in criteriaCatalogObjs
        ],
        "focusBorder": "legal",
        "showMorePresent": True,
    }

    return render(request, "pages/criteria_catalog.html", context)


def impressum(request):
    """Call render function for impressum page."""
    return render(request, "pages/impressum.html")


def showImage(request, idOfEnvironmentalImpactObj):
    """Call render function for show image page."""
    environmentalObjToReturn = EnvironmentalImpact.objects.get(
        id=idOfEnvironmentalImpactObj
    )
    context = {
        "imageInBackButton": "img/componentList/caret-left.svg",
        "imageName": environmentalObjToReturn.image,
        "backLink": "environmentalIntegrityBox",
        "backLinkParam": idOfEnvironmentalImpactObj,
        "backLinkText": environmentalObjToReturn.project_name,
        "focusBorder": "ecological",
    }
    return render(request, "pages/showImage.html", context)
