from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class CriteriaCatalogOverviewPage(object):

    def __init__(self, driver):
        """Constructor of CrteriaCatalogOverviewPage
        
        """
        self.driver = driver
    
    def getImplementedCriteriaCards(self):
        """Returns the implemented criteria cards.
        
        """
        card1 = self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogOverviewCard1,
        )
        card2 = self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogOverviewCard2,
        )
        return [card1, card2]


class CriteriaCatalogDetailsPage(object):

    def __init__(self, driver):
        """Constructor of CrteriaCatalogOverviewPage
        
        """
        self.driver = driver
    
    def getDetailsContentContainer(self):
        """Returns the details-content-container.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.criteriaCatalogDetailsContentContainer,
        )
    
    def getGetListOfAllHorizontalLineElements(self):
        """Returns a list of all horizontal line elements.
        
        """
        return self.driver.find_elements(
            By.XPATH,
            Locator.allHorizontalLineElements,
        )