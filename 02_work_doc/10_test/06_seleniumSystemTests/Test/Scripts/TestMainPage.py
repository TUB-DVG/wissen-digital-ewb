"""Test the Userinterface of Main-Page

This class is part of the Selenium-Test of Webcentral. 
It tests the first page, which is accessed when browsing to
https://wissen-digital-ewb.de.

"""
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Test.Scripts.TestWebcentral import TestWebcentral
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AboutPage import AboutPage

class TestMainPage(TestWebcentral):
    """Testclass for MainPage-Test

    Inherit from TestWebcentral. There methods should be implemented,
    which are relevant for all Test-Classes (like the login-functionality,
    which is no longer needed.)
    
    """
    def testImpressum(self):
        """Test if on click of Impressum link on the bottom of the site
        the Impressum page opens, which is located on $siteunderTtest + /pages/Impressum
        
        """
        self.driver.get(os.environ["siteUnderTest"])

        startPageObj = StartPage(self.driver)
        impressumLinkElement = startPageObj.getImpressumLink()
        # self.driver.implicitly_wait(10)
        # ActionChains(self.driver).move_to_element(impressumLinkElement).perform()
        self.driver.execute_script("arguments[0].scrollIntoView();", impressumLinkElement)
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(impressumLinkElement)).click()
        time.sleep(1)
        impressumLinkElement.click()
        time.sleep(1)

        self.assertEqual(
            self.driver.title,
            "Impressum",
            "Page should be Impressum, but its not!"
        )

    def testSearchField(self):
        """Test the searchfield on the startpage

        The Test is done by first insert 'Bim' into the input-field. After pushing Return, 
        BIM2SIM should be in the Result.
        
        """
        self.driver.get(os.environ["siteUnderTest"])
        startPageObj = StartPage(self.driver) 
        searchInputField = startPageObj.getSearchInputField()
        searchInputField.send_keys("Bim")
        searchInputField.send_keys(Keys.RETURN)
        time.sleep(1)
        foundInstanceOfBIM2SIM = False
        listOfRowsInResultsTable = startPageObj.getSearchResults()
        for rowElement in listOfRowsInResultsTable:
            if rowElement.text.find("BIM2SIM") >= 0:
                foundInstanceOfBIM2SIM = True
                firstColumnWebelement = startPageObj.getFirstColumn(rowElement)
                firstColumnWebelement.click()
                time.sleep(1)
                self.assertEqual(
                    "BIM2SIM",
                    self.driver.title,
                    "After clicking of the search result, which contains 'BIM2SIM', Page-Title should be BIM2SIM, but its not...",
                )
                break
        
        self.assertTrue(
            foundInstanceOfBIM2SIM, 
            "BIM2SIM is not in results! Check the search...",
        )

        # back to search results:
        self.driver.back()
        listOfRowsInResultsTable = startPageObj.getSearchResults()
        listOfTableRows = []
        for indexTable, rowElement in enumerate(listOfRowsInResultsTable):
            listOfRowsInResultsTable = startPageObj.getSearchResults()
            rowElement = listOfRowsInResultsTable[indexTable]
            # breakpoint()
            if rowElement.text.find("Forschungsprojekt") >= 0:
            
                self.driver.execute_script("arguments[0].scrollIntoView();", rowElement)
                childRowElement = startPageObj.getChildEbElement(rowElement)
                # breakpoint()
                childRowElement.click()
                time.sleep(1)
                self.assertTrue(
                    "Energiewendebauen" in self.driver.title,
                    "After clicking Forschungsprojekt it should redirect to Energiewendebauen page!",
                )
                self.driver.back()
        
    def testIfLinkToBuisnessAppsWorks(self):
        """Test if one can navigate from Main-Page to buisness-application site
        
        """

        startPageObj = StartPage(self.driver)
        linkToBuisnessApps = startPageObj.getLinkToBuisnessApps()        


        linkToBuisnessApps.click()

        time.sleep(1)
        
        self.assertEqual(
            self.driver.title,
            "Überblick über die Geschäftsmodellanwendungen",
            "Website should be 'Geschäftsmodellanwendungen', but its not!",
        )