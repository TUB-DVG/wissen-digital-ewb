from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class GenericPageObject:

    # def __init__(self, driver):
    #     """Constructor of GenericPageObject"""
    #     self.driver = driver

    def getAllElementsOfTagname(self, tagname: str) -> list:
        """Returns a list of all elements with the given tagname."""
        return self.driver.find_elements(
            By.TAG_NAME,
            tagname,
        )

    def getDescendantsByTagName(self, element, tagName):
        """Returns the div-element, which wraps the content of the page"""
        try:
            # breakpoint()
            return element.find_elements(By.XPATH, ".//" + tagName)

        except:
            return None

    def getFirstAncestorByTagName(self, element, tagName):
        """Get the first parent, which has the tag `tagName`"""
        return element.find_element(By.XPATH, f"ancestor::{tagName}")

    def getDescendantsByClass(self, element, className):
        """Returns the div-element, which wraps the content of the page"""
        return element.find_elements(By.CSS_SELECTOR, f".{className}")

    def getDirectChildren(self, element):
        """Returns the direct children of the given element"""
        try:
            return element.find_elements(By.XPATH, "./*")
        except:
            return None

    def getPreviousSiblingOfTagName(self, element, tagName):
        """Returns the previous sibling of the given element"""
        try:
            return element.find_element(By.XPATH, "preceding-sibling::" + tagName)
        except:
            return None

    def getFollowingSiblingOfTagName(self, element, tagName):
        """Returns the following sibling of the given element"""
        try:
            return element.find_element(By.XPATH, "following-sibling::" + tagName)
        except:
            return None

    def getAllSiblingsOfTagname(self, element, tagname: str):
        """ """

        return element.find_elements(By.XPATH, f"following-sibling::{tagname}")

    def getContentDiv(self):
        """Returns the div-element, which wraps the content of the page"""
        try:
            return self.driver.find_element(
                By.XPATH,
                ".//div[contains(@class, 'content')]",
            )
        except:
            return None

    def getNextSibling(self, domObj):
        """Return the next DOM-sibling of the `domObj`

        domObj: WebElement
            The WebElement of which the next sibling should be returned

        Returns:
        -------
        WebElement
            The next sibling of the `domObj`
        """

        return domObj.find_element(By.XPATH, "following-sibling::*")

    def getAllElementsOfClass(self, className: str) -> list:
        """Returns a list of all elements with the given class."""
        return self.driver.find_elements(
            By.CLASS_NAME,
            className,
        )

    def waitUntilElementIsLoaded(self, element):
        """Poll for the element for 10 seconds until its loaded."""
        wait = WebDriverWait(self.driver, timeout=10)
        wait.until(lambda d: element.is_displayed())

    def getBoxes(self):
        """Return boxes from the overview-page."""
        return self.driver.find_elements(By.XPATH, "//div[contains(@class, 'box ')]")
