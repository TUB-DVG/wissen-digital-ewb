"""Clicks though all Sites and tests if they load.

This module acts as system test of for the whole webcentral-page.
It clicks through all pages and checks if they are accessible.
"""

import pdb
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
from selenium.webdriver import ActionChains

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar


class TestClickThroughSites(WebDriverSetup):
    """ """

    def testClickNavbar(self) -> None:
        """ """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list")
        self.driver.set_page_load_timeout(30)

        navBar = NavBar(self.driver)

        LogoLink = navBar.getLogo()
        self.assertIsNotNone(
            LogoLink,
            "The Logo, which is a link at the same time is not shown! ",
        )

        LogoLink.click()

        self.assertEqual(
            "Wissensplattform - Digitalisierung Energiewendebauen",
            self.driver.title,
            "After clicking Logo, Browser should be redirected to Startpage, but was not!",
        )

    def testHoverOverDataAndClickWeatherdata(self):
        """Tests if a Sub-menu is displayed, when hovering over Data-NavBar-item."""
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list")
        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).perform()
        time.sleep(1)
        weatherDataItem = navBar.getWeatherDataItem()

        weatherDataItem.click()

        self.assertEqual(
            "Überblick über die Wetterdaten-Services",
            self.driver.title,
            "Page should be weatherdata-page, but it is not!",
        )

    def testHoverOverDataAndClickLastprofiles(self):
        """Tests if a Sub-menu is displayed, when hovering over Data-NavBar-item."""
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list")
        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).perform()
        time.sleep(1)

        lastprofileItem = navBar.getLastProfileItem()
        lastprofileItem.click()

        self.assertEqual(
            "Überblick über die Lastprofil Approximation",
            self.driver.title,
            "Page should be lastprofile-page, but it is not!",
        )
