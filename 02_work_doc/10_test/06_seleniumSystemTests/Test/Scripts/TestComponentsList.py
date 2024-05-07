import os
from random import choice
import sys
sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.NegativeEnvironmentalImpacts import NegativeEnvironmentalImpacts

class TestComponentsList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page 

    """
    def testComponentPageExists(self):
        """Test if the Components-List Page exists and is accessible via url and navbar

        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ")
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative Umweltwirkungen" in self.driver.title) 
        
        self.driver.get(os.environ["siteUnderTest"])
        navBar = NavBar(self.driver)
        linkToPage = navBar.returnNegativeEnvironmentalImpactLink()
        # breakpoint()
        self.scrollElementIntoView(linkToPage[1])
        linkToPage[1].click()
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative Umweltwirkungen" in self.driver.title)

    def testStructureOfPage(self):
        """Test if a div-element is present, in which the content is wraped

        This test-method is part of the test-first-dev cycle. It tests if a outer 
        div exists, which is of css-class `content`. Inside this div, there should be
        a div-wrapper for the description text, which is again composed of a heading and the
        text. In the bottom part of the page, there should be 2 boxes, which further contents.
        """

        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ")
        impactsObj = NegativeEnvironmentalImpacts(self.driver)
        contentDiv = impactsObj.getContentDiv()


        self.assertIsNotNone(contentDiv)
    
        descriptionHeadingDiv = impactsObj.getDescriptionHeadingDiv()
        self.assertIsNotNone(descriptionHeadingDiv)