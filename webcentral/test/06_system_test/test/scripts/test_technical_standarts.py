"""Test the Technical Standarts page

"""

import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from selenium import (
    webdriver,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.TechnicalStandartsPage import TechnicalStandartsPage


class TestTechnicalStandarts(WebDriverSetup):
    """Tests the 'Lastapproximation'-Tab"""

    def testclickLinks(self):
        """Test if the link"""
        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/")
        self.checkNavBar("technical")

        technicalStandartsPageObj = TechnicalStandartsPage(self.driver)
        linkToNorms = technicalStandartsPageObj.getNormsLink()

        self.driver.execute_script(
            "arguments[0].scrollIntoView();", linkToNorms
        )
        time.sleep(1)
        linkToNorms.click()

        time.sleep(1)
        self.checkNavBar("technical")
        self.checkPageTitle(
            "Überblick über technische Standards - Normen",
            "Overview of technical standards - Norms",
        )

        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/")
        time.sleep(1)
        linkToProtocols = technicalStandartsPageObj.getProtocolsLink()
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", linkToProtocols
        )
        time.sleep(1)
        linkToProtocols.click()

        time.sleep(1)
        self.checkNavBar("technical")
        self.checkPageTitle(
            "Überblick über technische Standards - Protokolle",
            "Overview of technical standards - Protocols",
        )
