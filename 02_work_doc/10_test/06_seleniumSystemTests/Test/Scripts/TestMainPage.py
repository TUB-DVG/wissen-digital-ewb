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
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AboutPage import AboutPage
from Src.PageObject.Pages.cookieBanner import CookieBanner

class TestMainPage(WebDriverSetup):
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
        checkedScientificProjects = 0
        for indexTable, rowElement in enumerate(listOfRowsInResultsTable):
            listOfRowsInResultsTable = startPageObj.getSearchResults()
            rowElement = listOfRowsInResultsTable[indexTable]
            if rowElement.text.find("Forschungsprojekt") >= 0:
                checkedScientificProjects += 1
                self.driver.execute_script("arguments[0].scrollIntoView();", rowElement)
                childRowElement = startPageObj.getChildEbElement(rowElement)
                self.driver.execute_script("var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));", rowElement)
                childRowElement.click()
                time.sleep(1)
                self.assertTrue(
                    "Energiewendebauen" in self.driver.title,
                    "After clicking Forschungsprojekt it should redirect to Energiewendebauen page!",
                )
                self.driver.back()
            if checkedScientificProjects == 2:
                break
        listOfRowsInResultsTable = startPageObj.getSearchResults()
        textOnFirstSearchResult = listOfRowsInResultsTable[1].text
        # on first site, "next" and "last" should be present:
        listOfNextElement = startPageObj.getNextElementInList()
        self.assertEqual(
            len(listOfNextElement),
            1,
            "next-search-results-page should be present, but it is not!",
        )
        listOfPreviousElement = startPageObj.getPreviousElementInList()
        self.assertEqual(
            len(listOfPreviousElement),
            0,
            "previous-search-results-page should not be present, but it is!",
        )
        listOfFirstElement = startPageObj.getFirstElementInList()
        self.assertEqual(
            len(listOfFirstElement),
            0,
            "First-search-results-page should not be present, but it is!",
        )
        listOfLastElement = startPageObj.getLastElementInList()
        self.assertEqual(
            len(listOfLastElement),
            1,
            "last-search-results-page should be present, but it is not!",
        )
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerObj.getCookieAcceptanceButton().click()
        time.sleep(1)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", listOfNextElement[0])
        time.sleep(1)
        listOfNextElement[0].click()
        time.sleep(1)
        resultsOnNextSite = startPageObj.getSearchResults()
        self.assertNotEqual(
            resultsOnNextSite[1].text,
            textOnFirstSearchResult,
            "The results on 2 different sites should differ!",
        )
        listOfNextElement = startPageObj.getNextElementInList()
        self.assertEqual(
            len(listOfNextElement),
            1,
            "next-search-results-page should be present, but it is not!",
        )
        listOfPreviousElement = startPageObj.getPreviousElementInList()
        self.assertEqual(
            len(listOfPreviousElement),
            1,
            "previous-search-results-page should be present, but it is not!",
        )
        listOfFirstElement = startPageObj.getFirstElementInList()
        self.assertEqual(
            len(listOfFirstElement),
            1,
            "First-search-results-page should be present, but it is not!",
        )
        listOfLastElement = startPageObj.getLastElementInList()
        self.assertEqual(
            len(listOfLastElement),
            1,
            "last-search-results-page should be present, but it is not!",
        )
        currentPageNumberElement = startPageObj.getCurrentSearchResultNumber()
        self.assertIn(
            "Seite 2",
            currentPageNumberElement.text,
            "Current Page Number should say 'Seite 2'"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", listOfPreviousElement[0])
        time.sleep(1)
        listOfPreviousElement[0].click()
        currentPageNumberElement = startPageObj.getCurrentSearchResultNumber()
        self.assertIn(
            "Seite 1",
            currentPageNumberElement.text,
            "Current Page Number should say 'Seite 1'"
        )       


        
    def testIfLinkToBuisnessAppsWorks(self):
        """Test if one can navigate from Main-Page to buisness-application site
        
        """
        self.driver.get(os.environ["siteUnderTest"])
        startPageObj = StartPage(self.driver)
        linkToBuisnessApps = startPageObj.getLinkToBuisnessApps()    
            
        self.driver.execute_script("arguments[0].scrollIntoView();", linkToBuisnessApps)
        
        time.sleep(1)
        linkToBuisnessApps.click()

        time.sleep(1)
        
        self.assertEqual(
            self.driver.title,
            "Überblick über die Geschäftsmodellanwendungen",
            "Website should be 'Geschäftsmodellanwendungen', but its not!",
        )

    def testLinkToTechnicalSTandarts(self):
        """Test if the Technical Standarts Link is working by clicking on it and 
        checking the page-title on the next site
        
        """
        self.driver.get(os.environ["siteUnderTest"])

        startPAgeObj = StartPage(self.driver)
        linkToTechnicalStandarts = startPAgeObj.getLinkToTechnicalStandarts()
        self.driver.execute_script("arguments[0].scrollIntoView();", linkToTechnicalStandarts)
        time.sleep(1)
        linkToTechnicalStandarts.click()
        self.assertEqual(
            self.driver.title,
            "Überblick über die technischen Standards",
            "Page should be technical-standarts-page after clicking on link on main-page...",
        )
    