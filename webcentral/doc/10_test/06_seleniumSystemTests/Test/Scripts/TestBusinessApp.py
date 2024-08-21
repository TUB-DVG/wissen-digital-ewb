"""Test the Userinterface of Business-Application-Page

This class is part of the Selenium-Test of Webcentral. 
It tests the Business-Application-Page, which is accessed when browsing to
https://wissen-digital-ewb.de/tool_list/buisnessApps/.

"""
import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from selenium import (
    webdriver, )
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AboutPage import AboutPage
from Src.PageObject.Pages.BusinessAppPage import BusinessAppPage
from Src.PageObject.Pages.SearchPage import SearchPage


class TestBusinessAppPage(WebDriverSetup):
    """ """

    def testSearchBar(self):
        """Test if the Search-Bar looks and acts as expected."""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/tool_list/buisnessApps/")

        searchBarObj = SearchPage(self.driver)

    def testCardsPresentOnVisit(self):
        """Test if the number of Business-Apps, shown in Cards is greater than 0."""

        self.driver.get(os.environ["siteUnderTest"] +
                        "/tool_list/buisnessApps/")
        businessAppObj = BusinessAppPage(self.driver)

        self.assertGreater(
            len(businessAppObj.getCards()),
            0,
            "The Number of Business-Apps should be greater than 0...",
        )

    def testSearchField(self):
        """Enter 'BIEC' into the searchField and check if 2 or more results are present."""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/tool_list/buisnessApps/")
        businessAppObj = BusinessAppPage(self.driver)

        searchInput = businessAppObj.getSearchField()
        searchInput.send_keys("BIEC")
        searchInput.send_keys(Keys.RETURN)

        time.sleep(1)
        self.assertEqual(
            len(businessAppObj.getCards()),
            2,
            "The Number of Results for 'BIEC' should be 2...",
        )

    def testIfDetailSiteIsShown(self):
        """Test, if on click on a Card, the Detail-Site is displayed."""

        self.driver.get(os.environ["siteUnderTest"] +
                        "/tool_list/buisnessApps/")
        businessAppObj = BusinessAppPage(self.driver)

        randomCard = random.choice(businessAppObj.getCards())
        cardName = randomCard.text.split("\n")[0]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            randomCard,
        )
        time.sleep(1)
        randomCard.click()

        self.assertEqual(
            self.driver.title,
            cardName,
            f"After clicking on '{cardName}'-card, the detail page of the card should appear...",
        )

    def testTagOnDetailPage(self):
        """ """
        self.driver.get(os.environ["siteUnderTest"] +
                        "/tool_list/buisnessApps/")
        businessAppObj = BusinessAppPage(self.driver)

        randomCard = random.choice(businessAppObj.getCards())
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            randomCard,
        )

        time.sleep(2)
        randomCard.click()

        tagElements = businessAppObj.getTagsOnDetailPage()
        for tag in tagElements:
            if tag.text == "":
                tagElements.remove(tag)

        randomTag = random.choice(tagElements)

        tagText = randomTag.text
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            randomTag,
        )
        time.sleep(1)

        randomTag.click()

        time.sleep(1)
        tagResult = businessAppObj.getSearchResultFilter(tagText)

        self.assertFalse(
            tagResult is None,
            f"Tag-Filter {tagText}, should be present on Site, but its not!",
        )
