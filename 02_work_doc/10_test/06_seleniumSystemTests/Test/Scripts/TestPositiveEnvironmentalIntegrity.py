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
from Src.PageObject.pages.DetailsPage import DetailsPage


class TestPositiveEnvironmentalIntegrity(WebDriverSetup):

    def testDetailsPage(self):
        """Test if it is possible to go onto the newly styled"""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/pages/environmentalIntegrityPositiv")

        time.sleep(1)

        # Check the structure of the page
        positiveEnvironmentalIntegrityObj = PositiveEnvironmentalIntegrity(
            self.driver)

        contentDiv = positiveEnvironmentalIntegrityObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        # check if 2 divs are present in the content container
        divDescription = (
            positiveEnvironmentalIntegrityObj.getDescendantsByClass(
                contentDiv, "descriptionContainer"))
        self.assertEqual(len(divDescription), 1)
        divFourCardsContainer = (
            positiveEnvironmentalIntegrityObj.getDescendantsByClass(
                contentDiv, "fourCardsContainer"))
        self.assertEqual(len(divFourCardsContainer), 1)

        # click on one of the box containers:
        randomBox = choice(divFourCardsContainer)
        randomBox.click()

        # check if the user is now on the details page:
        self.assertTrue(
            re.search(
                r"/pages/environmentalIntegrityPositiv/[0-3]+",
                self.driver.current_url,
            ))

        detailsPageObj = DetailsPage(self.driver)
        # check if the backlink is present:
        contentDiv = detailsPageObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        divsInsideContentDiv = detailsPageObj.getDescendantsByTag(
            contentDiv, "div")
        self.assertEqual(len(divsInsideContentDiv), 2)

        # check if the backlink is present:
        backLink = detailsPageObj.getDescendantsByTagName(
            divsInsideContentDiv[0], "a")

        self.assertTrue("/pages/environmentalIntegrityPositiv" in
                        backLink[0].get_attribute("href"))

        # check if the second-div has the class border-ecological:
        self.assertTrue("border-ecological" in
                        divsInsideContentDiv[1].get_attribute("class"))

        # check if 2 divs are present in the second div container:
        divDescription = detailsPageObj.getDescendantsByTag(
            divsInsideContentDiv[1], "div")

        self.assertEqual(len(divDescription), 2)
