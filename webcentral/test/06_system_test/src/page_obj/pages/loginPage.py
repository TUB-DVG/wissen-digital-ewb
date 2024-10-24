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


class LoginPage(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver
        self.loginButtonElement = Locator.loginButtonElement

    def getLoginButton(self):
        """Returns the Login-Button Element, if it is present."""

        try:
            return self.driver.find_element(
                By.XPATH,
                self.loginButtonElement,
            )
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None
