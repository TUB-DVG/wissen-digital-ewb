"""Tests the `Digitale Werkzeuge` (engl. digital tools)-Tab

This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

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
from selenium.webdriver import ActionChains

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.cookieBanner import CookieBanner

class TestDigitalToolsPage(WebDriverSetup):
    """
    
    """
    def testNavigateToDigitalToolsPage(self) -> None:
        """Navigates from norm list to digital-tools-tab.

        """
        print(os.environ["siteUnderTest"])
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")

        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()
        toolListItem = navBar.getNavToolList()
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).click(toolListItem).perform()
        
        time.sleep(1)
        
        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

    def testSearchField(self) -> None:
        """Tests the Search Function in `Digitale Anwendungen`
        
        """
        self.openToolList()

        toolListPage = ToolListPage(self.driver)
        # breakpoint()
        searchFieldElement = toolListPage.getSearchInputElement()
        if searchFieldElement is None:
            self.assertTrue(False)
            return
        listOfToolItems = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listOfToolItems),
            12,
            "Number of Tool Items should be 12 without search-filter!",
        )
        searchFieldElement.send_keys("Ansys")
        time.sleep(1)
        searchFieldElement.send_keys(Keys.RETURN)
        time.sleep(1)
        listOfToolItemsAfterReturn = toolListPage.getListOfToolItems()

        self.assertEqual(
            len(listOfToolItemsAfterReturn),
            1,
            "Number of Tool Items should be one for Search-String 'Ansys'!",
        )
        
        time.sleep(1)
        searchStrBox = toolListPage.getSearchStringButton("Ansys")
        self.assertIsInstance(
            searchStrBox, 
            WebElement, 
            "Search-String Button is not present!",
        )

        searchStringBoxX = toolListPage.getCloseOnSearchStrButton(searchStrBox)
        self.assertIsInstance(
            searchStrBox, 
            WebElement, 
            "Search-String-X Button is not present!",
        )

        # breakpoint()
        toolListPage.getXOfSearchFilter().click()
        
        time.sleep(1)
        listToolItemsAfterRmvdSearch = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listToolItemsAfterRmvdSearch),
            12,
            "After removing search-string 'Ansys', number of tool-items should be 12!",
        )

        searchFieldElement = toolListPage.getSearchInputElement()
        searchFieldElement.send_keys("B")
        searchFieldElement.send_keys(Keys.RETURN)
        time.sleep(1)
        numberOfToolItems = len(toolListPage.getListOfToolItems())
        self.assertLess(
            numberOfToolItems,
            12,
            "After writing 'B' into search-field, the number of Tool-items should be decreased!",
        )
        
    def testIfShowMoreExpandsText(self):
        """Tests, if clicking `Zeige mehr` shows the whole text.

        This method tests the expansion-text-field on tool-list page.
        First it tests if the expansion-field is collapsed after
        loading the page. This is done by checking if the list
        inside the text-field is displayed. After that, the
        `Zeige mehr ...`-Link is pressed, which expands the text-
        field. It is then checked if the list is now displayed.
        Finally, the `Zeige weniger ...`-button is pressed, which
        should collapse the text again. It is then tested, if
        the list is hidden.
        """
        # self.openToolListAndLogin()
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolListPage = ToolListPage(self.driver)

        time.sleep(5)
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerObj.getCookieAcceptanceButton().click()

        self.assertFalse(
            toolListPage.getListInExpandedText()[0].is_displayed(),
            "The list inside the expand-field is shown, but it should be collapsed on page load!",
        )

        toolListPage.getShowMoreElement().click()

        listOfListElements = toolListPage.getListInExpandedText()
        time.sleep(1)
        self.assertTrue(
            listOfListElements[0].is_displayed(),
            "List-Element is not Displayed after clicking on 'Zeige mehr ...'!",
        )

        time.sleep(1)
        showLessLink = toolListPage.getShowLessElement()
        self.driver.execute_script("arguments[0].click();",showLessLink)
        #time.sleep(1)
        #showLessLink.click()

        time.sleep(1)
        self.assertFalse(
            toolListPage.getListInExpandedText()[0].is_displayed(),
            "List is still displayed after clicking 'show less ...'!",
        )


    def openToolList(self) -> None:
        """Helper-method, which connects to tool-list page.

        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).perform()
        time.sleep(1)
        digitalToolsItem = navBar.getNavDigitalTools()

        digitalToolsItem.click()

    def checkPageTitle(self, pageTitle) -> None:
        """

        """
        try:
            if self.driver.title == pageTitle:
                print("WebPage loaded successfully")
                self.assertEqual(self.driver.title, pageTitle)
        except Exception as error:
            print(error + "WebPage Failed to load")
