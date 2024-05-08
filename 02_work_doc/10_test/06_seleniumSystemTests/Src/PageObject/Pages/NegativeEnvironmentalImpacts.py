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

class NegativeEnvironmentalImpacts(object):
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

    def getBoxesDiv(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.boxesDiv,
            )
        except:
            return None

    def getBox1and2(self):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return [
                self.driver.find_element(
                By.XPATH,
                Locator.box1,
                ),
                self.driver.find_element(
                    By.XPATH,
                    Locator.box2,
                )
            ]

        except:
            return None
    
    def getBoxHeading(self, boxElement):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return boxElement.find_element(
                By.XPATH,
                Locator.boxHeading,
            )
        except:
            return None

    def getBoxDescription(self, boxElement):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return boxElement.find_element(
                By.XPATH,
                Locator.boxDescription,
            )
        except:
            return None

    def getBoxImage(self, boxElement):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return boxElement.find_element(By.XPATH, Locator.boxImage,)
        except:
            return None


    def getImageInBox(self, imageDivElement):
        """Returns the div-element, which wraps the content of the page
        
        """
        try:
            return imageDivElement.find_element(By.XPATH, Locator.imageInDiv,)
        except:
            return None
    
    def getDescriptionHeadingDiv(self):
        """Returns the div-element, which wraps the description-heading
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.descriptionHeadingDiv,
            )
        except:
            return None

    def getDescriptionContentDiv(self):
        """Returns the div-element, which wraps the description-heading
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.descriptionContentDiv,
            )
        except:
            return None
    
    def getLinkToComponentList(self):
        """Returns the div-element, which wraps the description-heading
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//a[contains(@href, '{Locator.linkToComponentsListPage}')]",
            )
        except:
            return None

    def getLinkToDataProcessing(self):
        """Returns the div-element, which wraps the description-heading
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//a[contains(@href, '{Locator.linkToDataProcessingPage}')]",
            )
        except:
            return None