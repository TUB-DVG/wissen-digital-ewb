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


class TestUserEngagement(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testLinksToUserEngagementSite(self):
        """Test if the Components-List Page exists and is accessible via url and navbar"""

        self.driver.get(os.environ["siteUnderTest"])
        navbar = NavBar(self.driver)

        languageName = self.getLanguage()
        userEngagementLink = navbar.returnUserEngagementLink()
        self.assertEqual(len(userEngagementLink), 2)
        if languageName == "Deutsch":
            self.assertTrue("Nutzendenintegration" in userEngagementLink.text)
        else:
            self.assertTrue("User Engagement" in userEngagementLink.text)

        userEngagementLink.click()

        # check if the new page title includes the word "User Engagement" or "Nutzendenintegration"
        self.assertTrue("User Engagement" in self.driver.title
                        or "Nutzendenintegration" in self.driver.title)
