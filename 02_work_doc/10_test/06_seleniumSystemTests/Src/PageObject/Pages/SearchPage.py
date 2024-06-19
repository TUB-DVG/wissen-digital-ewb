"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator
from Src.PageObject.Pages import GenericPageObject


class SearchPage(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getUsageDropdown(self):
        """Return the usage-dropdown field"""
        return self.driver.find_elements(
            By.XPATH,
            Locator.usageDropdownElement,
        )

    def getAccessabilityDropdown(self):
        """Return the accessability-dropdown field"""
        return self.driver.find_elements(
            By.XPATH,
            Locator.accessabilityDropdownElement,
        )

    def getAccessabilityParagraph(self, searchText):
        """Return the accessability-value from details-page

        searchText: string
        Text, which is written inside the paragraph
        """
        return self.driver.find_element(
            By.XPATH,
            f"//p[contains(text(), {searchText})]",
        )

    def getLifeCyclePhaseSpan(self, searchText):
        """Return the LifeCyclePhase-value from details-page

        searchText: string
        Text, which is written inside the span
        """
        return self.driver.find_element(
            By.XPATH,
            f"//span[contains(text(), {searchText})]",
        )

    def getLifeCyclePhaseDropdown(self):
        """Return the webelement corresponding to the lifecyclePhaseDropdown on searchpage"""
        return self.driver.find_elements(
            By.XPATH,
            Locator.lifeCyclePhaseDropdownElement,
        )

    def getSearchSubmitButton(self):
        """Return the search submit button"""
        return self.driver.find_element(
            By.XPATH,
            Locator.searchSubmitButton,
        )

    def getCards(self):
        """Return the Cards, which show the search results"""
        return self.driver.find_elements(By.XPATH, Locator.cardLocator)

    def getUsageForToolOnDetailPage(self):
        """Return Element in which usages are shown."""
        return self.driver.find_element(By.XPATH, Locator.usageOnDetailPage)

    def getRadioButtons(self):
        """Return all radio buttons"""

        return self.driver.find_elements(By.XPATH, "//input[@type='radio']")

    def getTextInput(self):
        """Get free-text-search Selenium object."""
        return self.driver.find_element(By.XPATH, "//input[@name='searched']")

    def getSearchDivContainer(self):
        """Get Search-bar surrounding div container"""
        return self.driver.find_element(
            By.XPATH, "//div[contains(@class, 'searchContainer')]")
