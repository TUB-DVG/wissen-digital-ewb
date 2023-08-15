"""This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

"""
import sys
import time
import os
import random

sys.path.append(sys.path[0] + "/...")

from selenium import (
    webdriver,

)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.TestWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.lastprofile import Lastprofile
from Src.PageObject.Pages.CurrentLoadApproximation import (
    CurrentLoadApproximation,
)
from Src.PageObject.Pages.HeatApproximation import HeatApproximation
from Src.PageObject.Pages.cookieBanner import CookieBanner

class TestLastprofileTab(TestWebcentral):
    """Tests the 'Lastapproximation'-Tab
    
    """
    
    def testLastprofileApprox(self):
        """Clicks on 'Approximation der Stromlast' and tests the tool
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)

        lastProfileLink = lastprofilePage.getLinkToStromlastTool()
        self.driver.execute_script("var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));", lastProfileLink)
        time.sleep(1)
        lastProfileLink.click()

        self.assertEqual(
            "Stromlastprofil",
            self.driver.title,
            "Page should be 'Stromlastprofile', but its not!",
        )

        currentApproObj = CurrentLoadApproximation(self.driver)

        time.sleep(1)
        currentApproObj.switchToIFrame()
        headingElement = currentApproObj.getHeadingOfPage()

        self.assertEqual(
            headingElement.text,
            "Stromlast Approximation",
            "Heading Title should be Stromlast Approximation, but its not!",
        )
        
    def testHeatApproximation(self):
        """Tests if 'Heat Approximation' is reachable
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)

        linkToHeatApprox = lastprofilePage.getLinkForHeatApproxTool()

        cookieBanner = CookieBanner(self.driver)
        cookieBannerButn = cookieBanner.getCookieAcceptanceButton()  
        time.sleep(2)
        cookieBannerButn.click()

        actions = ActionChains(self.driver)
        try:
            actions.move_to_element(linkToHeatApprox).perform()
        except MoveTargetOutOfBoundsException as e:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", linkToHeatApprox)
        time.sleep(1)

        linkToHeatApprox.click()
        self.assertEqual(
            "Waermelastprofil",
            self.driver.title,
            "After clicking on Heat-Approximation Link, page should be Heat-Approximation. But its not!",
        )

        currentApproObj = HeatApproximation(self.driver)
        
        time.sleep(1)
        currentApproObj.switchToIFrame()
        headingElement = currentApproObj.getHeadingOfPage()

        self.assertEqual(
            headingElement.text,
            "Wärmelast Approximation",
            "Heading Title should be Wärmelast Approximation, but its not!",
        )

    
    def testLinksOnSite(self):
        """Tests, if the links present on the website lead to the right websites.
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)

        weatherServiceLink = lastprofilePage.getWeatherServiceLink()

        actions = ActionChains(self.driver)
        try:
            actions.move_to_element(weatherServiceLink).perform()
        except MoveTargetOutOfBoundsException as e:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", weatherServiceLink)
        time.sleep(1)
        
        weatherServiceLink.click()

        self.assertEqual(
            "GitHub - earthobservations/wetterdienst: Open weather data for humans.",
            self.driver.title,
            "After clicking on Wetterdienst-Link, the github-page of wetterdienst should appear!",
        )

        self.driver.back()

        loadProfileLink = lastprofilePage.getLoadProfileLink()
        loadProfileLink.click()

        self.assertEqual(
            "Standardlastprofile Strom | BDEW",
            self.driver.title,
            "After clicking on Standard Loadprofile-Link, the page of bdew should appear!",
        )

    def testDataLoadsOnStromlast(self):
        """Test the Stromlast App, if a graph is loaded.
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/stromlast")
        lastprofilePage = Lastprofile(self.driver)
        selectPlaceholderToHoverOver = lastprofilePage.getReactSelectPlaceholder()
        


