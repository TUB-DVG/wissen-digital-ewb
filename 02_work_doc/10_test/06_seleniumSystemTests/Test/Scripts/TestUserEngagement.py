""" Testing strategy for the UserEngagement Page:
    1. Test if the UserEngagement Page exists and is accessible via url and navbar from startpage (testLinksToUserEngagementSite).

"""

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
from Src.PageObject.Pages.ComponentListPage import ComponentListPage
from Src.PageObject.Pages.ComparisonPageSection import ComparisonPageSection
from Src.PageObject.Pages.UserEngagementPage import UserEngagmentPage

class TestUserEngagement(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testLinksToUserEngagementSite(self):
        """Test if the Components-List Page exists and is accessible via url and navbar"""

        self.driver.get(os.environ["siteUnderTest"])
        navbar = NavBar(self.driver)

        languageName = self.getLanguage()
        userEngagementLinks = navbar.returnUserEngagementLink()
        self.assertEqual(len(userEngagementLinks), 2)
        for userEngagementLink in userEngagementLinks:
            # breakpoint()
            if userEngagementLink.get_attribute("class") == "dropdown-item":
                navbarActivateDropdownButton = (
                    navbar.getOperationalDropdownButton())
                navbarActivateDropdownButton.click()
                # breakpoint()
                if languageName == "de":
                    self.assertTrue(
                        "Nutzendenintegration" in userEngagementLink.text)
                else:
                    self.assertTrue(
                        "User integration" in userEngagementLink.text)

            # userEngagementLink.click()
            # self.assertTrue("User Engagement" in self.driver.title
            #                 or "Nutzendenintegration" in self.driver.title)
            # self.driver.back()
            # userEngagementLinks = navbar.returnUserEngagementLink()

        userEngagementLinks[1].click()
        self.assertTrue("User integration" in self.driver.title
                        or "Nutzendenintegration" in self.driver.title)
        self.driver.back()
        userEngagementLinks = navbar.returnUserEngagementLink()
        navbarActivateDropdownButton = navbar.getOperationalDropdownButton()
        navbarActivateDropdownButton.click()
        userEngagementLinks[0].click()
        self.assertTrue("User integration" in self.driver.title
                        or "Nutzendenintegration" in self.driver.title)
        self.driver.back()

    def testUserEngagementPage(self):
        """Test if a description-container is present"""

        self.driver.get(os.environ["siteUnderTest"] + "/userEngagement")
        
        self.checkNavBar("operational")

        # userEngagementPage = UserEngagmentPage(self.driver)
        # self.assertTrue(userEngagementPage.isDescriptionContainerPresent())
