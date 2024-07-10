"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from Src.PageObject.Locators import Locator
from Src.PageObject.Pages.GenericPageObject import GenericPageObject


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
