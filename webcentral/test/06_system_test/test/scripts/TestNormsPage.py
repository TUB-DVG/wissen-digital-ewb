"""Test the Technical Standarts page

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
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.NormPage import NormPage
from Src.PageObject.Pages.Pagination import Pagination
from Src.PageObject.Pages.SearchPage import SearchPage

class TestNormsPage(WebDriverSetup):
    """Tests the 'Lastapproximation'-Tab
    
    """
    def testNormSearchBar(self):
        """Test the Norm-Search-Input Field 
        
        """
        
        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/norm")
        self._setLanguageToGerman()

        normPageObj = NormPage(self.driver)
        searchInputField = normPageObj.getSearchInputElement()

        searchInputField.send_keys("bisko")
        searchInputField.send_keys(Keys.RETURN)

        time.sleep(1)

        cardList = normPageObj.getCards() 

        self.assertEqual(
            len(cardList),
            1,
            "Number of Cards should be 1 after searching for 'bisko'!",
        )

        paginationObj = Pagination(self.driver)
        paginationStr = paginationObj.getPaginationCurrentSiteString()
        
        self.assertIn(
            "Seite 1 von 1",
            paginationStr.text,
            "Pagination string should be 'Seite 1 von 1' after searching for 'bisko'"
        )

        searchInputField.clear()
        time.sleep(1)

        cardList = normPageObj.getCards() 

        self.assertEqual(
            len(cardList),
            12,
            "Number of Cards should be 12 after deleting the Search-Filter...",
        )

    
    def testClickOnOneofTheCardsShown(self):
        """Click randomly on one of the cards and check if the right details-page is shown
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/norm")
        normPageObj = NormPage(self.driver)
        cardsOnPage = normPageObj.getCards()

        randomCard = random.choice(cardsOnPage)
        
        randomCardText = randomCard.text

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", randomCard)
        time.sleep(1)
        randomCard.click()

        time.sleep(1)

        self.assertIn(
            self.driver.title,
            randomCardText,
            f"Page Title should be '{randomCardText}', after clicking on the card with the same name!",
        )

