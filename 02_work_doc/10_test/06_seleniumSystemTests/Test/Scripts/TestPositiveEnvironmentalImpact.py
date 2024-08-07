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
    NegativeEnvironmentalImpacts, )
from Src.PageObject.Pages.PositiveEnvironmentalIntegrity import (
    PositiveEnvironmentalIntegrity, )
from Src.PageObject.Pages.DetailsPage import DetailsPage


class TestPositiveEnvironmentalImpact(WebDriverSetup):

    def testDetailsPage(self):
        """Test if it is possible to go onto the newly styled"""
        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityPositiv")

        time.sleep(1)

        # Check the structure of the page
        positiveEnvironmentalIntegrityObj = PositiveEnvironmentalIntegrity(
            self.driver)
        
        self.checkNavBar("ecological")

        contentDiv = positiveEnvironmentalIntegrityObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        # check if 2 divs are present in the content container
        divDescription = (
            positiveEnvironmentalIntegrityObj.getDescendantsByClass(
                contentDiv, "descriptionContainer"))
        self.assertEqual(len(divDescription), 1)
        divFourCardsContainer = (
            positiveEnvironmentalIntegrityObj.getDescendantsByClass(
                contentDiv, "boxes"))
        self.assertEqual(len(divFourCardsContainer), 1)

        boxesInBoxContainer = positiveEnvironmentalIntegrityObj.getDescendantsByClass(divFourCardsContainer[0], "box")
        self.assertGreaterEqual(len(boxesInBoxContainer), 3)
        
        # check if alt-text is present for images:
        for box in boxesInBoxContainer:
            logoImage = positiveEnvironmentalIntegrityObj.getDescendantsByTagName(box, "img")
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
            ))

        detailsPageObj = DetailsPage(self.driver)
        # check if the backlink is present:
        contentDiv = detailsPageObj.getContentDiv()
        self.assertIsNotNone(contentDiv)
        

        divsInsideContentDiv = detailsPageObj.getDescendantsByClass(
            contentDiv, "secondaryNavbar")

        # check if the backlink is present:
        backLink = detailsPageObj.getDescendantsByTagName(
            divsInsideContentDiv[0], "a")

        self.assertTrue("/pages/environmentalIntegrityPositiv" in
                        backLink[0].get_attribute("href"))

        # check if the second-div has the class border-ecological:
        detailsContentContainer = positiveEnvironmentalIntegrityObj.getDescendantsByClass(contentDiv, "border-ecological")
        self.assertEqual(len(detailsContentContainer), 1)
        # check if 2 divs are present in the second div container:
        divDescription = detailsPageObj.getDescendantsByClass(
            detailsContentContainer[0], "column__right")

        # check if the showMore-link is present:
        showMoreLink = detailsPageObj.getDescendantsByTagName(
            divDescription[0], "a")
        if self.getLanguage() == "de":
            for link in showMoreLink:
                self.assertTrue("Zeige mehr" in link.get_attribute("data-collapsed-text"))
        else:
            for link in showMoreLink:
                self.assertTrue("Show more" in link.get_attribute("data-collapsed-text"))

        leftColumn = detailsPageObj.getDescendantsByClass(contentDiv, "column__left")
        # test if the image is clickable and leads to a new page:
        image = detailsPageObj.getDescendantsByTagName(leftColumn[0],
                                                       "img")
        self.scrollElementIntoViewAndClickIt(image[0])

        self.assertTrue(re.search(
            r"/showImage",
            self.driver.current_url,
        ))

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
            ))
