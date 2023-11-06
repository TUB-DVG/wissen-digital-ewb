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
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AboutPage import AboutPage

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
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.AboutPage import AboutPage

class TestAboutPage(WebDriverSetup):
    """Tests the About-Page
    
    """

    def testHeading(self):
        """Tests if the two Headings on the Page are displayed.
        
        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/about")

        aboutPageObj = AboutPage(self.driver)
        topHeadingOfPage = aboutPageObj.getTopHeading()

        self.assertEqual(
            "Modul Digitalisierung",
            topHeadingOfPage.text,
            "Top Heading should be 'Modul Digitalisierung', but its not!",
        )

        subHeadingOfPage = aboutPageObj.getSubHeading()

        self.assertEqual(
            "Begleitforschung Energiewendebauen",
            subHeadingOfPage.text,
            "Sub Heading should be 'Begleitforschung Energiewendebauen', but its not!",
        )
    
    def testIfEWBImageIsLink(self):
        """Tests, if the 'EnergieWendeBauen'-Image is a Link.

        Tests, if the EWB-image on the right side redirects to the 
        EWB-Website.
        
        """

        self.driver.get(os.environ["siteUnderTest"] + "/pages/about")
        
        aboutPageObj = AboutPage(self.driver)
        ewbImage = aboutPageObj.getEWBImage()
        ewbImage.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)
        
        self.assertEqual(
            "Aktuelles - energiewendebauen.de",
            self.driver.title,
            "Page title should be 'Aktuelles - energiewendebauen.de', but its not!",
        )
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    
    def testIfLinksWork(self):
        """Clicks all Links on Page

        Tests if the Links on the About Page redirect to the right Pages. 
        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/about")
        
        aboutPageObj = AboutPage(self.driver)

        linkToUDKPage = aboutPageObj.getUDKLink()
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})", linkToUDKPage)
        time.sleep(1)
        linkToUDKPage.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)
        self.assertEqual(
            "Energiewendebauen | Berlin Career College/Zentralinstitut für Weiterbildung (ZIW)",
            self.driver.title,
            "Page title after clicking UDK-Team Link Link should be 'Energiewendebauen | Berlin Career College/Zentralinstitut für Weiterbildung (ZIW)', but its not!",
        )
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        linkToIOeWPage = aboutPageObj.getIOeWLink()
        linkToIOeWPage.click() 
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(3)
        self.assertEqual(
            "Energiewendebauen | IÖW",
            self.driver.title,            
            "Page title after clicking IÖW Link should be 'Energiewendebauen | IÖW', but its not!",
        )

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        imgOfEinsteinCenter = aboutPageObj.getImgOfEinsteinCenter() 

        self.driver.execute_script("arguments[0].scrollIntoView(true);", imgOfEinsteinCenter)
        time.sleep(1)
        imgOfEinsteinCenter.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(1)

        self.assertEqual(
            "Energiewendebauen | Einstein Center Digital Future",
            self.driver.title,            
            "Page title after clicking on image of Einstein Center is not 'Energiewendebauen | Einstein Center Digital Future'!",
        )
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        imgOfTUBerlin = aboutPageObj.getImgOfTUBerlin()
        imgOfTUBerlin.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        self.assertEqual(
            "Technische Universität Berlin",
            self.driver.title,            
            "Page title after clicking on image of TU Berlin is not 'Technische Universität Berlin'!",
        )

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        imgOfUDK = aboutPageObj.getImgOfUDK()
        imgOfUDK.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        self.assertEqual(
            "Energiewendebauen | Berlin Career College/Zentralinstitut für Weiterbildung (ZIW)",
            self.driver.title,            
            "Page title after clicking on image of UDK is not 'Energiewendebauen | Berlin Career College/Zentralinstitut für Weiterbildung (ZIW)'!",
        )

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

        imgOfIOEW = aboutPageObj.getImgOfIOEW()
        imgOfIOEW.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        self.assertEqual(
            "Energiewendebauen | IÖW",
            self.driver.title,            
            "Page title after clicking on image of IÖW is not 'Energiewendebauen | IÖW'!",
        )
