from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator


class UserEngagmentPage(object):
    """Class, which represents the About-Page-FrontEnd."""

    def __init__(self, driver):
        """Constructor of AboutPage"""
        self.driver = driver
