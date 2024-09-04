"""This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

"""

import datetime
import gettext
import glob
import sys
import time
import os
import random
from pathlib import Path

sys.path.append(sys.path[0] + "/...")

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
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.lastprofile import Lastprofile
from Src.PageObject.Pages.CurrentLoadApproximation import (
    CurrentLoadApproximation,
)
from Src.PageObject.Pages.HeatApproximation import HeatApproximation
from Src.PageObject.Pages.cookieBanner import CookieBanner


class TestLastProfile(WebDriverSetup):
    """Tests the 'Lastapproximation'-Tab"""

    def testTranslationOfHeatLoadApp(self):
        """Test if the Heat-Load-Approximation is translated correctly"""

        lastprofilePage = Lastprofile(self.driver)

        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        language = self.getLanguage()
        self.checkNavBar("technical")
        linkToHeatApprox = lastprofilePage.getLinkForHeatApproxTool()
        self.scrollElementIntoView(linkToHeatApprox)
        linkTextToHeatApprox = linkToHeatApprox.text

        translationObj = gettext.translation(
            "django", self.PATH_TO_TRANSLATION_FILE, ["de", "en"]
        )
        translatedString = translationObj.gettext(linkTextToHeatApprox)
        self.assertEqual(
            translatedString,
            linkTextToHeatApprox,
            "The translation of the Heat-Approximation-Link is not correct!",
        )

        linkToHeatApprox.click()

        currentAproxObj = HeatApproximation(self.driver)

        currentAproxObj.switchToIFrame()

        # here an explicit sleeping time is needed, since the translation needs some time.
        time.sleep(1)
        headingElement = currentAproxObj.getHeadingOfPage()

        self.assertEqual(
            headingElement.text,
            translationObj.gettext(headingElement.text),
            "Heading Title is not shown in the right language. Check the translation!",
        )
        if language == "en":
            bottomParagraph = currentAproxObj.getBottomParagraph()
            self.assertEqual(
                translationObj.gettext(bottomParagraph.text),
                bottomParagraph.text,
                "The bottom paragraph is not translated correctly!",
            )

    def testLastprofileApprox(self):
        """Clicks on 'Approximation der Stromlast' and tests the tool"""
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)
        self.checkNavBar("technical")
        lastProfileLink = lastprofilePage.getLinkToStromlastTool()
        self.driver.execute_script(
            "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));",
            lastProfileLink,
        )
        time.sleep(1)
        lastProfileLink.click()

        self.assertEqual(
            "Stromlastprofil",
            self.driver.title,
            "Page should be 'Stromlastprofile', but its not!",
        )

        currentApproObj = CurrentLoadApproximation(self.driver)
        cookieBannerObj = CookieBanner(self.driver)
        self.scrollElementIntoViewAndClickIt(
            cookieBannerObj.getCookieAcceptanceButton()
        )
        self._setLanguageToGerman()
        currentApproObj.switchToIFrame()
        headingElement = currentApproObj.getHeadingOfPage()

        self.assertEqual(
            headingElement.text,
            "Stromlast Approximation",
            "Heading Title should be Stromlast Approximation, but its not!",
        )

    def testHeatApproximation(self):
        """Tests if 'Heat Approximation' is reachable"""
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)
        self.checkNavBar("technical")
        linkToHeatApprox = lastprofilePage.getLinkForHeatApproxTool()

        cookieBanner = CookieBanner(self.driver)
        cookieBannerButn = cookieBanner.getCookieAcceptanceButton()
        time.sleep(2)
        cookieBannerButn.click()

        actions = ActionChains(self.driver)
        try:
            actions.move_to_element(linkToHeatApprox).perform()
        except MoveTargetOutOfBoundsException as e:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
                linkToHeatApprox,
            )
        time.sleep(1)
        # cookieBannerObj = CookieBanner(self.driver)
        # cookieBannerObj.getCookieAcceptanceButton().click()
        time.sleep(1)
        self.driver.save_screenshot("ss.png")
        linkToHeatApprox.click()

        self.checkPageTitle(
            "Waermelastprofil",
            "Thermal load profile",
        )

        currentApproObj = HeatApproximation(self.driver)
        time.sleep(1)
        self._setLanguageToGerman()
        currentApproObj.switchToIFrame()
        headingElement = currentApproObj.getHeadingOfPage()

        self.assertEqual(
            headingElement.text,
            "Wärmelast Approximation",
            "Heading Title should be Wärmelast Approximation, but its not!",
        )

    def testLinksOnSite(self):
        """Tests, if the links present on the website lead to the right websites."""
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/")
        lastprofilePage = Lastprofile(self.driver)
        cookieBannerObj = CookieBanner(self.driver)
        self.scrollElementIntoViewAndClickIt(
            cookieBannerObj.getCookieAcceptanceButton()
        )
        weatherServiceLink = lastprofilePage.getWeatherServiceLink()

        actions = ActionChains(self.driver)
        try:
            actions.move_to_element(weatherServiceLink).perform()
        except MoveTargetOutOfBoundsException as e:
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", weatherServiceLink
            )
        time.sleep(1)

        weatherServiceLink.click()
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.assertEqual(
            "GitHub - earthobservations/wetterdienst: Open weather data for humans.",
            self.driver.title,
            "After clicking on Wetterdienst-Link, the github-page of wetterdienst should appear!",
        )
        self.driver.switch_to.window(self.driver.window_handles[0])

        loadProfileLink = lastprofilePage.getLoadProfileLink()
        loadProfileLink.click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        self.assertEqual(
            "Standardlastprofile Strom | BDEW",
            self.driver.title,
            "After clicking on Standard Loadprofile-Link, the page of bdew should appear!",
        )

    def testDataLoadsOnStromlast(self):
        """Test the Stromlast App, if a graph is loaded."""
        self.driver.get(os.environ["siteUnderTest"] + "/LastProfile/stromlast")
        lastprofilePage = Lastprofile(self.driver)

        # switch into iframe of the react page:
        iframeElement = lastprofilePage.getPlotlyIFrame()
        self.driver.switch_to.frame(iframeElement)

        selectPlaceholderToHoverOver = lastprofilePage.getReactSelectPlaceholder()
        actions = ActionChains(self.driver)
        actions.move_to_element(selectPlaceholderToHoverOver).click().perform()

        openedSelectElement = lastprofilePage.getOpenedReactSelect()
        getElementToBeSelected = random.choice(openedSelectElement.text.split("\n")[1:])

        optionToClick = lastprofilePage.getReactOptionFromText(
            selectPlaceholderToHoverOver, getElementToBeSelected
        )
        optionToClick.click()

        listOfRadioButtons = lastprofilePage.getListOfRadioMonth()
        radioElementToClick = random.choice(listOfRadioButtons)
        radioElementToClick.click()

        inputFieldPowerRequirement = lastprofilePage.getInputFieldPowerRequirement()
        inputFieldPowerRequirement.send_keys(random.randrange(1, 100000, 1))
        inputFieldPowerRequirement.send_keys(Keys.RETURN)
        time.sleep(3)
        lineObj = lastprofilePage.getLinePloty()
        self.assertGreater(
            len(lineObj.get_attribute("d")),
            20,
            "The Line-Plot should at least contain 20 Datapoints, but it doesnt! Is the plot even loaded?",
        )

        # start a watchDog-Session, which looks in Downloads if Stromlastgang.csv is created

        # test if the data can be downloaded
        # buttonCSVDownload = lastprofilePage.getCsvDownloadButton()
        # time.sleep(1)
        # buttonCSVDownload.click()
        # time.sleep(1)
        # buttonCSVDownload.click()
        # time.sleep(3)
        # files = list(filter(os.path.isfile, glob.glob(str(Path.home()) + "/Downloads/" + "*")))

        # files.sort(key=lambda x: os.path.getmtime(x))
        # self.assertTrue("Stromlastgang" in files[-1], "Stromlastgang File wasnt the last modified file in downloads!")

        # lastModified = os.path.getmtime(files[-1])

        # self.assertTrue(lastModified > (datetime.datetime.now()-datetime.timedelta(seconds=20)).timestamp(), "Das Änderungsdatum ist älter als 20 Sekunden alt!")
