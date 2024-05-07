"""

"""
import sys
sys.path.append(sys.path[0] + "/....")

from selenium import (
    webdriver,
)
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class NavBar(object):
    """
    
    """
    def __init__(self, driver):
        """
        
        """
        self.driver = driver

    def getLogo(self):
        """Returns the Logo from left upper side of page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.LogoImage,
            )
        except:
            return None

    def getNavStart(self):
        """Returns the TU-Logo from left upper side of page
        
        """
        try:
            return self.driver.find_element(
                By.XPATH,
                Locator.navStartButton,
            )
        except:
            return None

    def getNavToolList(self) -> None:
        """
        
        """
        try:
            return self.driver.find_element(
                By.XPATH, 
                Locator.toolListLink,
            )
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None
    
    def getNavTechFocus(self):
        """Returns the Webelement, which represents the
        'Technischer Fokus'-NavBar-Element
        
        """
        try:
            return self.driver.find_element(
                By.XPATH, 
                Locator.navTechFocus,
            )
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None

    def getNavDigitalApps(self):
        """Returns the Webelement, which represents the 'Daten'-NavBar-Element
        
        """
        try:
            return self.driver.find_element(
                By.XPATH, 
                Locator.digitalApps,
            )
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None

    def getNavDigitalTools(self):
        """Returns the Webelement, which represents the 'Daten'-NavBar-Element
        
        """
        try:
            return self.driver.find_element(
                By.XPATH, 
                Locator.toolListLink,
            )
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None
    
    def clickOnNegativeEnvironmentalImpact(self):
        """Returns the Webelement, which represents the 'Daten'-NavBar-Element
        
        """
        try:
            self.driver.find_element(
                By.XPATH, 
                f"//a[contains(@href, '{Locator.linkToNegativeEnviormentalImpact}')]",
            ).click()
            return
        except NoSuchElementException:
            print("Tool Link Element couldnt be located on webpage!")
            return None


    def getWeatherDataItem(self):
        """Returns wheater-data item in submenu under data-tab
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.weatherDataItem,
        )

    def getLastProfileItem(self):
        """Returns wheater-data item in submenu under data-tab
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.lastProfileItem,
        )