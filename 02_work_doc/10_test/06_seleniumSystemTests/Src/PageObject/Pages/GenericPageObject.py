from selenium import (
    webdriver, )
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class GenericPageObject(object):

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
