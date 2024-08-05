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
        self.driver.get(os.environ["siteUnderTest"] + "/criteriaCatalog/4")
        
        self.checkPageTitle("Betrieb und Betriebsoptimierung", "Betrieb und Betriebsoptimierung")
        self.checkNavBar("legal")
        
        # check if info icon is present on the right side of the root layer:
        detailPageObj = CriteriaCatalogDetailsPage(self.driver)
        rootDivElements = detailPageObj.getRootLayerElements()
        
        for divElement in rootDivElements:
            imgElementsInDiv = detailPageObj.getDescendantsByTagName(divElement, "img")
            self.assertEqual(len(imgElementInDiv), 2)
            self.assertTrue(imgElementInDiv[1].text == "", "No alt-text should be present for info image")
            self.assertTrue(imgElementInDiv[1].value_of_css_property("float") == "right")
            self.assertTrue(imgElementInDiv[1].value_of_css_property("margin-top") == "20px")
            
            # when the image is clicked, a grey box to the left of the image should be displayed:
            ## get the div element, which contains the grey box:
            greyBoxDiv = detailPageObj.getDescendantsByTagName(divElement, "div")
            self.assertEqual(len(greyBoxDiv), 1)
            self.assertTrue("show" not in greyBoxDiv[0].get_attribute("class"))
            self.assertTrue(not greyBoxDiv[0].is_displayed())

            # after clicking the info-icon, the grey box should be displayed:
            imgElementsInDiv[1].click()
            self.assertTrue("show" in greyBoxDiv[0].get_attribute("class"))
            self.assertTrue(greyBoxDiv[0].is_displayed())



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

    def testLiteratureElement(self):
        """Test if the description text under literature is shown below the literature button
        after clicking the literature button.

        """
        self.driver.get(os.environ["siteUnderTest"] + "/criteriaCatalog/4")

        criteriaCatalogObj = CriteriaCatalogDetailsPage(self.driver)
        literatureButton = criteriaCatalogObj.getLiteratureElement()
        
        self.scrollElementIntoViewAndClickIt(literatureButton)
        liParentOfButton = criteriaCatalogObj.getFirstAncestorByTagName(literatureButton, "li")

        # there should be one paragraph object containing the literature list:
        paragraphChilds = criteriaCatalogObj.getDescendantsByTagName(liParentOfButton, "p")
        self.assertEqual(len(paragraphChilds), 1)

    def testFullTextSearchAndAllCollapseButton(self):
        """Test if a full text search expands the accordion and marks the results and the collapse everything button resets the style
        """

        self.driver.get(os.environ["siteUnderTest"] + "/criteriaCatalog/4")
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
                buttonInnerHTML = button.get_attribute("innerHTML")
                if "<mark>Personen</mark>" in buttonInnerHTML:
                    foundMarkedPersonen = True
                else:
                    # breakpoint()
                    # raise AssertionError("The search result is not marked with yellow background-color.")
                    pass

        if not foundMarkedPersonen:
            raise AssertionError("The search result was not found.")
        
        # test if the collapse everything button resets the style:
        collapseButton = criteriaCatalogDetails.getCollapseEverythingButton()
        self.scrollElementIntoViewAndClickIt(collapseButton)
        for button in buttonElements:
            if button.value_of_css_property("background-color") == 'rgb(255, 255, 0)':
                raise AssertionError("The background-color of the buttons is not resetted.")
            if button.get_attribute("id") != "0" and button.value_of_css_property("display") != "none":
                raise AssertionError("The buttons are not collapsed.")
    
        # check if the info-icon on the right site is still displayed:
        rootDivElements = criteriaCatalogDetails.getRootLayerElements()
        for rootElement in rootDivElements:
            imgDescandants = criteriaCatalogDetails.getDescendantsByTagName(rootElement, "img")
            self.assertEqual(len(imgDescandants), 3)
            self.assertTrue("info_icon.svg" in imgDescandants[1].get_attribute("src"))
            self.assertTrue(imgDescandants[1].is_displayed())

            self.assertTrue("info_icon_selected.svg" in imgDescandants[2].get_attribute("src"))
            self.assertTrue(not imgDescandants[2].is_displayed(), "image_icon_selected should not be displayed.")


