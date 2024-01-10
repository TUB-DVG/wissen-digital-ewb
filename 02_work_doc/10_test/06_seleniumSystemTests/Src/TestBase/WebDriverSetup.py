"""

"""
import os
import unittest
import urllib3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
class WebDriverSetup(unittest.TestCase):
    def setUp(self):
        """Start a webdriver-instance for every test in headless-mode.
        The headles browser instance is a firefox-instance and has the
        dimensions 1920x1080.
        
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        firefoxOptions = Firefox_Options()
        firefoxOptions.add_argument("--window-size=1920,1080")
        firefoxOptions.add_argument("start-maximised")
        # firefoxOptions.add_argument("--width=1920")
        # firefoxOptions.add_argument("--height=1080")
        if os.environ.get("HEADLESS") == "1":
            firefoxOptions.headless = True
        self.driver = webdriver.Firefox(options=firefoxOptions)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
 
    def tearDown(self):
        """Close the browser Window of every test.
        
        """
        if (self.driver != None):
            print("Cleanup of test environment")
            self.driver.close()
            self.driver.quit()

    def scrollElementIntoViewAndClickIt(self, element):
        """Scroll the element into the view of the browser-window.
        
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.element = element
        wait = WebDriverWait(self.driver, 10)  # waits for 10 seconds
        wait.until(self._elementIsClickable)

    def _elementIsClickable(self, driver):
        """Check if the element is clickable.
        
        """
        try:
            self.element.click()
        except:
            return False
        return True