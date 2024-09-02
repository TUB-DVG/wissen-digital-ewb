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

from src.page_obj.pages.cookie_banner import CookieBanner
from src.page_obj.pages.footer import Footer
from src.test_base.webdriver_setup import WebDriverSetup
from src.page_obj.pages.navbar import NavBar
from src.page_obj.pages.comparison_page_section import ComparisonPageSection
from src.page_obj.pages.user_integration_page import UserIntegrationPage
from src.page_obj.pages.overview_page_section import OverviewPageSection
from src.page_obj.pages.details_page import DetailsPage


class TestUserIntegration(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    # def testLinksToUserEngagementSite(self):
    #     """Test if the Components-List Page exists and is accessible via url and navbar"""
    #
    #     self.driver.get(os.environ["siteUnderTest"])
    #     navbar = NavBar(self.driver)
    #
    #     languageName = self.getLanguage()
    #     userEngagementLinks = navbar.returnUserEngagementLink()
    #     self.assertEqual(len(userEngagementLinks), 2)
    #     for userEngagementLink in userEngagementLinks:
    #         # breakpoint()
    #         if userEngagementLink.get_attribute("class") == "dropdown-item":
    #             navbarActivateDropdownButton = (
    #                 navbar.getOperationalDropdownButton())
    #             navbarActivateDropdownButton.click()
    #             # breakpoint()
    #             if languageName == "de":
    #                 self.assertTrue(
    #                     "Nutzendenintegration" in userEngagementLink.text)
    #             else:
    #                 self.assertTrue(
    #                     "User integration" in userEngagementLink.text)
    #
    #
    #     userEngagementLinks[1].click()
    #     self.assertTrue("User integration" in self.driver.title
    #                     or "Nutzendenintegration" in self.driver.title)
    #     self.driver.back()
    #     userEngagementLinks = navbar.returnUserEngagementLink()
    #     navbarActivateDropdownButton = navbar.getOperationalDropdownButton()
    #     navbarActivateDropdownButton.click()
    #     userEngagementLinks[0].click()
    #     self.assertTrue("User integration" in self.driver.title
    #                     or "Nutzendenintegration" in self.driver.title)
    #     self.driver.back()
    #
    def testUserEngagementPage(self):
        """Test if a description-container is present"""

        self.driver.get(os.environ["siteUnderTest"] + "/pages/userEngagement")
        self.checkNavBar("operational")

    def testOverviewText(self):
        """Test the overview text section.

        Test if the overview page section is translated. Test if the links work.

        """

        self.driver.get(os.environ["siteUnderTest"] + "/pages/userEngagement")
        self.overviewPageSectionObj = OverviewPageSection(self.driver)
        self.detailsPage = DetailsPage(self.driver)
        self.checkInGermanAndEnglish(
            self._testHeading,
            {
                "de": "Methoden der Nutzendenintegration",
                "en": "Methods of user integration",
            },
        )

        aTagsInOverviewText = self.overviewPageSectionObj.getLinks()

        aText = {
            "de": [
                "Teilnehmende Beobachtung",
                "Einzel-Interview",
                "Gruppen-Interview/Fokusgruppe",
                "Personas",
                "A/B-Test",
                "Prototyping",
                "Cognitive Walkthrough",
                "Styleguide",
                "Lautes Denken",
                "Eyetracking",
                "Heuristische Evaluation",
                "Usability-Befragung",
            ],
            "en": [
                "Participant observation",
                "Individual interview",
                "Group interview/focus group",
                "Personas",
                "A/B testing",
                "Prototyping",
                "Cognitive Walkthrough",
                "Style guide",
                "Thinking out loud",
                "Eye tracking",
                "Heuristic evaluation",
                "Usability survey",
            ],
        }

        for aTagIndex, aTag in enumerate(aTagsInOverviewText):

            self.checkInGermanAndEnglish(
                self._testLinks,
                {"de": aText["de"][aTagIndex], "en": aText["en"][aTagIndex]},
            )

    def _testHeading(self, expectedValue):
        """ """
        headingOfOverviewSection = self.overviewPageSectionObj.getHeading()
        self.assertEqual(headingOfOverviewSection.text, expectedValue)

    def _testLinks(self, expectedValue):
        """Test the links in the overview text of user integratio overview site"""

        linkToDetailsSite = self.overviewPageSectionObj.getLinkFromText(
            expectedValue
        )
        self.scrollElementIntoViewAndClickIt(linkToDetailsSite)
        self.assertEqual(self.driver.title, expectedValue)
        allATagsInContentContainer = (
            self.detailsPage.getATagsInContentContainer()
        )
        self.scrollElementIntoViewAndClickIt(choice(allATagsInContentContainer))
        self.assertTrue("Error" not in self.driver.title)
        self.driver.back()
        self.driver.back()
