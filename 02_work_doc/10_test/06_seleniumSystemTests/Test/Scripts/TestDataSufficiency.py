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
from Src.PageObject.Pages.DataSufficiency import DataSufficiency


class TestComponentsList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testPageStructure(self):
        """Test the structure of the Components-List Page"""
        self.driver.get(os.environ["siteUnderTest"] + "/pages/dataSufficiency")

        time.sleep(1)

        # Check the structure of the page
        dataSufficiencyObj = DataSufficiency(driver)

        contentDiv = dataSufficiencyObj.getContentDiv()
        self.assertIsNotNone(contentDiv)

        # check if 2 divs are present in the content container
        divDescription = dataSufficiencyObj.getDescendantsByClass(
            contentDiv, "descriptionContainer")
        self.assertEqual(len(divDescription), 1)
        divFourCardsContainer = dataSufficiencyObj.getDescendantsByClass(
            contentDiv, "fourCardsContainer")
        self.assertEqual(len(divFourCardsContainer), 1)
