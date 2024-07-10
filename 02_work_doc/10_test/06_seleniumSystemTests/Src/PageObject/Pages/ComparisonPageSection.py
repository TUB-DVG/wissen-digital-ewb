"""

"""
import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from Src.PageObject.Locators import Locator
from Src.PageObject.Pages.GenericPageObject import GenericPageObject


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
                Locator.firstComparisonDiv,
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

    def getStartComparisonDiv(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.startComparisonDiv,
            )
        except:
            return None

    def getResetComparisonDiv(self):
        """ """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.resetComparisonDiv,
            )
        except:
            return None
