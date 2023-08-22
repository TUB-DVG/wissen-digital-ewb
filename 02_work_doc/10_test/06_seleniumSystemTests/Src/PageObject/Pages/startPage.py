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

class StartPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
        #self.toolListLink = Locator.toolListLink


    def getImpressumLink(self):
        """Return Impressum Webelement
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.linkToImpressum, 
        )
    
    def getSearchInputField(self):
        """Return Search-Input Webelement from MainPage
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.inputSearchField, 
        )
    
    def getSearchResults(self):
        """Return the Search-Results

        The Search-Results are stored in a Table. One Row is represented 
        by an <tr></tr> Element. Therefore all <tr>-webelements are returned.
        This includes also the header-row.
        
        """
        return self.driver.find_elements(
            By.XPATH, 
            Locator.resultElements,
        )

    def getFirstColumn(self, columnWebelement):
        """Return first Column to a row-html <tr>-webelement
        
        """

        return columnWebelement.find_element(
            By.XPATH, 
            Locator.firstColumnToRow,
        )

    def getChildEbElement(self, webElement):
        """Return the first colum of the row

        Method returns the first td-element in that <tr>-tag

        webElement: Selenium.Webelement
        Selenium Webelement, which represents a <tr>-tag of a table
        """
        return webElement.find_element(By.XPATH, "td")

    def getLinkToBuisnessApps(self):
        """Return Link to Buisness-Apps
        
        """
        return self.driver.find_element(By.XPATH, Locator.linkToBuisnessApp)
