"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from src.page_obj.locators import Locator
from src.page_obj.pages.generic_page_obj import GenericPageObject


class ComparisonPageSection(GenericPageObject):

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getCompareButton(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.compareButton,
            )
        except:
            return None

    def getSecondComparisonDiv(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.secondComparisonDiv,
            )
        except:
            return None

    def getFirstComparisonDiv(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.compareContainer,
            )
        except:
            return None

    def getHeadingComparisonSite(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.headingComparisonSite,
            )
        except:
            return None

    def getComparisonTableContainer(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.comparisonTableContainer,
            )
        except:
            return None

    def getCompareResultsContainer(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.compareResultsContainer,
            )
        except:
            return None

    def getBackButton(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.backButton,
            )
        except:
            return None

    def getStartCompareButtonLink(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.compareButton,
            )
        except:
            return None
    
    def getResetButtonLink(self):
        return self.driver.find_element(
            By.XPATH,
            "//div[@id='cancelButtonTools']",
        )

    def getResetComparisonDiv(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.resetComparisonDiv,
            )
        except:
            return None
