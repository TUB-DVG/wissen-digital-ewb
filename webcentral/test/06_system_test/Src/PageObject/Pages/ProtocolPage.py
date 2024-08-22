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
from Src.PageObject.Pages.GenericPageObject import GenericPageObject

class ProtocolPage(GenericPageObject):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver

    def getSearchInputElement(self):
        """Return Search-input-field on 
        
        """
        return self.driver.find_element(By.XPATH, Locator.searchInputProtocols)


    def getCards(self):
        """Get the div-card-elements as list 
        
        """
        elements =  self.driver.find_elements(By.XPATH, Locator.cardLocator)
        if len(elements) > 0:
            self.waitUntilElementIsLoaded(elements[0])
        return elements
    
    def getXOfSearchFilter(self):
        """Get the X, link, which removes the searchfilter
        
        """
        return self.driver.find_element(By.XPATH, Locator.xFromSearchFilter)
