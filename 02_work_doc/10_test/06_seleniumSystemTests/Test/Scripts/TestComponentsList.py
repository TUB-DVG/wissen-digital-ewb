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

class TestComponentsList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page 

    """
    def testComponentPageExists(self):
        """Test if the Components-List Page exists and is accessible via url and navbar

        """
        self.driver.get(os.environ["siteUnderTest"] + "pages/componentsList")
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative umweltwirkungen" in self.driver.title) 
        
        self.driver.get(os.environ["siteUnderTest"])
        navBar = NavBar(self.driver)
        navBar.clickOnNegativeEnvironmentalImpact()
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative umweltwirkungen" in self.driver.title)
