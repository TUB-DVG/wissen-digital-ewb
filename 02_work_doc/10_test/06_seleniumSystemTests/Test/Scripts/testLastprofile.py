"""This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

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

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.testWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.loginPage import LoginPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.lastprofile import Lastprofile

class TestLastprofileTab(TestWebcentral):
    """Tests the 'Lastapproximation'-Tab
    
    """
    
    def testLastprofileApprox(self):
        """Clicks on 'Approximation der Stromlast' and tests the tool
        
        """
        self.login()
        self.driver.get("http://127.0.0.1:8070/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)

        lastprofilePage.getLinkToStromlastTool().click()

        self.assertEqual(
            "Stromlastprofil",
            self.driver.title,
            "Page should be 'Stromlastprofile', but its not!",
        )

