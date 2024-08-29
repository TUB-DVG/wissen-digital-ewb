"""

"""

import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.page_obj.locators import Locator


class Footer(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getLanguageSelectionField(self):
        """Returns the Language Selection Field from the Footer"""
        try:
            return Select(
                self.driver.find_element(
                    By.XPATH,
                    Locator.languageSelectionField,
                )
            )
        except:
            return None
