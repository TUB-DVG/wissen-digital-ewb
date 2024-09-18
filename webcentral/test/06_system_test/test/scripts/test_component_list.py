import os
from random import choice
import sys
import time
import re

sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.page_obj.pages.cookie_banner import CookieBanner
from src.page_obj.pages.footer import Footer
from src.test_base.webdriver_setup import WebDriverSetup
from src.page_obj.pages.navbar import NavBar
from src.page_obj.pages.search_page import SearchPage
from src.page_obj.pages.comparison_page_section import ComparisonPageSection
from src.page_obj.pages.negative_environmental_impacts import (
    NegativeEnvironmentalImpacts,
)
from src.page_obj.pages.component_list_page import ComponentListPage

# from src.page_obj.pages.ComparisonPageSection import ComparisonPageSection


class TestComponentList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testComponentPageExists(self):
        """Test if the Components-List Page exists and is accessible via url and navbar"""
        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ"
        )
        self.assertTrue(
            "Negative environmental impacts" in self.driver.title
            or "Negative Umweltwirkungen" in self.driver.title
        )

        self.driver.get(os.environ["siteUnderTest"])
        navBar = NavBar(self.driver)
        linkToPage = navBar.returnNegativeEnvironmentalImpactLink()
        self.scrollElementIntoView(linkToPage[1])
        linkToPage[1].click()
        self.assertTrue(
            "Negative environmental impacts" in self.driver.title
            or "Negative Umweltwirkungen" in self.driver.title
        )

    def testStructureOfPage(self):
        """Test if a div-element is present, in which the content is wraped

        This test-method is part of the test-first-dev cycle. It tests if a outer
        div exists, which is of css-class `content`. Inside this div, there should be
        a div-wrapper for the description text, which is again composed of a heading and the
        text. In the bottom part of the page, there should be 2 boxes, which further contents.
        """

        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ"
        )
        impactsObj = NegativeEnvironmentalImpacts(self.driver)
        contentDiv = impactsObj.getContentDiv()

        self.assertIsNotNone(contentDiv)

        descriptionHeadingDiv = impactsObj.getDescriptionHeadingDiv()
        self.assertIsNotNone(descriptionHeadingDiv)

        boxesDiv = impactsObj.getBoxesDiv()

        self.assertIsNotNone(boxesDiv)

        boxes1and2 = impactsObj.getBox1and2()
        self.assertIsNotNone(boxes1and2[0])
        self.assertIsNotNone(boxes1and2[1])

        # test the structure inside the boxes
        boxHeading1 = impactsObj.getBoxHeading(boxes1and2[0])
        self.assertIsNotNone(boxHeading1)

        boxContent1 = impactsObj.getBoxDescription(boxes1and2[0])
        self.assertIsNotNone(boxContent1)

        boxImage1 = impactsObj.getBoxImage(boxes1and2[0])
        self.assertIsNotNone(boxImage1)

        imageInDivBox1 = impactsObj.getImageInBox(boxes1and2[0])
        self.assertIsNotNone(imageInDivBox1)

        image1NaturalWidth = imageInDivBox1.get_attribute("naturalWidth")
        self.assertNotEqual(
            image1NaturalWidth,
            "0",
            "Image 1 is not displayed, only alt-text is shown",
        )

        boxHeading2 = impactsObj.getBoxHeading(boxes1and2[1])
        self.assertIsNotNone(boxHeading2)

        boxContent2 = impactsObj.getBoxDescription(boxes1and2[1])
        self.assertIsNotNone(boxContent2)

        boxImage2 = impactsObj.getBoxImage(boxes1and2[1])
        self.assertIsNotNone(boxImage2)

        imageInDivBox2 = impactsObj.getImageInBox(boxes1and2[1])
        self.assertIsNotNone(imageInDivBox2)

        image2NaturalWidth = imageInDivBox2.get_attribute("naturalWidth")
        self.assertNotEqual(
            image2NaturalWidth,
            "0",
            "Image 2 is not displayed, only alt-text is shown",
        )

        borderColor1 = boxes1and2[0].value_of_css_property("border-color")
        borderColor2 = boxes1and2[1].value_of_css_property("border-color")
        self.assertEqual(
            borderColor1,
            "rgb(143, 222, 151)",
            "Div box 1 does not have a green border",
        )
        self.assertEqual(
            borderColor2,
            "rgb(143, 222, 151)",
            "Div box 1 does not have a green border",
        )

    def testLinksFromOverviewPage(self):
        """Test if the links from the negative environmental impacts page leads to a working page."""
        self.driver.get(
            os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ"
        )
        impactsObj = NegativeEnvironmentalImpacts(self.driver)
        boxes1and2 = impactsObj.getBox1and2()
        # click the box since the <a> cant be clicked directly by selenium
        linkToComponentList = boxes1and2[0]
        linkToComponentList.click()
        self.assertTrue(
            "Components list" in self.driver.title
            or "Komponentenliste" in self.driver.title
        )
        self.driver.back()

        linkToDataProcessing = boxes1and2 = impactsObj.getBox1and2()[1]
        linkToDataProcessing.click()
        self.assertTrue(
            "Data processing" in self.driver.title
            or "Datenverarbeitung" in self.driver.title
        )

    def testComponentListPage(self):
        """Test the structure of the sub-page of the negative environmental impacts page"""
        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )

        componentsListPageObj = ComponentListPage(self.driver)
        divContent = componentsListPageObj.getContentDiv()
        self.assertIsNotNone(divContent)

        secondaryNavbarDiv = componentsListPageObj.getSecondaryNavbar()
        self.assertIsNotNone(secondaryNavbarDiv)

        # test if the secondaryNavBar holds 2 links:
        linksInSecNavBar = componentsListPageObj.getDescendantsByTagName(
            secondaryNavbarDiv, "a"
        )
        self.assertEqual(
            len(linksInSecNavBar),
            2,
            "The secondaryNavBar does not hold 2 links",
        )

        # test styling of link one:
        self.assertTrue(
            linksInSecNavBar[0].value_of_css_property("color")
            == self.ECOLOGICAL_COLOR
        )
        self.assertTrue(
            linksInSecNavBar[0].value_of_css_property("font-size") == "15px",
            "Font-size of link in Navbar should be 15px!",
        )

        borderColor = linksInSecNavBar[1].value_of_css_property("border-color")
        self.assertEqual(
            borderColor,
            self.ECOLOGICAL_COLOR,
            "The second link does not have a green border",
        )
        # check if the left link has a sibling element, which is an image:
        siblingElement = componentsListPageObj.getDescendantsByTagName(
            linksInSecNavBar[0], "img"
        )
        self.assertEqual(len(siblingElement), 1)

        # check if the right link has a following sibling element, which is an image:
        siblingElement = componentsListPageObj.getFollowingSiblingOfTagName(
            linksInSecNavBar[1], "img"
        )

        # test if the links are working
        linkToDataProcessing = linksInSecNavBar[1]
        linkToDataProcessing.click()
        self.assertTrue(
            "Expenses for data processing processes" in self.driver.title
            or "Aufwände für Datenverarbeitungsprozesse" in self.driver.title
        )

        self.driver.back()

        secondaryNavbarDiv = componentsListPageObj.getSecondaryNavbar()
        linkToEnvironmentalImpacts = (
            componentsListPageObj.getDescendantsByTagName(
                secondaryNavbarDiv, "a"
            )[0]
        )
        linkToEnvironmentalImpacts.click()
        self.assertTrue(
            "Negative environmental impacts" in self.driver.title
            or "Negative Umweltwirkungen" in self.driver.title
        )

        self.driver.back()

        # test the description section:
        descriptionSection = componentsListPageObj.getDescriptionSection()
        self.assertIsNotNone(descriptionSection)

        descriptionHeading = componentsListPageObj.getDescriptionHeading()

        self.assertIsNotNone(descriptionHeading)

        # check if the heading is displayed inside the div:
        headingText = descriptionHeading.text
        self.assertTrue(
            "Aufwände für verwendete Komponenten" in headingText
            or "Effort for used components" in headingText
        )

        self._setLanguageToEnglish()

        descriptionHeading = componentsListPageObj.getDescriptionHeading()
        headingText = descriptionHeading.text
        self.assertTrue("Effort for used components" in headingText)

        descriptionText = componentsListPageObj.getDescriptionText()
        self.assertIsNotNone(descriptionText)
        # self.assertTrue(
        #     "In analogy to the data value chain (see 'Expenses for data processing processes'), important components can be thought of from data acquisition (sensors) to data use (actuators). Figure 2 shows important components that are necessary to realize the effective use of data for the operational optimization of buildings and districts. Depending on which of these – or other – components had to be installed additionally for the digital application, the corresponding environmental impact must be included in the balance sheet. All life cycle phases must be taken into account. Here you will find important components and their environmental impact."
        #     in descriptionText.text)
        #
        descriptionDownloadLink = (
            componentsListPageObj.getDescriptionDownloadLink()
        )

        descriptionImageDiv = componentsListPageObj.getDescriptionImage()
        self.assertIsNotNone(descriptionImageDiv)

        # check if the image is displayed:
        imageInDivContainer = componentsListPageObj.getDescendantsByTagName(
            descriptionImageDiv, "img"
        )
        self.assertIsNotNone(imageInDivContainer)

        self.checkIfImageIsDisplayed(imageInDivContainer[0])

        downloadlink = componentsListPageObj.getDownloadLink()
        self.assertTrue(
            self.ECOLOGICAL_COLOR in downloadlink.value_of_css_property("color")
        )

        self.assertTrue(
            "downloads/EWB_Digi_Komponenten.xlsx"
            in downloadlink.get_attribute("href")
        )

    def testSearchContainer(self):
        """Test the search-container of the components-list page

        This includes the full-text-search and the selection-fields

        """
        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLanguageToGerman()

        searchBarObj = SearchPage(self.driver)

        searchContainer = componentsListPageObj.getSearchContainer()
        self.assertIsNotNone(searchContainer)

        # check if a search-input field is present
        searchInputField = componentsListPageObj.getSearchInputField()
        self.assertIsNotNone(searchInputField)

        # check if 2 selection-fields are present and if they contain the
        # data for Category and ComponentClass
        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )
        self.assertEqual(
            len(selectionFields),
            3,
            "There are not 4 selection-fields present",
        )

        divDropwdownElements = componentsListPageObj.getOptionsForSelect(
            selectionFields[0]
        )

        categoryOptionsSet = [
            divDropdown.text for divDropdown in divDropwdownElements
        ]

        # check if the selection-fields contain the correct data
        categorySet = set(
            [
                "Aktuatoren",
                "Signaleverarbeitung",
                "Infrastruktur",
                "Sensorik",
            ]
        )
        # check if the placeholders are correct for german:
        inputOfMultiSelects = componentsListPageObj.getInputOfMultiSelects()
        self.assertEqual(len(inputOfMultiSelects), 3)

        self.assertEqual(
            inputOfMultiSelects[0].get_attribute("placeholder"), "Kategorie"
        )
        self.assertEqual(
            inputOfMultiSelects[1].get_attribute("placeholder"), "Komponente"
        )
        self.assertEqual(
            inputOfMultiSelects[2].get_attribute("placeholder"), "Sortierung"
        )

        self.assertTrue(categorySet.issubset(categoryOptionsSet))

        componentsSet = set(
            [
                "Volumenstromregler",
                "Datenlogger",
                "Luftleitung",
                "Umwälzpumpe",
                "Präsenzmelder",
            ]
        )
        componentClassSelectionField = set(
            [optionElement.text for optionElement in selectionFields[1].options]
        )
        divDropwdownElements = componentsListPageObj.getOptionsForSelect(
            selectionFields[1]
        )
        componentClassSelectionField = [
            divDropdown.text for divDropdown in divDropwdownElements
        ]

        self.assertTrue(componentsSet.issubset(componentClassSelectionField))

        # check if the selection fields "sorting" and "overview" are present
        sortingDropdownField = selectionFields[2]
        self.scrollElementIntoViewAndClickIt(sortingDropdownField)
        sortingOptions = componentsListPageObj.getDropdownElements(
            sortingDropdownField
        )

        # check if the sorting-dropdown contains the correct elements:
        sortingList = [
            "Kategorie",
            "Komponente",
            "Energieverbrauch Nutzung",
            "Treibhauspotenzial",
            "Bauteilgewicht",
            "Lebensdauer",
        ]
        # sortingOptionsInDropdown = set(
        #     [optionElement.text for optionElement in sortingOptions])
        # self.assertTrue(sortingSet.issubset(sortingOptionsInDropdown))
        # randomly click one of the elements of the sorting-dropdown:

        chosenElement = choice(sortingOptions)
        foundMatch = False
        for element in sortingList:
            if element in chosenElement.text:
                foundMatch = True
                break
        self.assertTrue(foundMatch)

        parentOfChosenElement = componentsListPageObj.getParentElement(
            chosenElement
        )
        chosenElement.click()
        nestedDropdownItems = componentsListPageObj.getNestedDropdownElements(
            parentOfChosenElement
        )
        nestedOptionsText = [option.text for option in nestedDropdownItems]
        self.assertEqual(len(nestedOptionsText), 2)
        self.assertIn("Aufsteigend", nestedOptionsText)
        self.assertIn("Absteigend", nestedOptionsText)

        chosenNestedItem = choice(nestedDropdownItems)
        chosenNestedItemText = chosenNestedItem.text
        chosenElementText = chosenElement.text
        self.scrollElementIntoViewAndClickIt(chosenNestedItem)

        self._checkIfOrderingIsLikeSpecified(
            chosenElementText, chosenNestedItemText, componentsListPageObj
        )
        # check if the elements are now ordered in the specified way
        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )

        self._setLanguageToEnglish()

        categorySet = set(
            [
                "Actuators",
                "Signal processing",
                "Infrastructure",
                "Sensors",
            ]
        )

        componentsSet = set(
            [
                "Flow controller",
                "Data logger",
                "Air duct",
                "Circulation pump",
                "Presence sensor",
            ]
        )

        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )

        # check if the placeholders are correct for english:
        self.assertEqual(selectionFields[0].options[0].text, "Category")
        self.assertEqual(selectionFields[1].options[0].text, "Component")

        categoryOptionsSet = set(
            [optionElement.text for optionElement in selectionFields[0].options]
        )
        componentClassSelectionField = set(
            [optionElement.text for optionElement in selectionFields[1].options]
        )

        self.assertTrue(componentsSet.issubset(componentClassSelectionField))
        self.assertTrue(categorySet.issubset(categoryOptionsSet))

        # change the language back to german:
        self._setLanguageToGerman()

        # test the functionality of the search-input field:
        searchInputField = componentsListPageObj.getSearchInputField()
        searchInputField.send_keys("Volumenstromregler")
        searchInputField.send_keys(Keys.RETURN)
        time.sleep(1)
        searchResultsComponents = componentsListPageObj.getAllListElements()
        self.assertTrue(len(searchResultsComponents) >= 1)

        # in each result, the search-string should be present:
        for component in searchResultsComponents:
            self.assertTrue("Volumenstromregler" in component.text)

        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )
        # test the functionality of the category-selection field:
        categorySelectionField = selectionFields[0]
        self._checkIfSelectFieldsWorks(
            categorySelectionField, componentsListPageObj
        )

        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )

        self._checkIfSelectFieldsWorks(
            selectionFields[1], componentsListPageObj
        )

        # test the functionality of the overview selection field:
        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer()
        )
        self._checkIfSelectFieldsWorks(
            selectionFields[3], componentsListPageObj, True
        )

        # check if 2 radio-buttons are present in the search bar:
        radioButtons = searchBarObj.getRadioButtons()
        self.assertEqual(len(radioButtons), 2)

        textOfRadioButtons = {
            "de": ["Detail Ansicht", "Vergleichsmodus"],
            "en": ["Detail view", "Comparison mode"],
        }

        for radioindex, radioButton in enumerate(radioButtons):
            self.assertTrue(radioButton.is_displayed())
            self.assertTrue(
                radioButton.get_css_value("border-color")
                == self.ECOLOGICAL_COLOR
            )
            descriptionTextOfRadio = searchBarObj.getNextSibling(radioButton)
            self.assertTrue(descriptionTextOfRadio.tag_name == "span")
            self.assertTrue(
                descriptionTextOfRadio.text
                == textOfRadioButtons[self.getLanguage()][radioindex]
            )
            self.assertTrue(
                descriptionTextOfRadio.get_css_value("color")
                == self.ECOLOGICAL_COLOR,
                "Color of the SPan element shpuld be ecological color!",
            )

        # check if the functionallity of the radio buttons work
        # first radio button should expand all card listings

        # check if the cards have the
        cardsList = searchBarObj.getAllElementsOfClass("ListElement")
        self.assertTrue(len(cardsList) > 0)
        for card in cardsList:
            # in each card should be 2 collapsed containers
            self.assertEqual(
                len(searchBarObj.getDescendantsByClass(card, "collapse")), 2
            )

        # click the first radio button
        radioButtons[0].click()
        for card in cardsList:
            # in each card should be 2 showed containers
            self.assertEqual(
                len(searchBarObj.getDescendantsByClass(card, "show")), 2
            )

        # check functionallity of second radio button:
        radioButtons[1].click()
        # check if checkboxes in each card are present
        for card in cardsList:
            checkboxForCar = searchBarObj.getDescendantsByTagName(
                card, "input"
            )[0]
            self.assertTrue(
                checkboxForCar.get_css_value("visibility") == "visible"
            )
            self.assertTrue(
                checkboxForCar.get_css_value("border-color")
                == self.ECOLOGICAL_COLOR
            )
        # check if the start compare and reset button are shown:

        compareSectionObj = ComparisonPageSection(self.driver)
        startCompareDiv = compareSectionObj.getSecondComparisonDiv()
        self.assertTrue(startCompareDiv.is_displayed())

        # check if the comare button and the reset button are present:
        startCompareDiv = compareSectionObj.getStartComparisonDiv()
        self.assertTrue(startCompareDiv.is_displayed())
        self.assertTrue(
            startCompareDiv.get_css_value("background-color")
            == self.ECOLOGICAL_COLOR
        )
        self.assertTrue(
            "Vergleiche" in startCompareDiv.text
            or "Compare" in startCompareDiv.text
        )

        # check if the Reset button exists
        resetCompareDiv = compareSectionObj.getResetComparisonDiv()
        self.assertTrue(resetCompareDiv.is_displayed())
        self.assertTrue(
            resetCompareDiv.get_css_value("background-color")
            == "rgb(255, 255, 255)"
        )
        self.assertTrue(
            resetCompareDiv.get_css_value("border-color")
            == self.ECOLOGICAL_COLOR
        )
        self.assertTrue(
            "Zurücksetzen" in resetCompareDiv.text
            or "Reset" in resetCompareDiv.text
        )

    def testDifferentFiltersInSearch(self):
        """Test if Adding and Removing search-filters works as expected."""
        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()

        searchBarObj = SearchPage(self.driver)
        # use free tect search:
        searchInputField = componentsListPageObj.getSearchInputField()

        searchInputField.send_keys("Schneider Electric")
        searchInputField.send_keys(Keys.RETURN)

        time.sleep(1)
        
        showMoreObjs = componentsListPageObj.getShowMoreElements()
        self.assertGreaterEqual(len(showMoreObjs), 1)
        # self.assertGreaterEqual(len(searchFilters), 1)
        
        searchInput = self.driver.find_element(By.ID, "search-input-")
        self.assertTrue("Schneider Electric" in searchInput.get_attribute("value"))
        self.assertTrue(
            searchInput.value_of_css_property("border-color")
            == self.ECOLOGICAL_COLOR
        )

    def testIfCompareSectionIsPresent(self):
        """test if the compare section below the search container is present"""
        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLanguageToGerman()

        compareDiv = componentsListPageObj.getCompareContainer()
        # self.assertIsNotNone(compareDiv)

        compareButtons = componentsListPageObj.getDescendantsByTagName(
            compareDiv, "h6"
        )
        activeCompareElements = []
        for element in compareButtons:
            if element.is_displayed():
                activeCompareElements.append(element)

        self.assertEqual(len(activeCompareElements), 0)

        
        triggerComparisonMode = componentsListPageObj.getCompareRadio()

        # check if 2 other buttons appear, if the compareButton[0] is clicked:
        self.scrollElementIntoViewAndClickIt(triggerComparisonMode)

        activeCompareElements = []
        for element in compareButtons:
            if element.is_displayed():
                activeCompareElements.append(element)

        self.assertEqual(len(activeCompareElements), 2)
        self.assertEqual(activeCompareElements[0].text, "Vergleiche")
        self.assertEqual(activeCompareElements[1].text, "Zurücksetzen")
        
        # check if checkboxes appear in each component div, if the compareButton[0] is clicked:
        components = componentsListPageObj.getAllListElements()
        for component in components:
            checkbox = componentsListPageObj.getDescendantsByTagName(
                component, "input"
            )
            self.assertIsNotNone(checkbox)
            self.assertEqual(checkbox[0].get_attribute("type"), "checkbox")

        # choose 2 components and activate their checkboxes:
        component1 = choice(components)
        components.remove(component1)
        component2 = choice(components)

        self.scrollElementIntoViewAndClickIt(
            componentsListPageObj.getDescendantsByTagName(component1, "input")[
                0
            ]
        )

        self.scrollElementIntoViewAndClickIt(
            componentsListPageObj.getDescendantsByTagName(component2, "input")[
                0
            ]
        )

        self.scrollElementIntoViewAndClickIt(activeCompareElements[0])

        compareSectionObj = ComparisonPageSection(self.driver)
        
        # the content container should contain 2 sections, which are represented by 2 divs:
        columnsInFirstRow = self.driver.find_element(By.XPATH, "//tr").find_elements(By.XPATH, "./td")

        self.assertEqual(len(columnsInFirstRow), 2)
        
        backLink = self.driver.find_element(By.XPATH, "//a[contains(@href, '/component_list/components')]")


        siblingElement = compareSectionObj.getDescendantsByTagName(
            backLink, "img"
        )[0]
        # no alt text should be present, because the image is loaded successfully:
        self.assertTrue(siblingElement.text == "")
        self.assertTrue(
            backLink.value_of_css_property("color")
            == self.ECOLOGICAL_COLOR
        )
        self.assertTrue(
            backLink.value_of_css_property(
                "font-size"
            )
            == "15px"
        )

        # test if the back-button points back to components-listing page:
        backLink.click()

        self.waitUntilConditionIsMet(
            lambda d: self.driver.title == "Effort for used components"
            or self.driver.title == "Aufwände für verwendete Komponenten"
        )
        
        triggerComparisonMode = componentsListPageObj.getCompareRadio()
        self.scrollElementIntoViewAndClickIt(triggerComparisonMode)
        
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        breakpoint()
        for checkbox in checkboxes:
            
            self.assertFalse(checkbox.is_selected())
        
        
        


    def _checkIfComponentsPresent(self, translationElement):
        """Check if components are listed on the listing site."""
        components = self.componentsListPageObj.getAllListElements()
        self.assertGreater(len(components), 1)

    def testIfComponentListingContainer(self):
        """Test if the component listing container is present"""

        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )
        self.componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()

        self.checkInGermanAndEnglish(
            self._checkIfComponentsPresent,
            {
                "de": "",
                "en": "",
            },
        )

        componentClass = [
            "Volumenstromregler",
            "Datenlogger",
            "Luftleitung",
            "Umwälzpumpe",
            "Präsenzmelder",
        ]

        categoryElements = [
            "Aktuatoren",
            "Signaleverarbeitung",
            "Infrastruktur",
            "Sensorik",
        ]

        self._setLanguageToGerman()

        components = self.componentsListPageObj.getAllListElements()

        # check if the componentListingContainer contains the correct number of elements:
        for index, component in enumerate(components):
            # check if each component div has a border-ecological div-class:
            self.assertTrue(
                "border-ecological" in component.get_attribute("class")
            )

            # each component should contain a "Mehr anzeigen" expanding element:
            expandElement = self.componentsListPageObj.getDescendantsByTagName(
                component, "a"
            )
            self.assertIsNotNone(expandElement[0])
            self.assertTrue(
                "Zeige mehr"
                in expandElement[0].get_attribute("data-collapsed-text")
            )
            # self.scrollElementIntoViewAndClickIt(
            #         component.find_element(By.XPATH, ".//a")
            # )
            # self._checkIfStrElementFromListIsDisplayed(component,
            #                                            componentClass)
            # self._checkIfStrElementFromListIsDisplayed(component,
            #                                            categoryElements)

            self.assertTrue("Quelle" not in component.text)
            self.assertTrue("Weitere Informationen" not in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzungsphase (gesamt; in kWh/Jahr):" in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (gesamt; in kg CO2-e):" in component.text
            )
            self.assertTrue("Bauteilgewicht (in kg):" in component.text)
            self.assertTrue("Lebensdauer (in Jahre):" not in component.text)

            collapsedContainer = (
                self.componentsListPageObj.getDescendantsByClass(
                    component, "collapse"
                )
            )
            self.assertEqual(len(collapsedContainer), 3)

            self.assertTrue(not collapsedContainer[0].is_displayed())
            # check if the not shown elements are present after the expandElement is clicked:

            self.scrollElementIntoViewAndClickIt(expandElement[0])

            self.assertTrue(collapsedContainer[0].is_displayed())

            # check if the not shown elements are present after the expandElement is clicked:
            self.assertTrue("Quelle" in component.text)
            self.assertTrue("Weitere Informationen" in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzungsphase (gesamt; in kWh/Jahr):" in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (gesamt; in kg CO2-e):" in component.text
            )
            self.assertTrue("Bauteilgewicht (in kg):" in component.text)
            self.assertTrue("Lebensdauer (in Jahre)" in component.text)

            self.assertTrue(
                "Leistung Nutzungsphase (akitv; in W):" in component.text
            )
            self.assertTrue(
                "Leistung Nutzungsphase (passiv/ Stand-by; in W):"
                in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Herstellung; in kg CO2-e):"
                in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Nutzung; in kg CO2-e):" in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Entsorgung; in kg CO2-e):"
                in component.text
            )

            # get all elements, which hold numerical values:
            numericalValuesInListingRow = (
                self.componentsListPageObj.getDescendantsByClass(
                    component, "listingRowAttributeValues"
                )
            )
            self.assertGreaterEqual(
                len(numericalValuesInListingRow),
                9,
                "At least 9 containers, which can hold numerical values should be present in the listing cell.",
            )
            for numericalValue in numericalValuesInListingRow:
                textContent = numericalValue.text
                if "n/a" in textContent:
                    continue
                else:
                    if "." in textContent:
                        getTheDecimalPlaces = textContent.split(".")[1]
                    elif "," in textContent:
                        getTheDecimalPlaces = textContent.split(",")[1]
                    else:
                        getTheDecimalPlaces = ""
                    decimalPlaceCount = 0
                    for decimalPlace in getTheDecimalPlaces:
                        if decimalPlace in "123456789":
                            decimalPlaceCount += 1
                    self.assertLessEqual(
                        decimalPlaceCount,
                        2,
                        "There should only be 2 decimal places.",
                    )

            # check if the list-elements can collapsed again:
            self.scrollElementIntoViewAndClickIt(expandElement[0])
            time.sleep(1)
            self.assertTrue("Quelle" not in component.text)
            self.assertTrue("Weitere Informationen" not in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzung (aktiv; in W)" not in component.text
            )
            self.assertTrue(
                "Energieverbrauch Nutzung (passiv/ Stand-by; in W):"
                not in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Herstellung; in kg CO2-e):"
                not in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Nutzung; in kg CO2-e):"
                not in component.text
            )
            self.assertTrue(
                "Treibhauspotenzial (Entsorgung; in kg CO2-e):"
                not in component.text
            )

        # select english language and check if the component-attributes are translated:
        self._setLanguageToEnglish()
        components = self.componentsListPageObj.getAllListElements()

        randomComponent = choice(components)

        # expand the random component:
        expandElement = self.componentsListPageObj.getDescendantsByTagName(
            randomComponent, "a"
        )
        self.scrollElementIntoViewAndClickIt(expandElement[0])

        self.assertTrue(
            "Energy consumption usage phase (total; in kWh/year):" in randomComponent.text
        )
        self.assertTrue(
            "Total greenhouse gas potential (in kg CO2-e)"
            in randomComponent.text
        )
        self.assertTrue("Component weight (in kg):" in randomComponent.text)
        self.assertTrue("Lifespan (in years)" in randomComponent.text)
        self.assertTrue(
            "Power usage phase (active; in W):" in randomComponent.text
        )
        self.assertTrue(
            "Power usage phase (passive/stand-by; in W):" in randomComponent.text
        )
        self.assertTrue(
            "Greenhouse gas potential (production; in kg CO2-e)"
            in randomComponent.text
        )
        self.assertTrue(
            "Greenhouse gas potential (usage; in kg CO2-e)"
            in randomComponent.text
        )
        self.assertTrue(
            "Greenhouse gas potential (disposal; in kg CO2-e)"
            in randomComponent.text
        )
        self.assertTrue("Source" in randomComponent.text)
        self.assertTrue("Further information" in randomComponent.text)
        # self._checkIfStrElementFromListIsDisplayed(
        #     randomComponent,
        #     [
        #         "Actuators",
        #         "Signal processing",
        #         "Infrastructure",
        #         "Sensors",
        #     ],
        # )
        # self._checkIfStrElementFromListIsDisplayed(
        #     randomComponent,
        #     [
        #         "Flow controller",
        #         "Data logger",
        #         "Air duct",
        #         "Circulating pump",
        #         "Presence detector",
        #     ],
        # )
        #

    def testPagination(self):
        """Test if the pagination elements are present and working"""
        self.driver.get(
            os.environ["siteUnderTest"] + "/component_list/components"
        )
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLanguageToGerman()

        paginatorContainer = componentsListPageObj.getPaginationContainer()
        self.assertIsNotNone(paginatorContainer)

    def _checkIfStrElementFromListIsDisplayed(self, component, elementList):
        """Check if a string-element from a list is displayed"""
        isElementFound = False
        for element in elementList:
            if element in component.text:
                isElementFound = True
                break
        self.assertTrue(isElementFound)

    def _checkIfSelectFieldsWorks(
        self, selectionField, componentsListPageObj, overviewSelect=False
    ):
        """Check if the selection field works"""
        randomChoiceFromSelect = choice(selectionField.options[1:])
        randomChoiceFromSelectText = randomChoiceFromSelect.text

        self.scrollElementIntoView(randomChoiceFromSelect)

        selectionField.select_by_visible_text(randomChoiceFromSelectText)

        searchSubmitButton = componentsListPageObj.getSearchSubmitButton()
        searchSubmitButton.click()
        time.sleep(1)
        searchResultsComponents = componentsListPageObj.getAllListElements()
        self.assertTrue(len(searchResultsComponents) >= 1)

        if overviewSelect:
            if (
                randomChoiceFromSelectText == "Expanded"
                or randomChoiceFromSelectText == "Ausgeklappt"
            ):
                for component in searchResultsComponents:
                    self.assertTrue("Quelle" in component.text)
                    self.assertTrue("Weitere Informationen" in component.text)
            else:
                for component in searchResultsComponents:
                    self.assertTrue("Quelle" not in component.text)
                    self.assertTrue(
                        "Weitere Informationen" not in component.text
                    )
            return
        # in each result, the search-string should be present:
        for component in searchResultsComponents:
            self.assertTrue(randomChoiceFromSelectText in component.text)

    def _checkIfOrderingIsLikeSpecified(
        self,
        clickedAttributeElement,
        clickedOrderingElement,
        componentsListPageObj,
    ):
        """Check if the ordering is like specified in the nested dropdown"""

        allPresentComponentContainers = (
            componentsListPageObj.getAllListElements()
        )

        attributesSortedAlphabetically = {
            "de": [
                "Kategorie",
                "Komponente",
            ],
            "en": [
                "Category",
                "Component",
            ],
        }
        attributesSortedNumerically = {
            "de": [
                "Energieverbrauch Nutzung (gesamt; in W)",
                "Treibhauspotenzial (gesamt; in kg CO2-e)",
                "Bauteilgewicht (in kg)",
                "Lebensdauer (in Jahren)",
                "Energieverbrauch Nutzung (aktiv; in W)",
                "Energieverbrauch Nutzung (passiv/ Stand-by; in W)",
                "Treibhauspotenzial (Herstellung; in kg CO2-e)",
                "Treibhauspotenzial (Nutzung; in kg CO2-e)",
                "Treibhauspotenzial (Entsorgung; in kg CO2-e)",
            ],
            "en": [
                "Category",
                "Component",
            ],
        }
        extractedAttributeForComponents = []
        if (
            clickedAttributeElement == "Kategorie"
            or clickedAttributeElement == "Category"
        ):
            for component in allPresentComponentContainers:
                # check if the elements are sorted alphabetically:
                extractedAttributeForComponents.append(
                    componentsListPageObj.getDescendantsByTagName(
                        component, "h3"
                    )[0].text
                )
        elif (
            clickedAttributeElement == "Komponente"
            or clickedAttributeElement == "Component"
        ):
            for component in allPresentComponentContainers:
                extractedAttributeForComponents.append(
                    componentsListPageObj.getDescendantsByClass(
                        component, "subHeading"
                    )[0].text
                )

        else:
            for component in allPresentComponentContainers:
                # before extracting the information, the container has to be
                # extended, so that the information is present:
                collapsedContainerList = (
                    componentsListPageObj.getDescendantsByClass(
                        component, "collapse"
                    )
                )
                self.driver.execute_script(
                    "arguments[0].setAttribute('class', 'show')",
                    collapsedContainerList[0],
                )
                self.driver.execute_script(
                    "arguments[0].setAttribute('class', 'show')",
                    collapsedContainerList[1],
                )
                floatOrNone = self._findNextFloat(
                    component.text, clickedAttributeElement + ":"
                )
                if floatOrNone is not None:
                    extractedAttributeForComponents.append(floatOrNone)
                else:
                    extractedAttributeForComponents.append(None)

                # check if the elements are sorted alphabetically:
                # breakpoint()
                # extractedAttributeForComponents.append(
                #     componentsListPageObj.getDescendantsByTagName(
                #         component, "h3")[0].text)

        if clickedOrderingElement in attributesSortedAlphabetically:
            if (
                clickedOrderingElement == "Ascending"
                or clickedOrderingElement == "Aufsteigend"
            ):
                self.assertTrue(self._isSorted(extractedAttributeForComponents))
            else:
                self.assertTrue(
                    self._isSortedReverse(extractedAttributeForComponents)
                )
        # check if the elements are sorted numerically:
        else:
            if (
                clickedOrderingElement == "Ascending"
                or clickedOrderingElement == "Aufsteigend"
            ):
                self.assertTrue(self._isSorted(extractedAttributeForComponents))
            else:
                self.assertTrue(
                    self._isSortedReverse(extractedAttributeForComponents)
                )

    def _findNextFloat(self, text, substring):
        pattern = re.escape(substring) + r"\s*([\d\.]+)"
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
        else:
            return None

    def _isSorted(self, listToCheck):
        """Check if a list is sorted alphabetically"""
        if None in listToCheck:
            return True
        return listToCheck == sorted(listToCheck)

    def _isSortedReverse(self, listToCheck):
        """Check if a list is sorted alphabetically"""
        if None in listToCheck:
            return True
        return listToCheck == sorted(listToCheck, reverse=True)
