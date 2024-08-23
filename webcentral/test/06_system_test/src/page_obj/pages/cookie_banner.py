from selenium.webdriver.common.by import By

from src.page_obj.locators import Locator

class CookieBanner(object):
    """
    
    """
    def __init__(self, driver):
        """
        """
        self.driver = driver

    def getCookieAcceptanceButton(self):
        """Returns the cookie acceptance button, on cookie banner
        
        """
        return self.driver.find_element(
            By.XPATH, 
            Locator.cookieButton,
        )
