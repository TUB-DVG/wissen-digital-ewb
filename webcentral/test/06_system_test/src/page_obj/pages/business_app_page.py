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


class BusinessAppPage(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getCards(self):
        """Return the Cards, which shows the present Business-Applications"""
        return self.driver.find_elements(By.XPATH, Locator.cardLocator)

    def getSearchField(self):
        """Return the Search-Input-Field on the Business-Application Site"""
        return self.driver.find_element(By.XPATH, Locator.businessSearchField)

    def getFurtherInfoOnDetailsPage(self):
        """Return the a-Webelement to the FurtherInfo-Site"""
        return self.driver.find_element(
            By.XPATH, Locator.businessDetailsFurtherInfo
        )

    def getTagsOnDetailPage(self):
        """Return the list of Tags on the Details-Page of an BusinessApp"""
        return self.driver.find_elements(By.XPATH, Locator.businessDetailsTags)

    def getSearchResultFilter(self, tagText):
        """Return the Search-Result-filter, with the name `tagText`

        tagText:    str
        Tag Text in the Business-Application Detail
        """
        try:
            return self.driver.find_element(
                By.XPATH, f"//a[contains(text(), '{tagText}')]"
            )

        except:
            return None
