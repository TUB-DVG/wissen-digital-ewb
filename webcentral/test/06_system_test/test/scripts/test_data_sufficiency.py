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
from Src.PageObject.Pages.DataSufficiency import DataSufficiency


class TestDataSufficiency(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testPageStructure(self):
        """Test the structure of the Components-List Page"""
        self.driver.get(os.environ["siteUnderTest"] + "/pages/dataSufficiency")

        time.sleep(1)

        # Check the structure of the page
        dataSufficiencyObj = DataSufficiency(self.driver)

        contentDiv = dataSufficiencyObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        # check if 2 divs are present in the content container
        divDescription = dataSufficiencyObj.getDescendantsByClass(
            contentDiv, "descriptionContainer"
        )
        self.assertEqual(len(divDescription), 1)
        divFourCardsContainer = dataSufficiencyObj.getDescendantsByClass(
            contentDiv, "box "
        )
        self.assertGreaterEqual(len(divFourCardsContainer), 0)

    def testDotsPresentWhenCollapsed(self):
        """Test if three dots are present at the end of the collapsed component.
        The three dots indicate, that there is more text to be shown when clicking
        on `show more`
        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/dataSufficiency")
        dataSufficiencyObj = DataSufficiency(self.driver)

        boxesOnSite = dataSufficiencyObj.getBoxes()
        randomBox = choice(boxesOnSite)

        allFirstPartsOfCollapsables = dataSufficiencyObj.getAllCollapsableFirstParts()
        for firstPartOfCollapsable in allFirstPartsOfCollapsables:
            parentDiv = dataSufficiencyObj.getFirstAncestorByTagName(
                firstPartOfCollapsable, "div"
            )
            if "Show more" in parentDiv.text or "Zeige mehr" in parentDiv.text:
                nextSibling = dataSufficiencyObj.getFollowingSiblingOfTagName(
                    firstPartOfCollapsable, "div"
                )
                if "collapse" in nexSibling.get_attribute("class"):
                    self.assertEqual(
                        firstPartOfCollapsable.text[-3:],
                        "...",
                        "The last 3 characters should be dots, when the element is collapsed.",
                    )
                elif "show" in nextSibling.get_attribute("class"):
                    self.assertNotEqual(
                        firstPartOfCollapsable.text[-3:],
                        "...",
                        "The last 3 characters should be dots, when the element is collapsed.",
                    )
