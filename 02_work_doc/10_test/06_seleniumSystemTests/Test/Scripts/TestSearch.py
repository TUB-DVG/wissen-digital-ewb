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
    # def setUp(self):
    #     """Constructor of Testcase
        
    #     """
        

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

    def testAccessabilityDropdown(self):
        """
        
        """
        self.searchPageObj = SearchPage(self.driver)
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/buisnessApps/")
        self.accessibilityDropdown()

        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        self.accessibilityDropdown()

    def testLifeCyclePhaseDropdown(self):
        """
        
        """
        self.searchPageObj = SearchPage(self.driver)
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/buisnessApps/")
        self.lifeCyclePhaseDropdown()

        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        self.lifeCyclePhaseDropdown()

    def usageDropdown(self):
        """
        
        """
        usageDropdownoptions = self.searchPageObj.getUsageDropdown()

        # exclude Nutzung from list:
        for index, currentOption in enumerate(usageDropdownoptions):
            if currentOption.text == "Nutzung":
                del usageDropdownoptions[index]

        randomUsageElement = choice(usageDropdownoptions)
        randomUsageValue = randomUsageElement.text
        randomUsageElement.click()
        
        

        searchSubmittButton = self.searchPageObj.getSearchSubmitButton()
        searchSubmittButton.click()

        searchResultElements = self.searchPageObj.getCards()
        if len(searchResultElements) > 0:
            randomResult = choice(searchResultElements)
            self.scrollElementIntoViewAndClick(randomResult)
            usageOnDetailPage = self.searchPageObj.getUsageForToolOnDetailPage()
            self.assertTrue(randomUsageValue in usageOnDetailPage.text)
    
    def scrollElementIntoViewAndClick(self, webelement) -> None:
        """Scroll the Element into view and click it.
        
        This helper function is used to click an webelement, which is currently
        out of view of the browser page. Therefore it scrolls the page, so that the
        element is clickable, and clicks it.
        
        webelement: Webelement
            selenium webelement, which should be scrolled and clicked
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", webelement)        
        time.sleep(1)
        # breakpoint()
        webelement.click()
        time.sleep(1)


    def accessibilityDropdown(self):
        """

        """
        accessibilityDropdownoptions = self.searchPageObj.getAccessabilityDropdown()

        # exclude Nutzung from list:
        for index, currentOption in enumerate(accessibilityDropdownoptions):
            if currentOption.text == "Zugänglichkeit":
                del accessibilityDropdownoptions[index]

        randomAccessabilityElement = choice(accessibilityDropdownoptions)
        accessabilityElementValue = randomAccessabilityElement.text
        randomAccessabilityElement.click()
        
        searchSubmittButton = self.searchPageObj.getSearchSubmitButton()
        searchSubmittButton.click()

        searchResultElements = self.searchPageObj.getCards()
        if len(searchResultElements) > 0:
            randomResult = choice(searchResultElements)
            self.scrollElementIntoViewAndClick(randomResult)
            try:
                accessabilityOnDetailPage = self.searchPageObj.getAccessabilityParagraph(accessabilityElementValue)
            except:
                self.assertTrue(
                    False, 
                    f"Accessability Value '{accessabilityElementValue}' is not a displayed on details-page",
                )

    def lifeCyclePhaseDropdown(self):
        """
        
        """
        lifeCyclePhaseDropdownoptions = self.searchPageObj.getLifeCyclePhaseDropdown()

        # exclude Nutzung from list:
        for index, currentOption in enumerate(lifeCyclePhaseDropdownoptions):
            if currentOption.text == "Lebenszyklusphase":
                del lifeCyclePhaseDropdownoptions[index]

        randomLifeCyclePhaseElement = choice(lifeCyclePhaseDropdownoptions)
        randomLifeCyclePhaseValue = randomLifeCyclePhaseElement.text
        randomLifeCyclePhaseElement.click()
        
        

        searchSubmittButton = self.searchPageObj.getSearchSubmitButton()
        searchSubmittButton.click()

        searchResultElements = self.searchPageObj.getCards()
        if len(searchResultElements) > 0:
            randomResult = choice(searchResultElements)
            self.scrollElementIntoViewAndClick(randomResult)
            try:
                lifeCyclePhaseOnDetailPage = self.searchPageObj.getLifeCyclePhaseSpan(randomLifeCyclePhaseValue)
            except:
                self.assertTrue(
                    False, 
                    f"Accessability Value '{randomLifeCyclePhaseValue}' is not a displayed on details-page",
                )