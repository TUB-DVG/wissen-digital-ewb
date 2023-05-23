"""Tests the `Digitale Werkzeuge` (engl. digital tools)-Tab

This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

"""
import pdb
import sys
sys.path.append(sys.path[0] + "/...")

import time
import os
import unittest

from selenium import (
    webdriver,

)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.loginPage import LoginPage

class TestDigitalToolsTab(WebDriverSetup):
    """
    
    """
    def testNavigateToDigitalToolsTab(self) -> None:
        """Navigates from startpage to digital-tools-tab.

        """

        self.driver.get("http://127.0.0.1:8070")
        self.driver.set_page_load_timeout(30)
        webPageTitle = "Wissensplattform - Digitalisierung Energiewendebauen"
        
        self.checkPageTitle(webPageTitle)
        
        startPage = StartPage(self.driver)

        toolListLink = startPage.getToolListLink()
        if toolListLink is not None:
            toolListLink.click()
        else:
            self.assertTrue(False)
        
        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

    def testSearchField(self):
        """Tests the Search Function in `Digitale Anwendungen`
        
        """
        self.driver.get("http://127.0.0.1:8070/tool_list/")
        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

        loginPageObj = LoginPage(self.driver)

        loginButtonElement = loginPageObj.getLoginButton()

        if loginButtonElement is not None:
            loginButtonElement.click()


        startPage = StartPage(self.driver)   
        toolListLink = startPage.getToolListLink()
        toolListLink.click() 

        toolListPage = ToolListPage(self.driver)

        searchFieldElement = toolListPage.getSearchInputElement()
        if searchFieldElement is None:
            self.assertTrue(False)
            return
        
        searchFieldElement.send_keys("Ansys")
        time.sleep(1)
        listOfToolItems = toolListPage.getListOfToolItems()

        self.assertEqual(
            len(listOfToolItems),
            1,
            "Number of Tool Items should be one for Search-String 'Ansys'!",
        )
        searchFieldElement.send_keys(Keys.RETURN)
        listOfToolItemsAfterReturn = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listOfToolItemsAfterReturn),
            1,
            "Number of Tool Items should be one for Search-String 'Ansys'!",
        )

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


        pdb.set_trace()




        



    def checkPageTitle(self, pageTitle):
        """
        
        """
        try:
            if self.driver.title == pageTitle:
                print("WebPage loaded successfully")
                self.assertEqual(self.driver.title, pageTitle)
        except Exception as error:
            print(error + "WebPage Failed to load")
