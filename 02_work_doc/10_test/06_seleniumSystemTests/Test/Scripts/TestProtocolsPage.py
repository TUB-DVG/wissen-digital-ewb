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
from Src.PageObject.Pages.ProtocolPage import ProtocolPage
from Src.PageObject.Pages.Pagination import Pagination
from Src.PageObject.Pages.SearchPage import SearchPage

class TestProtocolsPage(WebDriverSetup):
    """Tests the 'Lastapproximation'-Tab
    
    """
    def testProtocolsSearchBar(self):
        """Test the Norm-Search-Input Field 
        
        """
        
        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/protocol")

        protocolPageObj = ProtocolPage(self.driver)
        searchInputField = protocolPageObj.getSearchInputElement()

        searchInputField.send_keys("dali")
        searchInputField.send_keys(Keys.RETURN)

        cardList = protocolPageObj.getCards() 

        self.assertEqual(
            len(cardList),
            1,
            "Number of Cards should be 1 after searching for 'bisko'!",
        )

        searchInputField.clear()
        searchInputField.send_keys(Keys.RETURN)

        cardList = protocolPageObj.getCards() 

        self.assertEqual(
            len(cardList),
            12,
            "Number of Cards should be 12 after deleting the Search-Filter...",
        )
    
    def testClickOnOneofTheCardsShown(self):
        """Click randomly on one of the cards and check if the right details-page is shown
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/TechnicalStandards/protocol")
        protocolPageObj = ProtocolPage(self.driver)
        cardsOnPage = protocolPageObj.getCards()

        randomCard = random.choice(cardsOnPage)
        
        randomCardText = randomCard.text

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", randomCard)
        time.sleep(1)
        randomCard.click()

        time.sleep(3)

        self.assertEqual(
            self.driver.title,
            randomCardText,
            f"Page Title should be '{randomCardText}', after clicking on the card with the same name!",
        )

    def testFilteringAndPagination(self):
        """Test if the pagination works, when selecting an filter from one of the select elements
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        self._setLanguageToGerman()

        searchBarPageObj = SearchPage(self.driver)
        paginationObj = Pagination(self.driver)

        multiselectInputs = searchBarPageObj.getMultiSelectClickables()
        chosenSelect = choice(multiselectInputs)
        chosenSelect.click()

        divOfOpenedDropDown = self.driver.find_element(By.XPATH, "//div[@class, 'dropdown-menu w-100']")
        dropdownElements = searchBarPageObj.getDescendantsByClass(divOfOpenedDropDown, "dropdown-item")
        chosenFilterItem = choice(dropdownElements)
        chosenFilterItem.click()
        
        spanForCurrentSite = paginationObj.getPaginationCurrentSiteString()
        textOfSpan = spanForCurrentSite.text
        numberOfPages = int(textOfSpan.split("von")[1])
        
        # click on next site and check if still the same number of pages are shown:
        paginationNextLink = paginationObj.getPaginationNextLink()
        paginationNextLink.click()
        
        numberOfPagesOnNextSite = paginationObj.getPaginationCurrentSiteString()
        textOfSpanOnNewSite = numberOfPagesOnNextSite.text
        numberOfPagesNewSite = int(textOfSpanOnNewSite.split("von")[1])
        self.assertEqual(numberOfPages, numberOfPagesNewSite)


