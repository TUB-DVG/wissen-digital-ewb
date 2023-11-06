"""

"""
import sys
sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class SearchPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
    
    def getUsageDropdown(self):
        """Return the usage-dropdown field 
        
        """
        return self.driver.find_elements(
            By.XPATH,
            Locator.usageDropdownElement,
        )
    
    def getAccessabilityDropdown(self):
        """Return the accessability-dropdown field
        
        """
        return self.driver.find_elements(
            By.XPATH,
            Locator.accessabilityDropdownElement,
        )


    def getSearchSubmitButton(self):
        """Return the search submit button

        """
        return self.driver.find_element(
            By.XPATH,
            Locator.searchSubmitButton,
        )        
    
    def getCards(self):
        """Return the Cards, which show the search results
        
        """
        return self.driver.find_elements(By.XPATH, Locator.cardLocator)
    
    def getUsageForToolOnDetailPage(self):
        """Return Element in which usages are shown.
        
        """
        return self.driver.find_element(By.XPATH, Locator.usageOnDetailPage)

    