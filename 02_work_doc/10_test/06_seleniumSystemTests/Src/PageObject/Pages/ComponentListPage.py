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

class ComponentListPage(object):
    """
    
    """
    def __init__(self, driver):
        """
        
        """
        self.driver = driver
    
    def getContentDiv(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.contentDiv,
            )
        except:
            return None

    def getSecondaryNavbar(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.secondaryNavBar}')]",
            )
        except:
            return None
    
    def getDescendantsByTagName(self, element, tagName):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return element.find_elements(
                By.TAG_NAME,
                tagName,
            )
        except:
            return None

    def getDescriptionSection(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(By.XPATH,f"//div[contains(@class, '{Locator.descriptionBox}')]")
        except:
            return None

    def getDescriptionHeading(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionHeading}')]",
            )
        except:
            return None

    def getDescriptionText(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionText}')]",
            )
        except:
            return None

    def getDescriptionDownloadLink(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionText}')]",
            )
        except:
            return None

    def getDescriptionImage(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionImage}')]",
            )
        except:
            return None