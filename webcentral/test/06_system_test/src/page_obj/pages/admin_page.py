from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator


class AdminPage(object):
    """Class, which represents the Admin-Page-FrontEnd."""

    def __init__(self, driver):
        """Constructor of AdminPage"""
        self.driver = driver

    def getUsernameInput(self):
        """Returns username input field."""
        return self.driver.find_element(
            By.XPATH,
            Locator.adminPageUsernameInput,
        )

    def getPasswordInput(self):
        """Returns password input field."""
        return self.driver.find_element(
            By.XPATH,
            Locator.adminPagePasswordInput,
        )

    def getLoginSubmit(self):
        """Returns the Login-Submit Button."""
        return self.driver.find_element(
            By.XPATH,
            Locator.adminPageSubmit,
        )
