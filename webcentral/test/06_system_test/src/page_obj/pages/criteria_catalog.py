from selenium.webdriver.common.by import By

from src.page_obj.locators import Locator
from src.page_obj.pages.generic_page_obj import GenericPageObject


class CriteriaCatalogOverviewPage(GenericPageObject):

    def __init__(self, driver):
        """Constructor of CrteriaCatalogOverviewPage"""
        self.driver = driver

    def getImplementedCriteriaCards(self):
        """Returns the implemented criteria cards."""
        card1 = self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogOverviewCard1,
        )
        card2 = self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogOverviewCard2,
        )
        return [card1, card2]


class CriteriaCatalogDetailsPage(GenericPageObject):

    def __init__(self, driver):
        """Constructor of CrteriaCatalogOverviewPage"""
        self.driver = driver

    def getGreyBoxForRootDiv(self, rootElement):
        """Return greyBox for the specified `rootElement`"""
        topicIdOfRootElement = self.getDescendantsByTagName(
            rootElement, "button"
        )[0].get_attribute("topicId")
        return self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class, 'grey-box') and @topicId='{topicIdOfRootElement}']",
        )

    def getDetailsContentContainer(self):
        """Returns the details-content-container."""
        return self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogDetailsContentContainer,
        )

    def getGetListOfAllHorizontalLineElements(self):
        """Returns a list of all horizontal line elements."""
        return self.driver.find_elements(
            By.XPATH,
            Locator.allHorizontalLineElements,
        )

    def getSearchField(self):
        """Returns the search field."""
        return self.driver.find_element(
            By.XPATH,
            Locator.fullTextSearchField,
        )

    def getCollapseEverythingButton(self):
        """Returns the collapse-everything-button."""
        return self.driver.find_element(
            By.XPATH,
            Locator.collpaseEveryThingButton,
        )

    def getAllButtonElements(self, parent):
        """Returns all child-buttons."""
        return parent.find_elements(
            By.TAG_NAME,
            "button",
        )

    def getRootLayerElements(self):
        """Return the root-layer elements of each tree(the elements, which are displayed
        when the catalog is loaded.)

        """
        return self.driver.find_elements(By.XPATH, "//div[@id='0']")

    def getLiteratureElement(self):
        """Return the literature button-element from the criteriaCatalog detail page"""
        return self.driver.find_element(By.XPATH, "//button[@topicId='1778']")

    def getNormsInfoContainers(self):
        """ """
        return self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'grey-box')]"
        )
