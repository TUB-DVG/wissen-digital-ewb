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
from selenium.webdriver.common.action_chains import ActionChains

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.TestWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AdminPage import AdminPage

class TestAdminPage(TestWebcentral):

    def testLoginAsAdmin(self):
        """Login as Admin with the credentials from .env
        
        """

        self.driver.get(os.environ["siteUnderTest"] + "/admin")

        self.assertEqual(
            "Log in | Django site admin",
            self.driver.title,
            "Site Title should be 'Log in | Django site admin'!",
        )

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        adminPageObj = AdminPage(self.driver)
        usernameInput = adminPageObj.getUsernameInput()
        usernameInput.send_keys(username)

        passwordInput = adminPageObj.getPasswordInput()
        passwordInput.send_keys(password)

        adminPageObj.getLoginSubmit().click()

        self.assertEqual(
            "Site administration | Django site admin",
            self.driver.title,
            "Page Title should be 'Site administration | Django site admin', but its not!",
        )
        


