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


class NormPage(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getSearchInputElement(self):
        """Return Search-input-field on"""
        return self.driver.find_element(By.XPATH, Locator.searchInputNorms)

    def getCards(self):
        """Get the div-card-elements as list"""
        return self.driver.find_elements(By.XPATH, Locator.cardLocator)

    def getXOfSearchFilter(self):
        """Get the X, link, which removes the searchfilter"""
        return self.driver.find_element(By.XPATH, Locator.xFromSearchFilter)
