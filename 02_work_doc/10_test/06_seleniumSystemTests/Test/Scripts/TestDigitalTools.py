"""Tests the `Digitale Werkzeuge` (engl. digital tools)-Tab

This module acts as system test of the digital tools tab. It is tested 
from the outside/from a enduser perspective using selenium-webdriver.

"""
import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from selenium import (
    webdriver, )
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.startPage import StartPage
from Src.PageObject.Pages.toolListPage import ToolListPage
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.cookieBanner import CookieBanner
from Src.PageObject.Pages.ComparisonPageSection import ComparisonPageSection
from Src.PageObject.Pages.SearchPage import SearchPage
from Src.PageObject.Pages.Pagination import Pagination

class TestDigitalToolsPage(WebDriverSetup):
    """ """

    TECHNICAL_COLOR_CODE = "rgb(143, 171, 247)"

    def _testSearchBar(self, dictOfTranslation):
        """ """

        searchInput = self.searchPartialObj.getTextInput()

        self.assertEqual(
            searchInput.get_attribute("placeholder"),
            dictOfTranslation["searchInput"],
            "Placeholder in search-input field is not as expected.",
        )
        placeholderColor = self.driver.execute_script(
            """
        var input = arguments[0];
        var pseudoElement = '::placeholder';
        var prop = 'color';
        return window.getComputedStyle(input, pseudoElement).getPropertyValue(prop);
        """,
            searchInput,
        )
        self.assertEqual(
            placeholderColor,
            self.TECHNICAL_COLOR_CODE,
            "Placeholder color of the search input field should be technical focus color.",
        )

        # get all select inputs of the search-bar:
        surroundingDiv = self.searchPartialObj.getSearchDivContainer()
        allSelectsInSearchBar = self.searchPartialObj.getDescendantsByTagName(
            surroundingDiv, "select")

        self.assertEqual(
            len(allSelectsInSearchBar),
            3,
            "The number of select elements in the search bar of the Tools page should be 3.",
        )

        # check if a radio button is present:
        listOfRadioButtons = self.searchPartialObj.getRadioButtons()
        self.assertEqual(
            len(listOfRadioButtons),
            1,
            "The number of radio elements in the search bar of the Tools page should be 1.",
        )

        # if the radio button is clicked, the compare buttons should appear
        # check if the radio buttons are not present by default:
        comparisonPageSecObj = ComparisonPageSection(self.driver)
        startComapareDiv = comparisonPageSecObj.getStartCompareButtonLink()
        resetComparisonDiv = comparisonPageSecObj.getResetButtonLink()
        self.assertTrue(not startComapareDiv.is_displayed())
        self.assertTrue(not resetComparisonDiv.is_displayed())

        # click the radio button:
        listOfRadioButtons[0].click()

        self.assertTrue(startComapareDiv.is_displayed())
        self.assertTrue(resetComparisonDiv.is_displayed())

        # check if the right translation is displayed:
        descriptionTextForRadio = self.searchPartialObj.getNextSibling(
            listOfRadioButtons[0])
        self.assertEqual(
            descriptionTextForRadio.text,
            dictOfTranslation["radioDescription"],
        )

    def testFilteringAndPagination(self):
        """Test if the pagination works, when selecting an filter from one of the select elements
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        self._setLanguageToGerman()

        # cookieBannerObj = CookieBanner(self.driver)
        # cookieBanner = cookieBannerObj.getCookieAcceptanceButton()
        # if cookieBanner.is_displayed():
        #     breakpoint()
        #     cookieBanner.click()

        searchBarPageObj = SearchPage(self.driver)
        paginationObj = Pagination(self.driver)

        multiselectInputs = searchBarPageObj.getMultiSelectClickables()
        chosenSelect = random.choice(multiselectInputs)
        chosenSelect.click()

        divOfOpenedDropDown = self.driver.find_element(By.XPATH, "//div[contains(@class, 'dropdown-menu w-100 show')]")
        dropdownElements = searchBarPageObj.getDescendantsByTagName(divOfOpenedDropDown, "div")[1:] 
        chosenFilterItem = random.choice(dropdownElements)
        chosenFilterItem.click()
        
        spanForCurrentSite = paginationObj.getPaginationCurrentSiteString()
        textOfSpan = spanForCurrentSite.text
        numberOfPages = int(textOfSpan.split("von")[1])
        
        # click on next site and check if still the same number of pages are shown:
        paginationNextLink = paginationObj.getPaginationNextLink()
        self.scrollElementIntoViewAndClickIt(paginationNextLink)
        
        numberOfPagesOnNextSite = paginationObj.getPaginationCurrentSiteString()
        textOfSpanOnNewSite = numberOfPagesOnNextSite.text
        numberOfPagesNewSite = int(textOfSpanOnNewSite.split("von")[1])
        self.assertEqual(numberOfPages, numberOfPagesNewSite)

    def testNavigateToDigitalToolsPage(self) -> None:
        """Navigates from norm list to digital-tools-tab."""
        print(os.environ["siteUnderTest"])
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")

        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()
        toolListItem = navBar.getNavToolList()
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).click(toolListItem).perform()

        time.sleep(1)

        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

    def testSearchField(self) -> None:
        """Tests the Search Function in `Digitale Anwendungen`"""
        # self.openToolList()
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")

        toolListPage = ToolListPage(self.driver)

        self.searchPartialObj = SearchPage(self.driver)

        # search-input field and 3 select-inputs should be present
        # furthermore the radio button for the comparison feature should be there.
        translationDict = {
            "de": {
                "searchInput": "Suchbegriff",
                "radioDescription": "Vergleichsmodus",
            },
            "en": {
                "searchInput": "search term",
                "radioDescription": "Comparison mode",
            },
        }
        self.checkInGermanAndEnglish(self._testSearchBar, translationDict)

        searchFieldElement = toolListPage.getSearchInputElement()
        if searchFieldElement is None:
            self.assertTrue(False)
            return
        listOfToolItems = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listOfToolItems),
            12,
            "Number of Tool Items should be 12 without search-filter!",
        )
        searchFieldElement.send_keys("BIM")
        searchFieldElement.send_keys(Keys.RETURN)
        time.sleep(3)
        listOfToolItemsAfterReturn = toolListPage.getListOfToolItems()

        self.assertEqual(
            len(listOfToolItemsAfterReturn),
            1,
            "Number of Tool Items should be one for Search-String 'Ansys'!",
        )
        
        searchFieldElement.clear()
        time.sleep(2) 
        listToolItemsAfterRmvdSearch = toolListPage.getListOfToolItems()
        self.assertEqual(
            len(listToolItemsAfterRmvdSearch),
            12,
            "After removing search-string 'Ansys', number of tool-items should be 12!",
        )

    def testIfShowMoreExpandsText(self):
        """Tests, if clicking `Zeige mehr` shows the whole text.

        This method tests the expansion-text-field on tool-list page.
        First it tests if the expansion-field is collapsed after
        loading the page. This is done by checking if the list
        inside the text-field is displayed. After that, the
        `Zeige mehr ...`-Link is pressed, which expands the text-
        field. It is then checked if the list is now displayed.
        Finally, the `Zeige weniger ...`-button is pressed, which
        should collapse the text again. It is then tested, if
        the list is hidden.
        """
        # self.openToolListAndLogin()
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolListPage = ToolListPage(self.driver)

        time.sleep(5)
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerObj.getCookieAcceptanceButton().click()

        self.assertFalse(
            toolListPage.getListInExpandedText()[0].is_displayed(),
            "The list inside the expand-field is shown, but it should be collapsed on page load!",
        )

        toolListPage.getShowMoreElement().click()

        listOfListElements = toolListPage.getListInExpandedText()
        time.sleep(1)
        self.assertTrue(
            listOfListElements[0].is_displayed(),
            "List-Element is not Displayed after clicking on 'Zeige mehr ...'!",
        )

        time.sleep(1)
        showLessLink = toolListPage.getShowLessElement()
        self.driver.execute_script("arguments[0].click();", showLessLink)
        # time.sleep(1)
        # showLessLink.click()

        time.sleep(1)
        self.assertFalse(
            toolListPage.getListInExpandedText()[0].is_displayed(),
            "List is still displayed after clicking 'show less ...'!",
        )

    def openToolList(self) -> None:
        """Helper-method, which connects to tool-list page."""
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        titleAfterClickLink = "Überblick über die Anwendungen"
        self.checkPageTitle(titleAfterClickLink)

        navBar = NavBar(self.driver)
        techItem = navBar.getNavTechFocus()

        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(techItem).perform()
        time.sleep(1)
        digitalToolsItem = navBar.getNavDigitalTools()

        digitalToolsItem.click()

    def checkPageTitle(self, pageTitle) -> None:
        """ """
        try:
            if self.driver.title == pageTitle:
                print("WebPage loaded successfully")
                self.assertEqual(self.driver.title, pageTitle)
        except Exception as error:
            print(error + "WebPage Failed to load")

    def testConsistentPagination(self):
        """
        This method tests the pagination of tool list
        the first page should have first and last page but no previous page.
        Also the number of pages displayed on the first page
        matches the number shown on the last page
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolPageObj = ToolListPage(self.driver)

        listOfNextElement = toolPageObj.getNextElementInList()
        self.assertEqual(
            len(listOfNextElement),
            1,
            "next-search-results-page should be present, but it is not!",
        )
        listOfPreviousElement = toolPageObj.getPreviousElementInList()
        self.assertEqual(
            len(listOfPreviousElement),
            0,
            "previous-search-results-page should not be present, but it is!",
        )
        listOfFirstElement = toolPageObj.getFirstElementInList()
        self.assertEqual(
            len(listOfFirstElement),
            0,
            "First-search-results-page should not be present, but it is!",
        )
        listOfLastElement = toolPageObj.getLastElementInList()
        self.assertEqual(
            len(listOfLastElement),
            1,
            "last-search-results-page should be present, but it is not!",
        )
        currentPageNumberElement = toolPageObj.getCurrentSearchResultNumber()
        indexPageEndNumber = currentPageNumberElement.text.split()[-1]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'})",
            listOfLastElement[0],
        )
        time.sleep(1)
        listOfLastElement[0].click()
        time.sleep(1)
        currentPageNumberElement = toolPageObj.getCurrentSearchResultNumber()
        lastPageEndNumber = currentPageNumberElement.text.split()[-1]
        self.assertEqual(
            indexPageEndNumber,
            lastPageEndNumber,
            "Page numbers on the first and last pages should be the same",
        )

    def testIfToolImageErrorTextIsPresent(self):
        """Check if a tool is on the page, which has the 'tool image (if=db)'-error
        In this test all pages of the digital-tools-tab are gone through and checked if one of the tools shows the image error 'tool image (if=db)'. If so the test is red.
        """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        toolsPageObj = ToolListPage(self.driver)
        paginationPagesStr = toolsPageObj.getCurrentSearchResultNumber()
        numberOfPages = int(paginationPagesStr.text[-1])
        script = """
        var img = arguments[0];
        if (img.naturalWidth === 0) {
            return img.alt;
        } else {
            return null;
        }
        """
        foundAltText = False
        for currentPageNumber in range(numberOfPages):
            listOfToolItemsOnCurrentPage = toolsPageObj.getListOfToolItems()
            for toolItem in listOfToolItemsOnCurrentPage:
                try:
                    imageOfCurrentItem = toolItem.find_element(
                        By.XPATH, ".//img")
                except NoSuchElementException:
                    continue
                altTextPresent = self.driver.execute_script(
                    script, imageOfCurrentItem)
                if altTextPresent:
                    toolName = toolItem.text.split("\n")[0]
                    print(
                        f"Alt Text is present for Tool {toolName} instead of the image."
                    )
                    foundAltText = True

            nextLink = toolsPageObj.getNextElementInList()
            if len(nextLink) > 0:
                nextLink = toolsPageObj.getNextElementInList()[0]
                self.scrollElementIntoViewAndClickIt(nextLink)

        self.assertFalse(
            foundAltText,
            "Found Alt-Text for images in Digital-Tools. Check if the image for the tool is present in the media-folder",
        )

    def testComparison(self):
        """ """
        self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")

        self._setLanguageToGerman()

        toolsPageObj = ToolListPage(self.driver)
        comparisonPageSection = ComparisonPageSection(self.driver)
        searchBarObj = SearchPage(self.driver)
        # click the Compare-Button and check if 2 buttons appear and the checkboxes
        # in each listing element is shown
        compareRadioButtonList = searchBarObj.getRadioButtons()

        # on the tools-page, only one radio button should be in the search-bar
        self.assertEqual(len(compareRadioButtonList), 1)

        # click the radio button to make the compare buttons and checkboxes appear:
        compareRadioButtonList[0].click()

        firstComparisonDiv = comparisonPageSection.getFirstComparisonDiv()
       
        self.assertTrue(
            firstComparisonDiv.is_displayed(),
            "The compare div-section should be displayed after clicking the compare radio button",
        )
        comparisonButtons = comparisonPageSection.getDescendantsByTagName(
            firstComparisonDiv, "h6")
        self.assertEqual(len(comparisonButtons), 2)

        # check if the right text is displayed in the comparison-buttons
        self.assertEqual(
            comparisonButtons[0].text,
            "Vergleiche",
            "The compare-button should be present",
        )
        self.assertEqual(
            comparisonButtons[1].text,
            "Zurücksetzen",
            "The reset-button should be present",
        )

        # check if the checkboxes are present in the listing elements
        listOfToolItems = toolsPageObj.getListOfToolItems()
        for toolItem in listOfToolItems:
            checkbox = toolItem.find_element(By.XPATH, ".//input")
            self.assertTrue(checkbox.is_displayed())

        # randomly decide how many tools to compare:
        numberOfToolsToCompare = random.randint(2, 5)
        # randomly select the tools to compare
        toolsToCompare = random.sample(listOfToolItems, numberOfToolsToCompare)
        for tool in toolsToCompare:
            self.scrollElementIntoView(tool)
            toolCheckbox = tool.find_element(By.XPATH, ".//input") 
            self.scrollElementIntoViewAndClickIt(toolCheckbox)

        # click the compare-button and check if the comparison-page is loaded
        self.scrollElementIntoViewAndClickIt(comparisonButtons[0])
        
        comparisonHeading = comparisonPageSection.getHeadingComparisonSite()
        self.assertEqual(
            comparisonHeading.text,
            "Ergebnisse",
            "The comparison-heading should be present",
        )

        comparisonTableContainer = (
            comparisonPageSection.getComparisonTableContainer())
        
        listOfTableRows = comparisonPageSection.getDescendantsByTagName(comparisonTableContainer, "tr")
        # check if the comparison tabel has all attributes as rows:
        shownAttributesStr = [
            "Attribut",
            "",
            "Einsatzbereich",
            "Verwendung",
            "Lebenszyklusphase",
            "Zielgruppe",
            "Benutzeroberfläche",
            "Räumliche Größenordnung der Anwendungsfälle",
            "Zugänglichkeit",
            "Programmiersprache (Umsetzung)",
            "Lizenz",
            "Entwicklungsstand - 1: pre-Alpha - 2: Alpha - 3: Beta - 4: Release Canidate - 5: Released",
            "Veröffentlichungsjahr",
            "Letztes Update",
        ]

        for attrIndex, attributeStr in enumerate(shownAttributesStr):
            firstRowElement = comparisonPageSection.getDescendantsByTagName(listOfTableRows[attrIndex], "th")[0]
            self.assertTrue(attributeStr in firstRowElement.text, f"{firstRowElement.text} should be {attributeStr}...")

        # self._setLanguageToEnglish()
        # check if a back button is present:
        backButton = comparisonPageSection.getBackButton()
        self.assertEqual(backButton.text, "Zurück zu den digitalen Werkzeugen")
        # check if the color is the tool-color and the font-size is small:
        self.assertEqual(
            backButton.value_of_css_property("color"),
            self.TECHNICAL_COLOR_CODE,
            "The color of the back-button should be the technical-focus-color",
        )
        self.assertEqual(
            backButton.value_of_css_property("font-size"),
            "15px",
            "The font-size of the back-button should be 14px",
        )
        siblingElement = comparisonPageSection.getDescendantsByTagName(
            backButton, "img")[0]
        self.assertIsNotNone(siblingElement)
        # no alt text should be present, because the image is loaded successfully:
        self.assertTrue(siblingElement.text == "")

        # check if the back button redirects to the tool-list page:
        # backButton.click()
        #
        # self.assertTrue("/tool_list/" in self.driver.current_url)

        # check if all the row-attribute names are translated:
        self._setLanguageToEnglish()

        comparisonHeading = comparisonPageSection.getHeadingComparisonSite()
        self.assertEqual(
            comparisonHeading.text,
            "Results",
            "The comparison-heading should be present",
        )

        shownAttributesStr = [
            "Attribute",
            "",
            "Area of application",
            "Applications",
            "Life cycle phase",
            "Target group",
            "User interface",
            "Spatial scale of use cases",
            "Accessibility",
            "Programming language (implementation)",
            "License",
            "Level of development - 1: pre-Alpha - 2: Alpha - 3: Beta - 4: Release Canidate - 5: Released",
            "Year of publication",
            "Last update",
        ]
        comparisonTableContainer = (
            comparisonPageSection.getComparisonTableContainer())
        listOfTableRows = comparisonPageSection.getDescendantsByTagName(comparisonTableContainer, "tr")

        for attrIndex, attributeStr in enumerate(shownAttributesStr):
            firstRowElement = comparisonPageSection.getDescendantsByTagName(listOfTableRows[attrIndex], "th")[0]
            self.assertTrue(attributeStr in firstRowElement.text, f"{firstRowElement.text} should be {attributeStr}...")

        # # check if the buttons are translated to english
        # self.driver.get(os.environ["siteUnderTest"] + "/tool_list/")
        #
        # self._setLanguageToEnglish()
        # firstComparisonDiv = comparisonPageSection.getFirstComparisonDiv()
        # compareButton = comparisonPageSection.getDescendantsByTagName(
        #     firstComparisonDiv, "h6")[0]
        # self.assertEqual(
        #     compareButton.text,
        #     "Compare",
        #     "The compare-button should be present",
        # )
        # compareButton.click()
        # secondComparisonDiv = comparisonPageSection.getSecondComparisonDiv()
        # comparisonButtons = comparisonPageSection.getDescendantsByTagName(
        #     secondComparisonDiv, "h6")
        #
        # self.assertEqual(len(comparisonButtons), 2)
        # self.assertEqual(
        #     comparisonButtons[0].text,
        #     "Compare",
        #     "The compare-button should be present",
        # )
        # self.assertEqual(
        #     comparisonButtons[1].text,
        #     "Reset to default",
        #     "The reset-button should be present",
        # )
