import os
from random import choice
import sys
import time
import re

sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from Src.PageObject.Pages.cookieBanner import CookieBanner
from Src.PageObject.Pages.Footer import Footer
from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.NegativeEnvironmentalImpacts import (
    NegativeEnvironmentalImpacts,
)
from Src.PageObject.Pages.PositiveEnvironmentalIntegrity import (
    PositiveEnvironmentalIntegrity,
)
from Src.PageObject.Pages.DetailsPage import DetailsPage


class TestPositiveEnvironmentalImpact(WebDriverSetup):

    def testDetailsPage(self):
        """Test if it is possible to go onto the newly styled"""
        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/environmentalIntegrityPositiv"
        )

        time.sleep(1)

        # Check the structure of the page
        positiveEnvironmentalIntegrityObj = PositiveEnvironmentalIntegrity(self.driver)

        self.checkNavBar("ecological")

        contentDiv = positiveEnvironmentalIntegrityObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        # check if 2 divs are present in the content container
        divDescription = positiveEnvironmentalIntegrityObj.getDescendantsByClass(
            contentDiv, "descriptionContainer"
        )
        self.assertEqual(len(divDescription), 1)
        divFourCardsContainer = positiveEnvironmentalIntegrityObj.getDescendantsByClass(
            contentDiv, "boxes"
        )
        self.assertEqual(len(divFourCardsContainer), 1)

        boxesInBoxContainer = positiveEnvironmentalIntegrityObj.getDescendantsByClass(
            divFourCardsContainer[0], "box"
        )
        self.assertGreaterEqual(len(boxesInBoxContainer), 3)

        # check if alt-text is present for images:
        for box in boxesInBoxContainer:
            logoImage = positiveEnvironmentalIntegrityObj.getDescendantsByTagName(
                box, "img"
            )
            self.assertEqual(len(logoImage), 1)
            self.assertTrue(logoImage[0].text == "")

        # click on one of the box containers:
        randomBox = choice(boxesInBoxContainer)
        randomBox.click()

        # check if the user is now on the details page:
        self.assertTrue(
            re.search(
                r"/pages/environmentalIntegrityPositiv/[0-9]+",
                self.driver.current_url,
            )
        )

        detailsPageObj = DetailsPage(self.driver)
        # check if the backlink is present:
        contentDiv = detailsPageObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        divsInsideContentDiv = detailsPageObj.getDescendantsByClass(
            contentDiv, "secondaryNavbar"
        )

        # check if the backlink is present:
        backLink = detailsPageObj.getDescendantsByTagName(divsInsideContentDiv[0], "a")

        self.assertTrue(
            "/pages/environmentalIntegrityPositiv" in backLink[0].get_attribute("href")
        )

        # check if the second-div has the class border-ecological:
        detailsContentContainer = (
            positiveEnvironmentalIntegrityObj.getDescendantsByClass(
                contentDiv, "border-ecological"
            )
        )
        self.assertEqual(len(detailsContentContainer), 1)
        # check if 2 divs are present in the second div container:
        divDescription = detailsPageObj.getDescendantsByClass(
            detailsContentContainer[0], "column__right"
        )

        # check if the showMore-link is present:
        showMoreLink = detailsPageObj.getDescendantsByTagName(divDescription[0], "a")
        if self.getLanguage() == "de":
            for link in showMoreLink:
                self.assertTrue(
                    "Zeige mehr" in link.get_attribute("data-collapsed-text")
                )
        else:
            for link in showMoreLink:
                self.assertTrue(
                    "Show more" in link.get_attribute("data-collapsed-text")
                )

        # check if literature is present:
        literatureDiv = detailsPageObj.getDescendantsByClass(
            divDescription, "literatureHeading"
        )
        self.assertEqual(len(literatureDiv), 1)
        self.assertTrue(
            "Weiterführende Literatur und Hinweise" in literatureDiv[0].text
        )

        leftColumn = detailsPageObj.getDescendantsByClass(contentDiv, "column__left")
        # test if the image is clickable and leads to a new page:
        image = detailsPageObj.getDescendantsByTagName(leftColumn[0], "img")
        self.scrollElementIntoViewAndClickIt(image[0])

        self.assertTrue(
            re.search(
                r"/showImage",
                self.driver.current_url,
            )
        )

        # check if a backlink is present and has green color:
        backLink = detailsPageObj.getBackLink()
        colorOfbackLink = backLink.value_of_css_property("color")
        self.assertTrue(self.ECOLOGICAL_COLOR in colorOfbackLink)

        backLink.click()
        # check if the user is now on the details page:
        self.assertTrue(
            re.search(
                r"/pages/environmentalIntegrityPositiv/[0-9]+",
                self.driver.current_url,
            )
        )

    def testLinksInText(self):
        """Test if the links in the text of the details page lead to the
        right location.
        """

        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/environmentalIntegrityPositiv"
        )
        envImpactObj = PositiveEnvironmentalIntegrity(self.driver)

        # get all boxes:
        boxesOnEnvImpactOverviewPage = envImpactObj.getBoxes()
        self._removeCookieBanner()
        for box in boxesOnEnvImpactOverviewPage:
            textContent = box.text
            if "FeBOp-MFH" in textContent:
                aDescadents = envImpactObj.getDescendantsByClass(box, "box__content")
                self.scrollElementIntoViewAndClickIt(aDescadents[0])

                break
        self.assertTrue(
            "FeBOp-MFH" in self.driver.title,
            "Didnt find box for FeBOp-MFH-project",
        )

        detailsPageObj = DetailsPage(self.driver)

        rightColumn = detailsPageObj.getRightColumn()
        linksInRightColumn = detailsPageObj.getDescendantsByTagName(rightColumn, "a")
        self.assertEqual(len(linksInRightColumn), 3)

        for link in linksInRightColumn:
            if "evaluation" in link.get_attribute("href"):
                self.scrollElementIntoViewAndClickIt(link)
                break

        evaluationDiv = envImpactObj.getEvaluationDiv()
        linksInEvaluation = envImpactObj.getDescendantsByTagName(evaluationDiv, "a")

        breakpoint()
        # first link should point to components:
        self.assertTrue("components" in linksInEvaluation[0].get_attribute("href"))
        self.assertTrue("Hilfestellung" in linksInEvaluation[0].text)

        # first link should point to components:
        self.assertTrue("dataProcessing" in linksInRightColumn[1].get_attribute("href"))
        self.assertTrue("Kennwerte" in linksInRightColumn[1].text)

        self.scrollElementIntoViewAndClickIt(linksInEvaluation[0])
        self.assertTrue("components" in self.driver.current_url)
        self.assertTrue(
            "Komponentenliste" in self.driver.title
            or "Componentent list" in self.driver.title
        )

        self.driver.back()
        evaluationDiv = envImpactObj.getEvaluationDiv()
        linksInEvaluation = envImpactObj.getDescendantsByTagName(evaluationDiv, "a")

        self.scrollElementIntoViewAndClickIt(linksInEvaluation[1])
        self.assertTrue("dataProcessing" in self.driver.current_url)
        self.assertTrue(
            "Aufwände für Datenverarbeitungsprozesse" in self.driver.title
            or "Expenses for data processing processes" in self.driver.title
        )
