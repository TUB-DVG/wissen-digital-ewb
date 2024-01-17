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
from selenium.common.exceptions import NoSuchElementException

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
        time.sleep(3)
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
        searchFieldElement.send_keys("Bim")
        searchFieldElement.send_keys(Keys.RETURN)
        time.sleep(1)
        numberOfToolItems = len(toolListPage.getListOfToolItems())
        self.assertLess(
            numberOfToolItems,
            12,
            "After writing 'Bim' into search-field, the number of Tool-items should be decreased!",
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

    def testConsistentPagination(self):
        """
        This method tests the pagination of tool list
        the first page should have first and last page but no previous page.
        Also the number of pages displayed on the first page 
        matches the number shown on the last page
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolPageObj = ToolListPage(self.driver)

        listOfNextElement = toolPageObj.getNextElementInList()
        self.assertEqual(
            len(listOfNextElement),
            1,
            "next-search-results-page should be present, but it is not!",
        )
        listOfPreviousElement = toolPageObj.getPreviousElementInList()
        self.assertEqual(
            len(listOfPreviousElement),
            0,
            "previous-search-results-page should not be present, but it is!",
        )
        listOfFirstElement = toolPageObj.getFirstElementInList()
        self.assertEqual(
            len(listOfFirstElement),
            0,
            "First-search-results-page should not be present, but it is!",
        )
        listOfLastElement = toolPageObj.getLastElementInList()
        self.assertEqual(
            len(listOfLastElement),
            1,
            "last-search-results-page should be present, but it is not!",
        )
        currentPageNumberElement = toolPageObj.getCurrentSearchResultNumber()
        indexPageEndNumber = currentPageNumberElement.text.split()[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", listOfLastElement[0])
        time.sleep(1)
        listOfLastElement[0].click()
        time.sleep(1)
        currentPageNumberElement = toolPageObj.getCurrentSearchResultNumber()
        lastPageEndNumber = currentPageNumberElement.text.split()[-1]
        self.assertEqual(
            indexPageEndNumber,
            lastPageEndNumber,
            "Page numbers on the first and last pages should be the same",
        )
    def testIfToolImageErrorTextIsPresent(self):
        """Check if a tool is on the page, which has the 'tool image (if=db)'-error
      In this test all pages of the digital-tools-tab are gone through and checked if one of the tools shows the image error 'tool image (if=db)'. If so the test is red.
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolsPageObj = ToolListPage(self.driver)
        paginationPagesStr = toolsPageObj.getCurrentSearchResultNumber()
        numberOfPages = int(paginationPagesStr.text[-1])
        script = """
        var img = arguments[0];
        if (img.naturalWidth === 0) {
            return img.alt;
        } else {
            return null;
        }
        """ 
        foundAltText = False
        for currentPageNumber in range(numberOfPages):
            listOfToolItemsOnCurrentPage = toolsPageObj.getListOfToolItems()
            for toolItem in listOfToolItemsOnCurrentPage:
                try:
                    imageOfCurrentItem = toolItem.find_element(By.XPATH, ".//img")
                except NoSuchElementException:
                    continue
                altTextPresent = self.driver.execute_script(script, imageOfCurrentItem)
                if altTextPresent:
                    toolName = toolItem.text.split('\n')[0]
                    print(f"Alt Text is present for Tool {toolName} instead of the image.")                
                    foundAltText = True
            
            nextLink = toolsPageObj.getNextElementInList()
            if len(nextLink) > 0:
                nextLink = toolsPageObj.getNextElementInList()[0]
                self.scrollElementIntoViewAndClickIt(nextLink)
            
        self.assertFalse(foundAltText, "Found Alt-Text for images in Digital-Tools. Check if the image for the tool is present in the media-folder")
        
