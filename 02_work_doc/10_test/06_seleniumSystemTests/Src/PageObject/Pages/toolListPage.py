"""

"""
import sys
sys.path.append(sys.path[0] + "/....")
import pdb

from selenium import (
    webdriver,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class ToolListPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
        self.toolListLink = Locator.toolListLink


    def getSearchInputElement(self):
        """
        
        """
        try:
            return self.driver.find_element(
                By.XPATH, 
                Locator.toolListSearchInput,
            )
        except NoSuchElementException:
            print("Search input Element couldnt be located on webpage!")
            return None
    
    def getListOfToolItems(self) -> list:
        """Returns a list of tool items, which are present in driver-instance

        This method returns a list of tool items, which are currently
        visible in the `self.driver`-instance (in the Browser). The
        visible tool items can differ, depending on the selected
        search parameters.

        Parameters
        ----------

        Returns
        -------
            list
        List of selenium-elements, whereby each element represents a
        list-item object in the UI on the `Digitale Werkzeuge`-Tab.
        
        """
        return self.driver.find_elements(
            By.XPATH, 
            Locator.toolItemsIdentifer,
        )
    
    def getSearchStringButton(self, searchStr: str) -> WebElement:
        """Returns the selenium webelement, for Search String Button
        
        """

        return self.driver.find_element(
            By.XPATH,
            f"//a[contains(text(), 'Suchbegriff: {searchStr}')]",
        )

    def getCloseOnSearchStrButton(self, searchStrBox: WebElement) -> WebElement:
        """Returns the WebElement, which reprents the X in Search-String-Box
        
        """

        return searchStrBox.find_element(
            By.XPATH,
            Locator.searchStrBoxX,
        )


