from selenium.webdriver.common.by import By

from src.page_obj.locators import Locator


class OverviewPageSection(object):
    """Class, which represents the About-Page-FrontEnd."""

    def __init__(self, driver):
        """Constructor of AboutPage"""
        self.driver = driver

    def getHeading(self):
        """Return the heading from the overview page section.

        """
        return self.driver.find_element(By.XPATH, Locator.overviewPageHeading) 
