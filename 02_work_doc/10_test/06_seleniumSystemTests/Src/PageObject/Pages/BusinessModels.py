"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator


class BusinessModels(GenericPageObject):

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getHeadingContainer(self):
        """Get the heading container containing icon and heading"""

        return self.driver.find_element(
            By.XPATH, "//div[contains(@class, 'description-heading')]")

    def getDescriptionContainer(self):
        """Get the heading container containing icon and heading"""

        return self.driver.find_element(
            By.XPATH, "//div[contains(@class, 'description-content')]")
