import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.BusinessModels import BusinessModels


class TestBusinessModels(WebDriverSetup):
    """ """

    def _checkTranslationOfHeading(self, transDict):
        """ """
        headingContainer = self.businessModelObj.getHeadingContainer()

        introContentContainer = self.businessModelObj.getDescriptionContainer()

        iconinHeadingContainer = self.businessModelObj.getDescendantsByTagName(
            headingContainer, "img")

        self.assertEqual(len(iconinHeadingContainer), 1)
        self.assertTrue("circle-icon.svg" in
                        iconinHeadingContainer[0].get_attribute("src"))
        self.checkIfSvgIsDisplayed(iconinHeadingContainer[0])

        self.headingText = self.businessModelObj.getDescendantsByTagName(
            headingContainer, "p")[0]

        self.introContentText = self.businessModelObj.getDescendantsByTagName(
            introContentContainer, "p")[0]
        self.assertEqual(transDict["heading"], self.headingText.text)
        self.assertEqual(transDict["introText"], self.introContentText.text)

    def testStructureOfOverviewPage(self):
        """Test if the content is present and if all images are loaded"""

        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/businessModels"
        )  # first test if a heading and a introduction text is present:
        self.checkNavBar("operational")

        self.businessModelObj = BusinessModels(self.driver)

        translationDict = {
            "en": {
                "heading":
                "Business models",
                "introText":
                "The focus in a research project often lies in an innovative product, a digital application, or a new software. In most cases, the development ends with the creation of the prototype in the research project. However, it is desirable to translate it into a business model for successful development. The information found here is intended to help support the development of business models and overcome challenges that arise. For this purpose, challenges have been collected, clustered, and initial solution approaches have been discussed from previous research projects in interviews and workshops. In addition, a collection of tools has been created to support the development from prototype to business model.",
            },
            "de": {
                "heading":
                "Geschäftsmodelle",
                "introText":
                "Der Fokus in einem Forschungsprojekt liegt häufig in einem innovativen Produkt, einer digitalen Anwendung oder auch einer neuen Software. Bei der Erstellung des Prototyps endet in den meisten Fällen die Entwicklung im Forschungsprojekt. Bei einer erfolgreichen Entwicklung ist die Übersetzung in ein Geschäftsmodell jedoch wünschenswert. Die hier aufzufindenden Informationen sollen dabei helfen, die Entwicklung von Geschäftsmodellen zu unterstützen und auftretende Herausforderungen zu meistern. Dafür wurden aus bisherigen Forschungsprojekte in Interviews und Workshops Herausforderungen gesammelt, geclustert und erste Lösungsansätze diskutiert. Daneben wurde auch eine Sammlung von Tools erstellt, die bei der Entwicklung vom Prototyp zum Geschäftsmodell unterstützen.",
            },
        }

        self.checkInGermanAndEnglish(self._checkTranslationOfHeading,
                                     translationDict)
