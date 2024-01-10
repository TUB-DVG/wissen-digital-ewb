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

    def getLinkToTechnicalStandarts(self):
        """Return Link to Technical Standarts Page
        
        """
        return self.driver.find_element(By.XPATH, Locator.linkToTechnicalStandarts)

    def getLinkToPublications(self, focus: str):
        """Return the Link to the Technical Publications Page,
        which is located in the box "Technische Publikationen"
        below the search-bar.

        focus: str
            String, which represents the focus for which the publication-link should 
            be returned    
        """
        if focus == "technisch":
            locator = Locator.linkToTechnicalPublications
        elif focus == "betrieblich":
            locator = Locator.linkToOperationalPublications
        elif focus == "rechtlich":
            locator = Locator.linkToLegalPublications
        elif focus == "ökologisch":
            locator = Locator.linkToEcologicalPublications
        else:
            return None
        return self.driver.find_element(By.XPATH, locator)

    def getNextElementInList(self) -> list:
        """Return List of webelements, containing next-element of pagination

        The Element is returned as list, to check if is present on page

        Returns:
        List(Webelement):   
        """

        return self.driver.find_elements(By.XPATH, Locator.paginationNextLink)

    def getPreviousElementInList(self) -> list:
        """Return List of webelements, containing previous-element of pagination

        The Element is returned as list, to check if is present on page

        Returns:
        List(Webelement):   
        """

        return self.driver.find_elements(By.XPATH, Locator.paginationPreviousLink)

    def getLastElementInList(self) -> list:
        """Return List of webelements, containing Last-element of pagination

        The Element is returned as list, to check if is present on page

        Returns:
        List(Webelement):   
        """

        return self.driver.find_elements(By.XPATH, Locator.paginationLastLink)

    def getFirstElementInList(self) -> list:
        """Return List of webelements, containing First-element of pagination

        The Element is returned as list, to check if is present on page

        Returns:
        List(Webelement):   
        """

        return self.driver.find_elements(By.XPATH, Locator.paginationFirstLink)
    
    def getCurrentSearchResultNumber(self):
        """Return the span element, which holds the current Search result page number
        
        """
        return self.driver.find_element(By.XPATH, Locator.paginationCurrentSite)