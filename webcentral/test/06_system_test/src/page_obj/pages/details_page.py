"""

"""

import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.page_obj.locators import Locator
from src.page_obj.pages.generic_page_obj import GenericPageObject


class DetailsPage(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        # super().__init__(driver)
        self.driver = driver

    def getATagsInContentContainer(self):
        """Returns a tag in the content container"""
        return self.driver.find_element(
            By.XPATH, "//div[contains(@class, 'container')]"
        ).find_elements(By.XPATH, ".//a")
