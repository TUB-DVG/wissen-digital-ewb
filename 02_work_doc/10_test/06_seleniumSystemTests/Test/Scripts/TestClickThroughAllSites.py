"""Clicks though all Sites and tests if they load.

This module acts as system test of for the whole webcentral-page.
It clicks through all pages and checks if they are accessible.
"""
import pdb
import sys
sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from selenium import (
    webdriver,

)
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.TestWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar

class TestClickThroughSites(TestWebcentral):
    """
    
    """

    def testClickNavbar(self) -> None:
        """
        
        """
        self.driver.get("http://127.0.0.1:8070/")
        self.driver.set_page_load_timeout(30)

        navBar = NavBar(self.driver)

        tuLogoLink = navBar.getTULogo()
        self.assertIsNotNone(
            tuLogoLink,
            "The TU-Logo, which is a link at the same time is not shown! ",
        )

        tuLogoLink.click()
        

        self.assertEqual(
            "Wissensplattform - Digitalisierung Energiewendebauen",
            self.driver.title,
            "After clicking TU-Logo, Browser should be redirected to Startpage, but was not!",
        )

        navStartbutton = navBar.getNavStart()  
        self.assertIsNotNone(
            navStartbutton,
            "The Nav-Bar has no Start-Button!",
        )

        navStartbutton.click()

        self.assertEqual(
            "Wissensplattform - Digitalisierung Energiewendebauen",
            self.driver.title,
            "After clicking Start in Nav-Bar, Browser should be redirected to Startpage, but was not!",
        )

        navDataWebelement = navBar.getNavData()

        self.assertIsNotNone(
            navDataWebelement,
            "The Nav-Bar has no Daten-Button!",
        )
        navDataWebelement.click()

        self.assertEqual(
            "Daten",
            self.driver.title,
            "After clicking 'Daten' in Nav-Bar, Browser should be redirected to Daten-page, but was not!",
        )      

        navDigitalAppsWebelement = navBar.getNavDigitalApps()

        self.assertIsNotNone(
            navDigitalAppsWebelement,
            "The Nav-Bar has no Daten-Button!",
        )

        navDigitalAppsWebelement.click()

        self.assertEqual(
            "Wissensplattform",
            self.driver.title,
            "After clicking 'Digitale Anwendungen' in Nav-Bar, Browser should be redirected to 'Digitale Anwendungen'-page, but was not!",
        )      

        navToolListWebelement = navBar.getNavDigitalTools()

        self.assertIsNotNone(
            navToolListWebelement,
            "The Nav-Bar has no 'Digitale Werkzeuge'-Button!",
        )

        navToolListWebelement.click()

        self.assertEqual(
            "Überblick über die Anwendungen",
            self.driver.title,
            "After clicking 'Digitale Werkzeuge' in Nav-Bar, Browser should be redirected to 'Digitale Werkzeuge'-page, but was not!",
        )      

    def testHoverOverDataAndClickWeatherdata(self):
        """Tests if a Sub-menu is displayed, when hovering over Data-NavBar-item. 
        
        """
        self.driver.get("http://127.0.0.1:8070/")
        navBar = NavBar(self.driver)
        dataItem = navBar.getNavData()
  
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(dataItem).perform()
        time.sleep(1)
        weatherDataItem = navBar.getWeatherDataItem()
        
        
        weatherDataItem.click()

        self.assertEqual(
            "Überblick über die Wetterdaten-Services",
            self.driver.title,
            "Page should be weatherdata-page, but it is not!",
        )

    def testHoverOverDataAndClickLastprofiles(self):
        """Tests if a Sub-menu is displayed, when hovering over Data-NavBar-item. 
        
        """
        self.driver.get("http://127.0.0.1:8070/")
        navBar = NavBar(self.driver)
        dataItem = navBar.getNavData()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(dataItem).perform()
        time.sleep(1)
        
        lastprofileItem = navBar.getLastProfileItem()
        lastprofileItem.click()

        
        self.assertEqual(
            "Überblick über die Lastprofil Approximation",
            self.driver.title,
            "Page should be lastprofile-page, but it is not!",
        )
    
