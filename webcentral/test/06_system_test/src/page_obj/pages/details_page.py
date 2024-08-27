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

from src.page_obj.locators import Locator
from src.page_obj.pages.generic_page_obj import GenericPageObject


class DetailsPage(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getLinkNavigatorDiv(self):
        """Returns the div-element, which wraps the navigation links"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.linkNavigatorDiv,
            )
        except:
            return None

    def getBackLink(self):
        """Returns the back link"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.backButton,
            )
        except:
            return None

    def getSecondaryNavBar(self):
        """Returns the secondary navigation bar"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, {Locator.secondaryNavBar})]",
            )
        except:
            return None

    def getRightColumn(self):
        """Return the right column of the details-page"""
        return self.driver.find_element(By.XPATH, "//div[contains(@class, 'column__right')]")

    def getATagsInContentContainer(self):
        """Get all a-tags in the content container.

        """
        return self.driver.find_elements(By.XPATH, "//div[contains(@class, 'border-operational')]//a")
