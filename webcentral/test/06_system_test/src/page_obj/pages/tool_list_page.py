"""

"""

import sys

sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from src.page_obj.locators import Locator
from src.page_obj.pages.generic_page_obj import GenericPageObject


class ToolListPage(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver
        self.toolListLink = Locator.toolListLink

    def getSearchInputElement(self):
        """ """
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
        elements = self.driver.find_elements(
            By.XPATH,
            Locator.toolItemsIdentifer,
        )
        self.waitUntilElementIsLoaded(elements[0])
        return elements

    def getSearchStringButton(self, searchStr: str) -> WebElement:
        """Returns the selenium webelement, for Search String Button"""

        return self.driver.find_element(
            By.XPATH,
            f"//a[contains(text(), 'Suchbegriff: {searchStr}')]",
        )

    def getXOfSearchFilter(self):
        """Return the X to remove a search filter"""
        return self.driver.find_element(By.XPATH, Locator.searchStrBoxX)

    def getCloseOnSearchStrButton(self, searchStrBox: WebElement) -> WebElement:
        """Returns the WebElement, which reprents the X in Search-String-Box"""
        try:
            return searchStrBox.find_element(
                By.XPATH,
                Locator.searchStrBoxX,
            )
        except NoSuchElementException:
            print("The x is not present on a search filter. Test failed!")

    def getSearchCategorySelect(self) -> WebElement:
        """Returns Categorie-Select from Search Tab"""

        return Select(
            self.driver.find_element(
                By.XPATH,
                Locator.searchCategorieSelect,
            )
        )

    def getSearchLicenceSelect(self) -> WebElement:
        """Returns Licence-Select from Search Tab"""

        return Select(
            self.driver.find_element(
                By.XPATH,
                Locator.searchLicenceSelect,
            )
        )

    def getSearchLifecycleSelect(self) -> WebElement:
        """Returns Licence-Select from Search Tab"""

        return Select(
            self.driver.find_element(
                By.XPATH,
                Locator.searchLifecycleSelect,
            )
        )

    def getMagniferButton(self):
        """Returns the magnitfer-button in the search-bar."""

        return self.driver.find_element(
            By.XPATH,
            Locator.searchMagniferButton,
        )

    def getListOfCurrentlyActiveSearchFilter(self):
        """Returns list of currently active search filter."""
        return self.driver.find_elements(
            By.XPATH,
            Locator.activeSearchFilter,
        )

    def getResetButton(self):
        """Returns the Search-Reset Button."""
        return self.driver.find_element(
            By.XPATH,
            Locator.searchResetButton,
        )

    def getShowMoreElement(self):
        """Returns the `Zeige mehr`-link element on tool-list page."""
        return self.driver.find_element(
            By.XPATH,
            Locator.showMoreLink,
        )

    def getListInExpandedText(self):
        """Returns list of list-elements in expanded Text."""
        return self.driver.find_elements(By.XPATH, Locator.listInExpandedText)

    def getShowLessElement(self):
        """Returns the `Zeige weniger ...`-element"""
        return self.driver.find_element(
            By.XPATH,
            Locator.showLessLink,
        )

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
        """Return the span element, which holds the current Search result page number"""
        return self.driver.find_element(By.XPATH, Locator.paginationCurrentSite)
