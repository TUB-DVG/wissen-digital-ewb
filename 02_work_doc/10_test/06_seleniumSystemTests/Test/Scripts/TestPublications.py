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
from selenium.webdriver.support import expected_conditions as EC

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



