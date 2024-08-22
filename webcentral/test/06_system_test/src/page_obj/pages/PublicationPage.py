"""

"""
import sys
sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Src.PageObject.Locators import Locator

class PublicationPage(object):
    """
    
    """

    def __init__(self, driver):
        """
        
        """
        self.driver = driver
    
    def getPublicationContainer(self):
        """Return the most outer container of the publications-page to check
        if the border color matches the expected color.

        """
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, Locator.publicationContainer)))
        return element
    
    def getPublicationSearchBoxForm(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxForm)

    def getPublicationSearchBoxInput(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxInput)
    
    def getPublicationSearchBoxSelect(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxSelect)
    
    def getPublicationSearchBoxSubmit(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxSubmit)
    
    def getPublicationSearchBoxReset(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationSearchBoxReset)
    
    def getPublicationRemoveFocusFilter(self):
        """Return the publication search box div, to check if it has the correct color.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationCloseButton)
    
    def getPublicationPaginatorObjects(self):
        """Return a list of all paginator objects, each of which represents a publication.

        """
        return self.driver.find_elements(By.CLASS_NAME, Locator.paginatorObjects)
    
    def getTitleOfPaginationObject(self, paginatorObject) -> str:
        """Return the title of `paginatorObject`

        The title of `paginatorObject` lies inside a h3-tag and can be accessed by
        searching in the child-elements of `paginatorObject`.

        paginatorObject: WebElement
            Selenium-WebElement, which represents a item in the paginator.

        """
        return paginatorObject.find_element(By.XPATH, Locator.paginatorObjectTitle).text

    def getAuthorsOfPaginationObject(self, paginatorObject) -> str:
        """Return the Authors of `paginatorObject` of type Publication.

        The authors of `paginatorObject` lie inside a p-tag and can be accessed by
        searching in the child-elements of `paginatorObject`.

        paginatorObject: WebElement
            Selenium-WebElement, which represents a item in the paginator.

        """
        return paginatorObject.find_elements(By.XPATH, Locator.paginatorObjectAuthorsAndType)[0].text

    def getTypeOfPaginationObject(self, paginatorObject) -> str:
        """Return the Type of `paginatorObject` of type Publication.

        The Type of `paginatorObject` lie inside a p-tag and can be accessed by
        searching in the child-elements of `paginatorObject`.

        paginatorObject: WebElement
            Selenium-WebElement, which represents a item in the paginator.

        """
        return paginatorObject.find_elements(By.XPATH, Locator.paginatorObjectAuthorsAndType)[1].text

    def getPublicationDetailsPageTitle(self):
        """Return the title of the publication details page.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationDetailsPageTitle).text

    def getAuthorsOfPublicationOnDetailsPage(self):
        """Return the authors of the publication on the details page.

        """
        return self.driver.find_element(By.XPATH, Locator.publicationDetailsPageAuthorsHeading).find_element(By.XPATH, Locator.publicationDetailsPageAuthorsValues).text

    def getPublicationDetailsPageType(self):
        """Return the title of the publication details page.

        """
        return self.driver.find_element(By.CLASS_NAME, Locator.publicationDetailsPageType).text

    def getListingElements(self):
        """Return all listing results for publications
        """
        publicationListingElements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'card ')]")
        return publicationListingElements
    
    def getFokusForElement(self, element) -> str:
        return element.find_elements(By.XPATH, ".//p")[2].text
