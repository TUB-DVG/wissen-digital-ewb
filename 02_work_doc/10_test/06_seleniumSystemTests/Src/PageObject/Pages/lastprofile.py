from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class Lastprofile(object):
    """
    
    """
    def __init__(self, driver):
        """Constructor of the Lastprofile-Class
        
        """
        self.driver = driver

    def getLinkToStromlastTool(self):
        """Returns the link to the Stromlast-Approximation tool.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.stromlastApprLink,
        )