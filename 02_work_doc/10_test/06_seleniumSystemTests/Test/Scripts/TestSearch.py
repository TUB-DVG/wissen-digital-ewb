"""Script to test the different search sites like
    - business-Apps site
    - tools-site
It is used to reduce redundancy in the businessApps and Tools-test scripts,
since the search in buisnessApps and Tools work the same way.
"""
import sys
sys.path.append(sys.path[0] + "/...")

import time
import os
from random import choice

from selenium import (
    webdriver,

)
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

class TestSearch(WebDriverSetup):
    """
    
    """
    def testUsageDropDown(self):
        """Test if the usage dropdown works.
        
        One element of the usage dropdown menu is chosen randomly
        and clicked. After that the search button is clicked. This 
        process is done for tools and business Apps
        
        """
        self.searchPageObj = SearchPage(self.driver)

        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/buisnessApps/")
        self.usageDropdown()

        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        self.usageDropdown()

    def usageDropdown(self):
        """
        
        """
        usageDropdownoptions = self.searchPageObj.getUsageDropdown()

        # exclude Nutzung from list:
        for index, currentOption in enumerate(usageDropdownoptions):
            if currentOption.text == "Nutzung":
                del usageDropdownoptions[index]

        randomUsageElement = choice(usageDropdownoptions)
        randomUsageElement.click()
        
        searchSubmittButton = self.searchPageObj.getSearchSubmitButton()
        searchSubmittButton.click()

        searchResultElements = self.searchPageObj.getCards()
        if len(searchResultElements) > 0:
            randomResult = choice(searchResultElements)

            usageOnDetailPage = self.searchPageObj.getUsageForToolOnDetailPage()
            self.assertTrue(randomUsageElement in usageOnDetailPage.text)
    
    def accessibilityDropdown(self):
        """

        """
        accessibilityDropdownoptions = self.searchPageObj.getUsageDropdown()

        # exclude Nutzung from list:
        for index, currentOption in enumerate(usageDropdownoptions):
            if currentOption.text == "Nutzung":
                del usageDropdownoptions[index]

        randomUsageElement = choice(usageDropdownoptions)
        randomUsageElement.click()
        
        searchSubmittButton = self.searchPageObj.getSearchSubmitButton()
        searchSubmittButton.click()

        searchResultElements = self.searchPageObj.getCards()
        if len(searchResultElements) > 0:
            randomResult = choice(searchResultElements)

            usageOnDetailPage = self.searchPageObj.getUsageForToolOnDetailPage()
            self.assertTrue(randomUsageElement in usageOnDetailPage.text)