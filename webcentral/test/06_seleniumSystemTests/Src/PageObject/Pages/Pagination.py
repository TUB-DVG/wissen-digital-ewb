"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator
from Src.PageObject.Pages.GenericPageObject import GenericPageObject


class Pagination(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver
    
    def getPaginationCurrentSiteString(self):
        """Get the span element, which holds the information on which
        site of the total number of sites the user currently is.
        """
        element = self.driver.find_element(By.XPATH, "//span[@class='current']")
        self.waitUntilElementIsLoaded(element)
        return element
    
    def getPaginationNextLink(self):
        """Return link to next pagination site
        """

        nextElement = self.driver.find_element(By.XPATH, "//a[@id='paginationNextLink']")
        self.waitUntilElementIsLoaded(nextElement)
        return nextElement

