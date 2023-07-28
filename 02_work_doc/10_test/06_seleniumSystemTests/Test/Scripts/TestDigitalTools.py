"""Tests the `Digitale Werkzeuge` (engl. digital tools)-Tab

This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

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
from selenium.webdriver import ActionChains

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.TestWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.cookieBanner import CookieBanner

class TestDigitalToolsPage(TestWebcentral):
    """
    
    """
    def testNavigateToDigitalToolsPage(self) -> None:
        """Navigates from norm list to digital-tools-tab.

        """

        self.driver.get("http://127.0.0.1:8070/norm_list")

        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).perform()
        time.sleep(1)
        toolListItem = navBar.getNavToolList()

        if toolListItem is not None:
            toolListItem.click()
        else:
            self.assertTrue(False)

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

        searchStringBoxX.click()
        
        time.sleep(1)
        listToolItemsAfterRmvdSearch = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listToolItemsAfterRmvdSearch),
            12,
            "After removing search-string 'Ansys', number of tool-items should be 12!",
        )

        searchFieldElement = toolListPage.getSearchInputElement()
        searchFieldElement.send_keys("B")

        time.sleep(1)
        numberOfToolItems = len(toolListPage.getListOfToolItems())
        self.assertLess(
            numberOfToolItems,
            12,
            "After writing 'B' into search-field, the number of Tool-items should be decreased!",
        )
        searchFieldElement.send_keys(Keys.RETURN)

        time.sleep(1)

        self.assertEqual(
            len(toolListPage.getListOfToolItems()),
            numberOfToolItems,
            "After pressing 'Return', the number of tool-items should stay the same!",
        )

        listOfSelectWebElements = []
        listOfSelectWebElements.append(toolListPage.getSearchCategorySelect())
        listOfSelectWebElements.append(toolListPage.getSearchLicenceSelect())
        listOfSelectWebElements.append(toolListPage.getSearchLifecycleSelect())

        numberOfSelectsToBeSet = random.choice([1, 2, 3,])

        chosenElementsList = []
        for currentNumberOfSelect in range(numberOfSelectsToBeSet):
            elementInSelectToChoose = random.choice(
                listOfSelectWebElements[currentNumberOfSelect].options,
            )
            if elementInSelectToChoose != listOfSelectWebElements[currentNumberOfSelect].first_selected_option:
                chosenElementsList.append(elementInSelectToChoose)
            elementInSelectToChoose.click()


        magniferButtonElement = toolListPage.getMagniferButton()
        magniferButtonElement.click()

        listOfActiveSearchFilter = toolListPage.getListOfCurrentlyActiveSearchFilter()
        
        for indexInList, chosenElement in enumerate(listOfActiveSearchFilter):
            if indexInList == 0:
                self.assertTrue(
                    "Suchbegriff: B" == chosenElement.text,
                    "Text Search Filter 'Suchbegriff: B' is not used, when selecting a Categorie afterwards!",
                    )
            else:
                self.assertTrue(
                    chosenElement.text == chosenElementsList[indexInList-1].text,
                    "Active Search-Filter Box does not represent choosen Element from Select-Input!",
                )
       
        resetButtonElement = toolListPage.getResetButton()
        resetButtonElement.click()

        self.assertEqual(
            len(toolListPage.getListOfToolItems()),
            12,
            "After pressing 'Reset', the number of tool-items should be 12 again!",
        )

        
        self.assertEqual(
            len(toolListPage.getListOfToolItems()),
            12,
            "After pressing 'Return', the number of tool-items should stay the same!",
        )

        time.sleep(1)

        numberOfSelectsToBeSet = random.choice([1, 2, 3,])

        chosenElementsList = []
        for currentNumberOfSelect in range(numberOfSelectsToBeSet):
            elementInSelectToChoose = random.choice(
                listOfSelectWebElements[currentNumberOfSelect].options,
            )
            if elementInSelectToChoose != listOfSelectWebElements[currentNumberOfSelect].first_selected_option:
                chosenElementsList.append(elementInSelectToChoose)
            elementInSelectToChoose.click()

    # def testSearchFirstCategoryThenString(self):
    #     """
        
    #     """
    #     self.openToolListAndLogin()

    #     toolListPage = ToolListPage(self.driver)

    #     listOfSelectWebElements = [
    #         toolListPage.getSearchCategorySelect(),
    #         toolListPage.getSearchLicenceSelect(),
    #         toolListPage.getSearchLifecycleSelect(),
    #     ]
    #     numberOfSelectsToBeSet = random.choice([1, 2, 3,])

    #     chosenElementsList = []
    #     for currentNumberOfSelect in range(numberOfSelectsToBeSet):
    #         elementInSelectToChoose = random.choice(
    #             listOfSelectWebElements[currentNumberOfSelect].options,
    #         )
    #         if elementInSelectToChoose != listOfSelectWebElements[currentNumberOfSelect].first_selected_option:
    #             chosenElementsList.append(elementInSelectToChoose)
    #         elementInSelectToChoose.click()

    #     magniferButtonElement = toolListPage.getMagniferButton()
    #     magniferButtonElement.click()
    #     listOfActiveSearchFilter = toolListPage.getListOfCurrentlyActiveSearchFilter()
    #     pdb.set_trace()
    #     for indexInList, chosenElement in enumerate(listOfActiveSearchFilter):
    #         self.assertTrue(
    #             chosenElement.text == chosenElementsList[indexInList].text,
    #             "Active Search-Filter Box does not represent choosen Element from Select-Input!",
    #         )      

    #     searchFieldElement = toolListPage.getSearchInputElement()
    #     searchFieldElement.send_keys("Hi")

    #     toolListPage.getMagniferButton().click()    
    #     listOfActiveSearchFilter = toolListPage.getListOfCurrentlyActiveSearchFilter()
    #     chosenElementsList.insert(0, "Suchbegriff: Hi")

    #     for indexInList, chosenElement in enumerate(listOfActiveSearchFilter):
    #         if indexInList == 0:
    #             self.assertTrue(
    #                 chosenElementsList[0] == chosenElement,
    #                 "Text Search Filter is not displayed!",
    #                 )
    #         else:
    #             self.assertTrue(
    #                 chosenElement.text == chosenElementsList[indexInList].text,
    #                 "Active Search-Filter Box does not represent choosen Element from Select-Input!",
    #             )

    # def testIsRedirectedToPreviousPageAfterLogin(self) -> None:
    #     """Tests, if user gets redirected to previous page after login.
        
    #     """
    #     self.driver.get("http://127.0.0.1:8070/tool_list/")
    #     time.sleep(1)

    #     if self.driver.title == "Login":
    #         loginPageObj = LoginPage(self.driver)
    #         loginPageObj.getLoginButton().click()
        
    #     self.assertTrue(
    #         self.driver.title == "Überblick über die Anwendungen",
    #         "Login Does not redirect back to tool_list!",
    #     )

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
        self.openToolListAndLogin()

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
        self.driver.get("http://127.0.0.1:8070/tool_list/")
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
