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

class StartPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
        #self.toolListLink = Locator.toolListLink


    def getImpressumLink(self):
        """Return Impressum Webelement
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.linkToImpressum, 
        )

    

