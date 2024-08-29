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


class TechnicalStandartsPage(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getNormsLink(self):
        """Return the Link to the Norm-Page"""
        return self.driver.find_element(By.XPATH, Locator.linkToNormsOnTS)

    def getProtocolsLink(self):
        """Return the Link to the Protocols-Page"""
        return self.driver.find_element(By.XPATH, Locator.linkToProtocolsOnTS)
