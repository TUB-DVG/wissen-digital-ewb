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

    def getLinkFromText(self, linkText: str):
        """Get link from displayed text.

        """
        return self.driver.find_element(By.XPATH, f"//a[contains(text(), '{linkText}')]")

    def getLinks(self):
        """Get all links in overview text.

        """
        return self.driver.find_elements(By.XPATH, "//div[contains(@class, 'description-content')]//a")
