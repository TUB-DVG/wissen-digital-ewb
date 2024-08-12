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


class ComponentListPage(GenericPageObject):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getContentDiv(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.contentDiv,
            )
        except:
            return None

    def getSecondaryNavbar(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.secondaryNavBar}')]",
            )
        except:
            return None

    def getDescriptionSection(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionBox}')]")
        except:
            return None

    def getDescriptionHeading(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionHeading}')]",
            )
        except:
            return None

    def getDescriptionText(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionText}')]",
            )
        except:
            return None

    def getDescriptionDownloadLink(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionText}')]",
            )
        except:
            return None

    def getDescriptionImage(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, '{Locator.descriptionImage}')]",
            )
        except:
            return None

    def getSearchContainer(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[contains(@class, {Locator.searchContainer})]",
            )
        except:
            return None

    def getSearchInputField(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.searchInputField,
            )
        except:
            return None

    def getSelectFieldsInSearchContainer(self):
        """Returns the div-element, which wraps the content of the page"""
        return [
                self.driver.find_element(
                    By.XPATH,
                    Locator.selectCategory,
                ),
                self.driver.find_element(
                    By.XPATH,
                    Locator.selectComponent,
                ),
            self.driver.find_element(
                By.XPATH,
                Locator.selectSorting,
            ),
        ]

    def getInputOfMultiSelects(self):
        """Return all input fields, which are part of a use-select-bootstrap select.

        """
        return self.driver.find_elements(By.XPATH, "//div[contains(@class, 'input-wrapper')]/input")

    def getOptionsForSelect(self, selectElement):
        """Return the options as a list of divs of the element `selectElement`

        """
        divSiblingOfSelect = selectElement.find_element(By.XPATH, "following-sibling::div")
        
        return self.getDescendantsByClass(divSiblingOfSelect, "dropdown-item")


    def getCompareContainer(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.compareContainer,
            )
        except:
            return None

    def getPaginationContainer(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                f"//div[@id='{Locator.paginationContainer}']",
            )
        except:
            return None

    def getDownloadLink(self):
        """Return the a-element, which triggers the download of the component-list excel file.

        """
        return self.driver.find_element(By.XPATH, "//div[contains(@class, 'descriptionContainer')]/div/a")

    def getComponentListingContainer(self):
        """Return the Component Listing Container"""
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.componentListingContainer,
            )
        except:
            return None

    def getAllListElements(self):
        """Return the Component Listing Container"""
        try:
            return self.driver.find_elements(
                By.XPATH,
                Locator.componentListElementContainer,
            )
        except:
            return None

    def getCollapsedContainerInComponent(self):
        """Return the Component Listing Container"""
        try:
            return self.driver.find_elements(
                By.ID,
                "//div[contains(@class, 'collapse')]",
            )
        except:
            return None

    def getDescendantsByClass(self, element, className):
        """ """
        try:
            return element.find_elements(
                By.XPATH, f".//*[contains(@class, '{className}')]")
        except:
            return None

    def getSearchSubmitButton(self):
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.searchSubmit,
            )
        except:
            return None

    def getDropdownElements(self, element):
        try:
            return element.find_elements(
                By.XPATH,
                "./..//div[@class='dropdown']/a[@id='nestedDropdownMenuButton']",
            )
        except:
            return None

    def getNestedDropdownElements(self, element):
        return element.find_elements(
            By.XPATH,
            ".//a[@class='dropdown-item nested']",
        )

    def getParentElement(self, element):
        return element.find_element(
            By.XPATH,
            "./..",
        )
