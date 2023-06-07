from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Src.PageObject.Locators import Locator

class StromlastApproximation(object):
    """
    
    """
    def __init__(self, driver):
        """
        """
        self.driver = driver

    def selectElementFromReactSelect(self):
        """
        
        """
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, 
                    Locator.selectTypeOfAppr,
                ),
            )
        ).click()
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH, 
                    "//div[contains(@class, 'select__menu')]/div[contains(@class, 'select__menu-list')]//div[contains(@class, 'select__option') and text()='Gewerbe Verbrauch Abend']"))).click()