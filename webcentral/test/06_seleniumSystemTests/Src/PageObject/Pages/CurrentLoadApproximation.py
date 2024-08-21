from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Src.PageObject.Locators import Locator

class CurrentLoadApproximation(object):
    """
    
    """
    def __init__(self, driver):
        """
        """
        self.driver = driver

    def getHeadingOfPage(self):
        """Returns the h1-heading of the page.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.headingOfCurrentLoadApproxSite,    
        )

    def switchToIFrame(self):
        """Switches to the Iframe in which the react app is located.
        
        """

        iframeObj = self.driver.find_element(
            By.XPATH,
            Locator.currentLoadIFrame,
        )
        self.driver.switch_to.frame(iframeObj)