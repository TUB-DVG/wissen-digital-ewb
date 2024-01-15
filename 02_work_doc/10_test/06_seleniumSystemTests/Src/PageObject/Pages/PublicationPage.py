"""

"""
import sys
sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Src.PageObject.Locators import Locator

class PublicationPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
    
    def getPublicationContainer(self):
        """Return the most outer container of the publications-page to check
        if the border color matches the expected color.

        """
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, Locator.publicationContainer)))
        return element
    
    def getPublicationSearchBoxForm(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxForm)

    def getPublicationSearchBoxInput(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxInput)
    
    def getPublicationSearchBoxSelect(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxSelect)
    
    def getPublicationSearchBoxSubmit(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxSubmit)
    
    def getPublicationSearchBoxReset(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxReset)