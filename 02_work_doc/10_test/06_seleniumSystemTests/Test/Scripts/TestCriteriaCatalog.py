import os
from random import choice
import sys
sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.CriteriaCatalog import (
    CriteriaCatalogOverviewPage,
    CriteriaCatalogDetailsPage,
)

class TestCriteriaCatalog(WebDriverSetup):
    """Represent the Selenium-Test of the Criteria-Catalog Page 

    """
    
    def testOverviewPage(self):
        """Test the design and structure of the criteria-catalog overview page 

        """
        self.driver.get(os.environ["siteUnderTest"] + "/en/pages/criteriaCatalog/")
        
        self.checkPageTitle("Kriterienkatalog - Übersicht", "Catalog of criteria - Overview")
        self.checkNavBar("legal")

    # def testColorOfLines(self):
    #     """Tests if the color of the lines in the Criteria-Catalog is correct.

    #     """

        # # click one of the cards of the criteriaCatalog-overview page:
        # # at the moment only the upper 2 cards lead to a functioning page
        # self.driver.get(os.environ["siteUnderTest"] + "pages/criteriaCatalog")
        # criteriaCatalogOverview = CriteriaCatalogOverviewPage(self.driver)
        # implementedCriteriaCards = criteriaCatalogOverview.getImplementedCriteriaCards()
        # chosenCard = choice(implementedCriteriaCards)
        # chosenCard.click()

        # # test if the horizontal lines have the same color like the box-border:
        # criteriaCatalogDetails = CriteriaCatalogDetailsPage(self.driver)
        # detailsContentContainer = criteriaCatalogDetails.getDetailsContentContainer()
        # breakpoint()
        # horizontalLineElements = criteriaCatalogDetails.getGetListOfAllHorizontalLineElements()

    def testFullTextSearchAndAllCollapseButton(self):
        """Test if a full text search expands the accordion and marks the results and the collapse everything button resets the style
        """

        self.driver.get(os.environ["siteUnderTest"] + "/criteriaCatalog/Profilbildung")
        criteriaCatalogDetails = CriteriaCatalogDetailsPage(self.driver)
        searchField = criteriaCatalogDetails.getSearchField()
        searchField.send_keys("Personen")
        searchField.send_keys(Keys.RETURN)

        # test if the accordion is expanded:
        detailsContentContainer = criteriaCatalogDetails.getDetailsContentContainer()
        buttonElements = criteriaCatalogDetails.getAllButtonElements(detailsContentContainer)
        foundMarkedPersonen = False

        for button in buttonElements:
            if "Personen" in button.text:
                if button.value_of_css_property("background-color") == "rgb(255, 255, 0)":
                    foundMarkedPersonen = True
                else:
                    raise AssertionError("The search result is not marked with yellow background-color.")

        if not foundMarkedPersonen:
            raise AssertionError("The search result was not found.")
        
        # test if the collapse everything button resets the style:
        collapseButton = criteriaCatalogDetails.getCollapseEverythingButton()
        collapseButton.click()
        for button in buttonElements:
            if button.value_of_css_property("background-color") == 'rgb(255, 255, 0)':
                raise AssertionError("The background-color of the buttons is not resetted.")
            if button.get_attribute("id") != "0" and button.value_of_css_property("display") != "none":
                raise AssertionError("The buttons are not collapsed.")
        
