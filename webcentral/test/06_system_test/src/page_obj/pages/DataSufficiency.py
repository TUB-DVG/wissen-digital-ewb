"""

"""

import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from Src.PageObject.Locators import Locator
from Src.PageObject.Pages.GenericPageObject import GenericPageObject


class DataSufficiency(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getContentDiv(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.contentDiv,
            )
        except:
            return None

    def getAllCollapsableFirstParts(self):
        """Get the div of the collapsables, which include the text,
        which is shown in collapsed state.

        """
        return self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'firstPart')]"
        )
