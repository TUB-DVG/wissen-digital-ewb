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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.PublicationPage import PublicationPage
from Src.PageObject.Pages.toolListPage import ToolListPage

class TestPublicationPage(WebDriverSetup):
    
    def testAllPublicationPages(self):
        """Test the publication pages with all focuses

        This testmethod calls the protected method _colorOfBorder for times 
        with the different focuses.
        """
        focusStringsList = ["technisch", "betrieblich", "ökologisch", "rechtlich"]
        for focus in focusStringsList:
            self._colorOfBorder(focus)
            self.driver.back()
    
    def testRemoveFocusFilter(self):
        """Check if an error occurs when the focus filter is removed
        
        This Tests checks, if an error is produced, if the focus filter is removed.
        Therefore the cross of the showing focus-search-filter is clicked. 
        After that it is tested, if the search-box is still available.
        After that, it also tests the reset-button.

        """
        
        focusStringsList = {
            "technisch": "11",
            "betrieblich": "12",
            "ökologisch": "13",
            "rechtlich": "14",
        }
        randomFocusElement = random.choice(list(focusStringsList.keys()))
            
        self.driver.get(os.environ["siteUnderTest"] + "/publications/?searched=&fo=" + focusStringsList[randomFocusElement])
        publicationPage = PublicationPage(self.driver)
        # breakpoint()
        removeFocusFilterLink = publicationPage.getPublicationRemoveFocusFilter()
        self.scrollElementIntoViewAndClickIt(removeFocusFilterLink)

        try:
            publicationSearchBoxElement = publicationPage.getPublicationSearchBoxInput()
            WebDriverWait(self.driver, 10).until(lambda d : publicationSearchBoxElement.is_displayed())
        except TimeoutException:
            self.fail("The publication search box is not available after removing the focus filter")

        self.driver.get(os.environ["siteUnderTest"] + "/publications/?searched=&fo=" + focusStringsList[randomFocusElement])
        resetButton = publicationPage.getPublicationSearchBoxReset()
        self.scrollElementIntoViewAndClickIt(resetButton)
        try:
            publicationSearchBoxElement = publicationPage.getPublicationSearchBoxInput()
            WebDriverWait(self.driver, 10).until(lambda d : publicationSearchBoxElement.is_displayed())
        except TimeoutException:
            self.fail("The publication search box is not available after removing the focus filter")

    def _colorOfBorder(self, focus: str) -> None:
        """Check if the color of the border is correct

        The color of the border should be the same as the focus of the publication
        """
        self.driver.get(os.environ["siteUnderTest"])

        # click the link to the technical-publications page:
        startPageObj = StartPage(self.driver)
        linkToPublicationsPage = startPageObj.getLinkToPublications(focus) 

        self.scrollElementIntoViewAndClickIt(linkToPublicationsPage)

        publicationPageObj = PublicationPage(self.driver)
        publicationContainer = publicationPageObj.getPublicationContainer()

        expectedColor = ""
        if focus == "technisch":
            expectedColor = "rgb(175, 197, 255)"
            containerClassName = "container technical-cards"
        elif focus == "betrieblich":
            expectedColor = "rgb(255, 174, 157)"
            containerClassName = "container operational-cards"
        elif focus == "ökologisch":
            expectedColor = "rgb(174, 234, 180)"
            containerClassName = "container ecological-cards"
        elif focus == "rechtlich":  
            expectedColor = "rgb(245, 232, 106)"
            containerClassName = "container legal-cards"
        else:
            expectedColor = "rgb(255, 255, 255)"
            containerClassName = "container neutral-cards"

        # Check the border-color of the publicationContainer div-element
        borderColor = publicationContainer.value_of_css_property("border-color")
        
        self.assertEqual(publicationContainer.get_attribute("class"), containerClassName)

        publicationSearchBoxDiv = publicationPageObj.getPublicationSearchBoxForm()
        self.assertEqual(publicationSearchBoxDiv.value_of_css_property("border-color"), expectedColor)
        self.assertEqual(publicationPageObj.getPublicationSearchBoxInput().value_of_css_property("border-color"), expectedColor)
        self.assertEqual(publicationPageObj.getPublicationSearchBoxSelect().value_of_css_property("border-color"), expectedColor)
        self.assertEqual(publicationPageObj.getPublicationSearchBoxSubmit().value_of_css_property("background-color"), expectedColor)
        self.assertEqual(publicationPageObj.getPublicationSearchBoxReset().value_of_css_property("background-color"), expectedColor)



