from selenium.webdriver.common.by import By

from src.page_obj.locators import Locator


class UserIntegrationPage(object):
    """Class, which represents the About-Page-FrontEnd."""

    def __init__(self, driver):
        """Constructor of AboutPage"""
        self.driver = driver
