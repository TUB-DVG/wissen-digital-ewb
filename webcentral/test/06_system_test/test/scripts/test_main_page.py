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
from selenium.common.exceptions import TimeoutException

from src.test_base.webdriver_setup import WebDriverSetup
from src.page_obj.pages.start_page import StartPage
from src.page_obj.pages.tool_list_page import ToolListPage
from src.page_obj.pages.navbar import NavBar
from src.page_obj.pages.about_page import AboutPage
from src.page_obj.pages.cookie_banner import CookieBanner
from src.page_obj.pages.criteria_catalog import (
    CriteriaCatalogOverviewPage,
    CriteriaCatalogDetailsPage,
)


class TestMainPage(WebDriverSetup):
    """Testclass for MainPage-Test

    Inherit from TestWebcentral. There methods should be implemented,
    which are relevant for all Test-Classes (like the login-functionality,
    which is no longer needed.)

    """

    def testReloadOfResultsPage(self):
        """Check if reload of StartSearch-Result Page produces an error

        When pressing reload on the results page a django-error is thrown, which also
        leads to a 500 Internal Server Error by nginx in the production environment.
        That should not happen. A bugfix was implemented, which returns the startpage,
        when the reload button on the webbrowser was clicked. That behaviour is tested
        here.
        """
        lengthOfRandomSearch = 2

        self.driver.get(os.environ["siteUnderTest"])
        startPageObj = StartPage(self.driver)
        searchInputField = startPageObj.getSearchInputField()
        searchStr = ""
        for currentNumberOfSearch in range(lengthOfRandomSearch):
            searchStr += chr(random.randint(ord("a"), ord("z")))

        searchInputField.send_keys(searchStr)
        searchInputField.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "searchResultH2"))
        )
        self.driver.get(os.environ["siteUnderTest"] + "/ResultSearch")
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "inputSearchField"))
            )
        except TimeoutException:
            self._checkForPageError(
                "After reloading the page, an django-error appears, because the search-string is None"
            )

    def testIfCriteriaCatalogTopicsInResults(self):
        """Test if Topics of the critera-catalog are in the search results."""
        self.driver.get(os.environ["siteUnderTest"])

        startPageObj = StartPage(self.driver)
        searchInput = startPageObj.getSearchInputField()

        searchInput.send_keys("Zweckspezifizierung")
        searchInput.send_keys(Keys.RETURN)

        self.waitUntilPageIsLoaded("searchResultH2")
        searchResults = startPageObj.getSearchResults()
        foundCriteriaCatalogResult = False
        for result in searchResults:
            dataHrefAttr = result.get_attribute("data-href")
            if "criteriaCatalog" in dataHrefAttr:
                foundCriteriaCatalogResult = True
                break
        self.assertTrue(
            foundCriteriaCatalogResult,
            "No result from criteria catalog was displayed!",
        )

        # click one of the criteria catalog results:
        result.click()

        criteriaCatalogObj = CriteriaCatalogDetailsPage(self.driver)
        greyBoxes = criteriaCatalogObj.getNormsInforContainers()

        for box in greyBoxes:
            self.assertTrue(not box.is_displayed())
        # chck if we are on the criteria catalog:
        breakpoint()

    def testImpressum(self):
        """Test if on click of Impressum link on the bottom of the site
        the Impressum page opens, which is located on $siteunderTtest + /pages/Impressum

        """
        self.driver.get(os.environ["siteUnderTest"])

        startPageObj = StartPage(self.driver)
        impressumLinkElement = startPageObj.getImpressumLink()
        # self.driver.implicitly_wait(10)
        # ActionChains(self.driver).move_to_element(impressumLinkElement).perform()
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", impressumLinkElement
        )
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(impressumLinkElement)).click()
        time.sleep(1)
        impressumLinkElement.click()
        time.sleep(1)

        self.assertEqual(
            self.driver.title,
            "Impressum",
            "Page should be Impressum, but its not!",
        )

    def testSearchFieldWithRandomCharacters(self):
        """Check if search produces results for random search-string

        This test checks, if start-search produces an result for an
        random character combination of length 2. Since there was an
        error present in the past, due to wrong format of 'lastUpdate',
        this test should find out about that error.
        """
        lengthOfRandomSearch = 2

        self.driver.get(os.environ["siteUnderTest"])
        startPageObj = StartPage(self.driver)
        searchInputField = startPageObj.getSearchInputField()
        searchStr = ""
        for currentNumberOfSearch in range(lengthOfRandomSearch):
            searchStr += chr(random.randint(ord("a"), ord("z")))

        searchInputField.send_keys(searchStr)
        searchInputField.send_keys(Keys.RETURN)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "searchResultH2"))
            )
        except TimeoutException:
            self._checkForPageError(
                "The start-search produced a ValueError. This could be because of wrong format of the 'lastUpdate'-row. Check the database!"
            )

    def testSearchFieldForBim2Sim(self):
        """Test the searchfield on the startpage

        It writes 'Bim' into the input-field. After pushing Return,
        BIM2SIM should be in the Result.

        """
        self.driver.get(os.environ["siteUnderTest"])
        startPageObj = StartPage(self.driver)
        searchInputField = startPageObj.getSearchInputField()
        searchInputField.send_keys("Bim")
        searchInputField.send_keys(Keys.RETURN)
        time.sleep(1)
        foundInstanceOfBim = False
        # check if the results page is loaded:
        self.assertTrue(
            self.driver.title != "Server Error (500)"
            or "ValueError" not in self.driver.title,
            "The start-search produced a ValueError. This could be because of wrong format of the 'lastUpdate'-row. Check the database!",
        )
        listOfRowsInResultsTable = startPageObj.getSearchResults()
        for rowElement in listOfRowsInResultsTable:
            if rowElement.text.find("BIM2SIM") >= 0:
                foundInstanceOfBim = True
                firstColumnWebelement = startPageObj.getFirstColumn(rowElement)
                firstColumnWebelement.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(2)
                self.assertEqual(
                    "BIM2SIM",
                    self.driver.title,
                    "After clicking of the search result, which contains 'EnOB: AluPV', Page-Title should be 'Energiewendebauen | 03EN1050B', but its not...",
                )
                # self.driver.close()
                # self.driver.switch_to.window(self.driver.window_handles[0])
                #
                break

        self.assertTrue(
            foundInstanceOfBim,
            "BIM2SIM is not in results! Check the search...",
        )

        # back to search results:
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
                self.driver.execute_script(
                    "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0); var elementTop = arguments[0].getBoundingClientRect().top; window.scrollBy(0, elementTop-(viewPortHeight/2));",
                    rowElement,
                )
                childRowElement.click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(1)
                self.assertTrue(
                    "Energiewendebauen" in self.driver.title,
                    "After clicking Forschungsprojekt it should redirect to Energiewendebauen page!",
                )
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            if checkedScientificProjects == 2:
                break
        self.driver.back()
        time.sleep(1)
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
        self.scrollElementIntoViewAndClickIt(
            cookieBannerObj.getCookieAcceptanceButton()
        )
        self.scrollElementIntoViewAndClickIt(listOfNextElement[0])
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
            "Current Page Number should say 'Seite 2'",
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            listOfPreviousElement[0],
        )
        time.sleep(1)
        listOfPreviousElement[0].click()
        currentPageNumberElement = startPageObj.getCurrentSearchResultNumber()
        self.assertIn(
            "Seite 1",
            currentPageNumberElement.text,
            "Current Page Number should say 'Seite 1'",
        )

    # def testIfLinkToBuisnessAppsWorks(self):
    #     """Test if one can navigate from Main-Page to buisness-application site"""
    #     self.driver.get(os.environ["siteUnderTest"])
    #     startPageObj = StartPage(self.driver)
    #     linkToBuisnessApps = startPageObj.getLinkToBuisnessApps()
    #
    #     self.driver.execute_script("arguments[0].scrollIntoView();",
    #                                linkToBuisnessApps)
    #
    #     time.sleep(1)
    #     linkToBuisnessApps.click()
    #
    #     time.sleep(1)
    #
    #     self.assertEqual(
    #         self.driver.title,
    #         "Überblick über die Geschäftsmodellanwendungen",
    #         "Website should be 'Geschäftsmodellanwendungen', but its not!",
    #     )
    #
    # def testLinkToTechnicalSTandards(self):
    #     """Test if the Technical Standarts Link is working by clicking on it and
    #     checking the page-title on the next site
    #
    #     """
    #     self.driver.get(os.environ["siteUnderTest"])
    #
    #     startPAgeObj = StartPage(self.driver)
    #     linkToTechnicalStandarts = startPAgeObj.getLinkToTechnicalStandarts()
    #     self.driver.execute_script("arguments[0].scrollIntoView();",
    #                                linkToTechnicalStandarts)
    #     time.sleep(1)
    #     linkToTechnicalStandarts.click()
    #     self.assertEqual(
    #         self.driver.title,
    #         "Überblick über die technischen Standards",
    #         "Page should be technical-standarts-page after clicking on link on main-page...",
    #     )
    #
    def testContainers(self):
        """Check if the right links and description is shown in german and english."""
        self.driver.get(os.environ["siteUnderTest"])

        self.startPageObj = StartPage(self.driver)

        self._checkFocusContainer(
            "operational",
            {
                "heading_de": "Betrieblicher Fokus",
                "heading_en": "Operational Focus",
                "linkNamesEnglish": [
                    "Business models",
                    "User integration",
                ],
                "linkNamesGerman": [
                    "Geschäftsmodelle",
                    "Nutzendenintegration",
                ],
                "borderColor": self.OPERATIONAL_COLOR,
            },
        )

        self._checkFocusContainer(
            "ecological",
            {
                "heading_de": "Ökologischer Fokus",
                "heading_en": "Ecological Focus",
                "linkNamesEnglish": [
                    "Negative environmental impacts ",
                    "Positive environmental impacts",
                ],
                "linkNamesGerman": [
                    "Negative Umweltwirkungen",
                    "Positive Umweltwirkungen - Good-practice",
                ],
                "borderColor": self.ECOLOGICAL_COLOR,
            },
        )

        self._checkFocusContainer(
            "legal",
            {
                "heading_de": "Rechtlicher Fokus",
                "heading_en": "Legal Focus",
                "linkNamesEnglish": [
                    "Privacy Overview",
                    "Catalog of criteria",
                    "Icons and visualization",
                ],
                "linkNamesGerman": [
                    "Datenschutz-übersicht",
                    "Kriterienkatalog",
                    "Icons und Visualisierung",
                ],
                "borderColor": self.LEGAL_COLOR,
            },
        )

    def testPageStructure(self):
        """Test if the navBar has 5 focuses and if the 5. focus is present on the page."""
        self.driver.get(os.environ["siteUnderTest"])

        startPAgeObj = StartPage(self.driver)

        # test if a container is present, which has te class row-12 and a global
        # border
        globalFocusContainer = self.driver.find_element(
            By.XPATH, "//div[@id='globalFocusContainer']"
        )
        self.assertTrue("col-12" in globalFocusContainer.get_attribute("class"))
        self.assertTrue(
            globalFocusContainer.value_of_css_property("outline-color")
            == self.GLOBAL_COLOR
        )

        # check if the links have black font color and are underlined in the global focus color:
        linksInGlobalFocusContainer = globalFocusContainer.find_elements(
            By.XPATH, ".//a"
        )
        for link in linksInGlobalFocusContainer:
            self.assertTrue(link.value_of_css_property("color") == "rgb(0, 0, 0)")
            self.assertTrue(
                link.value_of_css_property("border-bottom-color") == self.GLOBAL_COLOR
            )

    def _checkFocusContainer(self, focusName, dataDict):
        """ """

        self.focusContainer = self.startPageObj.getFocusContainer(focusName)
        self.focusName = focusName

        self.checkInGermanAndEnglish(
            self._checkTitle,
            {"de": dataDict["heading_de"], "en": dataDict["heading_en"]},
        )
        self.checkInGermanAndEnglish(
            self._checkBorder,
            {"de": dataDict["borderColor"], "en": dataDict["borderColor"]},
        )
        self.checkInGermanAndEnglish(
            self._checkLinks,
            {
                "de": dataDict["linkNamesGerman"],
                "en": dataDict["linkNamesEnglish"],
            },
        )
        self.checkInGermanAndEnglish(
            self._clickLinks,
            {
                "de": dataDict["linkNamesGerman"],
                "en": dataDict["linkNamesEnglish"],
            },
        )

    def _checkTitle(self, expectedValue):
        """Check the title in german and english"""
        self.focusContainer = self.startPageObj.getFocusContainer(self.focusName)
        headingText = self.startPageObj.getDescendantsByTagName(
            self.focusContainer, "h3"
        )[0]
        self.assertEqual(
            headingText.text,
            expectedValue,
            f"The heading of the focusContainer should be {expectedValue}, but its {headingText.text}!",
        )

    def _checkBorder(self, expectedValue):
        """Check the border of the container on the german and english page."""
        self.focusContainer = self.startPageObj.getFocusContainer(self.focusName)
        self.assertTrue(
            self.focusContainer.value_of_css_property("outline-color") == expectedValue
        )

    def _checkLinks(self, expectedValues):
        """ """
        self.focusContainer = self.startPageObj.getFocusContainer(self.focusName)
        # check the links in the operational focus container:
        linkListElements = self.startPageObj.getDescendantsByTagName(
            self.focusContainer, "a"
        )

        self.assertEqual(
            len(linkListElements),
            len(expectedValues),
            "The number of links in the focus box is not as expected!",
        )

        for linkNumber, linkElement in enumerate(linkListElements):
            self.assertEqual(linkElement.text, expectedValues[linkNumber])

    def _clickLinks(self, expectedValue):
        """ """
        self.focusContainer = self.startPageObj.getFocusContainer(self.focusName)
        # check the links in the operational focus container:
        linkListElements = self.startPageObj.getDescendantsByTagName(
            self.focusContainer, "a"
        )

        for linkIndex, linkElement in enumerate(linkListElements):
            self.focusContainer = self.startPageObj.getFocusContainer(self.focusName)
            linkListElements = self.startPageObj.getDescendantsByTagName(
                self.focusContainer, "a"
            )
            reloadedCurrentLinkElement = linkListElements[linkIndex]

            self.scrollElementIntoViewAndClickIt(reloadedCurrentLinkElement)
            self.assertTrue("PageError" not in self.driver.title)
            self.driver.back()
