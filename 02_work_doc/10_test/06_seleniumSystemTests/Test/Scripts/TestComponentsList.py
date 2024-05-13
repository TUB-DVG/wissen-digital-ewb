import os
from random import choice
import sys
import time
from random import choice

sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Src.PageObject.Pages.cookieBanner import CookieBanner
from Src.PageObject.Pages.Footer import Footer
from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.NegativeEnvironmentalImpacts import (
    NegativeEnvironmentalImpacts, )
from Src.PageObject.Pages.ComponentListPage import ComponentListPage


class TestComponentsList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def testComponentPageExists(self):
        """Test if the Components-List Page exists and is accessible via url and navbar"""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/pages/environmentalIntegrityNegativ")
        self.assertTrue("Negative environmental impacts" in self.driver.title
                        or "Negative Umweltwirkungen" in self.driver.title)

        self.driver.get(os.environ["siteUnderTest"])
        navBar = NavBar(self.driver)
        linkToPage = navBar.returnNegativeEnvironmentalImpactLink()
        # breakpoint()
        self.scrollElementIntoView(linkToPage[1])
        linkToPage[1].click()
        self.assertTrue("Negative environmental impacts" in self.driver.title
                        or "Negative Umweltwirkungen" in self.driver.title)

    def testStructureOfPage(self):
        """Test if a div-element is present, in which the content is wraped

        This test-method is part of the test-first-dev cycle. It tests if a outer
        div exists, which is of css-class `content`. Inside this div, there should be
        a div-wrapper for the description text, which is again composed of a heading and the
        text. In the bottom part of the page, there should be 2 boxes, which further contents.
        """

        self.driver.get(os.environ["siteUnderTest"] +
                        "/pages/environmentalIntegrityNegativ")
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
        self.driver.get(os.environ["siteUnderTest"] +
                        "/pages/environmentalIntegrityNegativ")
        impactsObj = NegativeEnvironmentalImpacts(self.driver)
        boxes1and2 = impactsObj.getBox1and2()
        # click the box since the <a> cant be clicked directly by selenium
        linkToComponentList = boxes1and2[0]
        linkToComponentList.click()
        self.assertTrue("Components list" in self.driver.title
                        or "Komponentenliste" in self.driver.title)
        self.driver.back()

        linkToDataProcessing = boxes1and2 = impactsObj.getBox1and2()[1]
        linkToDataProcessing.click()
        self.assertTrue("Data processing" in self.driver.title
                        or "Datenverarbeitung" in self.driver.title)

    def testComponentListPage(self):
        """Test the structure of the sub-page of the negative environmental impacts page"""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/component_list/components")

        componentsListPageObj = ComponentListPage(self.driver)
        divContent = componentsListPageObj.getContentDiv()
        self.assertIsNotNone(divContent)

        secondaryNavbarDiv = componentsListPageObj.getSecondaryNavbar()
        self.assertIsNotNone(secondaryNavbarDiv)

        # test if the secondaryNavBar holds 2 links:
        linksInSecNavBar = componentsListPageObj.getDescendantsByTagName(
            secondaryNavbarDiv, "a")
        self.assertEqual(
            len(linksInSecNavBar),
            2,
            "The secondaryNavBar does not hold 2 links",
        )

        # test if the links are working
        linkToDataProcessing = linksInSecNavBar[1]
        linkToDataProcessing.click()
        self.assertTrue("Data processing" in self.driver.title
                        or "Datenverarbeitung" in self.driver.title)

        self.driver.back()

        secondaryNavbarDiv = componentsListPageObj.getSecondaryNavbar()
        linkToEnvironmentalImpacts = (
            componentsListPageObj.getDescendantsByTagName(
                secondaryNavbarDiv, "a")[0])
        linkToEnvironmentalImpacts.click()
        self.assertTrue("Negative environmental impacts" in self.driver.title
                        or "Negative Umweltwirkungen" in self.driver.title)

        self.driver.back()

        # test the description section:
        descriptionSection = componentsListPageObj.getDescriptionSection()
        self.assertIsNotNone(descriptionSection)

        descriptionHeading = componentsListPageObj.getDescriptionHeading()
        self.assertIsNotNone(descriptionHeading)

        # check if the heading is displayed inside the div:
        headingText = descriptionHeading.text
        self.assertTrue("Aufwände für verwendete Komponenten" in headingText
                        or "Effort for used components" in headingText)

        self._setLanguageToEnglish()

        descriptionHeading = componentsListPageObj.getDescriptionHeading()
        headingText = descriptionHeading.text
        self.assertTrue("Effort for used components" in headingText)

        descriptionText = componentsListPageObj.getDescriptionText()
        self.assertIsNotNone(descriptionText)
        self.assertTrue(
            "In analogy to the data value chain (see 'Expenses for data processing processes'), important components can be thought of from data acquisition (sensors) to data use (actuators). Figure 2 shows important components that are necessary to realize the effective use of data for the operational optimization of buildings and districts. Depending on which of these – or other – components had to be installed additionally for the digital application, the corresponding environmental impact must be included in the balance sheet. All life cycle phases must be taken into account. Here you will find important components and their environmental impact."
            in descriptionText.text)

        descriptionDownloadLink = (
            componentsListPageObj.getDescriptionDownloadLink())
        self.assertIsNotNone(descriptionDownloadLink)

        descriptionImageDiv = componentsListPageObj.getDescriptionImage()
        self.assertIsNotNone(descriptionImageDiv)

        # check if the image is displayed:
        imageInDivContainer = componentsListPageObj.getDescendantsByTagName(
            descriptionImageDiv, "img")
        self.assertIsNotNone(imageInDivContainer)

        self.checkIfImageIsDisplayed(imageInDivContainer[0])

    def testSearchContainer(self):
        """Test the search-container of the components-list page

        This includes the full-text-search and the selection-fields

        """
        self.driver.get(os.environ["siteUnderTest"] +
                        "/component_list/components")
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLangaugeToGerman()

        searchContainer = componentsListPageObj.getSearchContainer()
        self.assertIsNotNone(searchContainer)

        # check if a search-input field is present
        searchInputField = componentsListPageObj.getSearchInputField()
        self.assertIsNotNone(searchInputField)

        # check if 2 selection-fields are present and if they contain the
        # data for Category and ComponentClass
        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer())
        self.assertEqual(
            len(selectionFields),
            4,
            "There are not 4 selection-fields present",
        )

        # check if the selection-fields contain the correct data
        categorySet = set([
            "Aktuatoren",
            "Signaleverarbeitung",
            "Infrastruktur",
            "Sensorik",
        ])

        # check if the placeholders are correct for german:
        self.assertEqual(selectionFields[0].options[0].text, "Kategorie")
        self.assertEqual(selectionFields[1].options[0].text, "Komponente")

        categoryOptionsSet = set([
            optionElement.text for optionElement in selectionFields[0].options
        ])

        self.assertTrue(categorySet.issubset(categoryOptionsSet))

        componentsSet = set([
            "Volumenstromregler",
            "Datenlogger",
            "Luftleitung",
            "Umwälzpumpe",
            "Präsenzmelder",
        ])
        componentClassSelectionField = set([
            optionElement.text for optionElement in selectionFields[1].options
        ])
        self.assertTrue(componentsSet.issubset(componentClassSelectionField))

        # check if the selection fields "sorting" and "overview" are present
        sortingSet = set([
            "Aufsteigend",
            "Absteigend",
        ])
        sortingOptionsSet = set([
            optionElement.text for optionElement in selectionFields[2].options
        ])

        overviewSet = set([
            "Ausgeklappt",
            "Eingeklappt",
        ])
        overviewOptionsSet = set([
            optionElement.text for optionElement in selectionFields[3].options
        ])

        self.assertTrue(sortingSet.issubset(sortingOptionsSet))
        self.assertTrue(overviewSet.issubset(overviewOptionsSet))

        self._setLanguageToEnglish()

        categorySet = set([
            "Actuators",
            "Signal processing",
            "Infrastructure",
            "Sensors",
        ])

        componentsSet = set([
            "Flow controller",
            "Data logger",
            "Air duct",
            "Circulation pump",
            "Presence sensor",
        ])
        sortingSet = set([
            "Ascending",
            "Descending",
        ])
        overviewSet = set([
            "Expanded",
            "Collapsed",
        ])
        selectionFields = (
            componentsListPageObj.getSelectFieldsInSearchContainer())

        # check if the placeholders are correct for english:
        self.assertEqual(selectionFields[0].options[0].text, "Category")
        self.assertEqual(selectionFields[1].options[0].text, "Component")
        self.assertEqual(selectionFields[2].options[0].text, "Sorting")
        self.assertEqual(selectionFields[3].options[0].text, "Overview")

        categoryOptionsSet = set([
            optionElement.text for optionElement in selectionFields[0].options
        ])
        componentClassSelectionField = set([
            optionElement.text for optionElement in selectionFields[1].options
        ])
        sortingSetSelectionField = set([
            optionElement.text for optionElement in selectionFields[2].options
        ])
        overviewSetSelectionField = set([
            optionElement.text for optionElement in selectionFields[3].options
        ])
        self.assertTrue(componentsSet.issubset(componentClassSelectionField))
        self.assertTrue(categorySet.issubset(categoryOptionsSet))
        self.assertTrue(sortingSet.issubset(sortingSetSelectionField))
        self.assertTrue(overviewSet.issubset(overviewSetSelectionField))

    def testIfCompareSectionIsPresent(self):
        """test if the compare section below the search container is present"""
        self.driver.get(os.environ["siteUnderTest"] +
                        "/component_list/components")
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLangaugeToGerman()

        compareDiv = componentsListPageObj.getCompareContainer()
        self.assertIsNotNone(compareDiv)

        compareButtons = componentsListPageObj.getDescendantsByTagName(
            compareDiv, "h6")
        activeCompareElements = []
        for element in compareButtons:
            if element.is_displayed():
                activeCompareElements.append(element)

        self.assertEqual(len(activeCompareElements), 1)

        self.assertEqual(activeCompareElements[0].text, "Vergleiche")

        # check if 2 other buttons appear, if the compareButton[0] is clicked:
        activeCompareElements[0].click()

        activeCompareElements = []
        for element in compareButtons:
            if element.is_displayed():
                activeCompareElements.append(element)

        self.assertEqual(len(activeCompareElements), 2)
        self.assertEqual(activeCompareElements[0].text, "Vergleiche")
        self.assertEqual(activeCompareElements[1].text, "Zurücksetzen")

    def testIfComponentListingContainer(self):
        """Test if the component listing container is present"""

        self.driver.get(os.environ["siteUnderTest"] +
                        "/component_list/components")
        componentsListPageObj = ComponentListPage(self.driver)

        self._removeCookieBanner()
        self._setLangaugeToGerman()

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

        componentListingContainer = (
            componentsListPageObj.getComponentListingContainer())
        self.assertIsNotNone(componentListingContainer)

        # check if the componentListingContainer contains the correct number of elements:
        components = componentsListPageObj.getAllListElements()
        self.assertEqual(len(components), 3)
        for index, component in enumerate(components):
            # check if each component div has a border-ecological div-class:
            self.assertTrue(
                "border-ecological" in component.get_attribute("class"))

            # each component should contain a "Mehr anzeigen" expanding element:
            expandElement = componentsListPageObj.getDescendantsByTagName(
                component, "a")
            self.assertIsNotNone(expandElement[0])
            self.assertTrue("Zeige mehr" in expandElement[0].get_attribute(
                "data-collapsed-text"))
            self._checkIfStrElementFromListIsDisplayed(component,
                                                       componentClass)
            self._checkIfStrElementFromListIsDisplayed(component,
                                                       categoryElements)

            self.assertTrue("Quelle" not in component.text)
            self.assertTrue("Weitere Informationen" not in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzung (gesamt; in W):" in component.text)
            self.assertTrue(
                "Treibhauspotenzial (gesamt; in kg CO2-e):" in component.text)
            self.assertTrue("Bauteilgewicht (in kg):" in component.text)
            self.assertTrue("Lebensdauer (in Jahren)" in component.text)

            collapsedContainer = componentsListPageObj.getDescendantsByClass(
                component, "collapse")
            # breakpoint()
            self.assertEqual(len(collapsedContainer), 3)

            self.assertTrue(not collapsedContainer[0].is_displayed())
            # check if the not shown elements are present after the expandElement is clicked:
            self.scrollElementIntoViewAndClickIt(expandElement[0])

            self.assertTrue(collapsedContainer[0].is_displayed())

            # check if the not shown elements are present after the expandElement is clicked:
            self.assertTrue("Quelle" in component.text)
            self.assertTrue("Weitere Informationen" in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzung (gesamt; in W):" in component.text)
            self.assertTrue(
                "Treibhauspotenzial (gesamt; in kg CO2-e):" in component.text)
            self.assertTrue("Bauteilgewicht (in kg):" in component.text)
            self.assertTrue("Lebensdauer (in Jahren)" in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzung (aktiv; in W)" in component.text)
            self.assertTrue(
                "Energieverbrauch Nutzung (passiv/ Stand-by; in W):" in
                component.text)
            self.assertTrue("Treibhauspotenzial (Herstellung; in kg CO2-e):" in
                            component.text)
            self.assertTrue(
                "Treibhauspotenzial (Nutzung; in kg CO2-e):" in component.text)
            self.assertTrue("Treibhauspotenzial (Entsorgung; in kg CO2-e):" in
                            component.text)

            # check if the list-elements can collapsed again:
            self.scrollElementIntoViewAndClickIt(expandElement[0])
            time.sleep(1)
            self.assertTrue("Quelle" not in component.text)
            self.assertTrue("Weitere Informationen" not in component.text)

            self.assertTrue(
                "Energieverbrauch Nutzung (aktiv; in W)" not in component.text)
            self.assertTrue(
                "Energieverbrauch Nutzung (passiv/ Stand-by; in W):" not in
                component.text)
            self.assertTrue("Treibhauspotenzial (Herstellung; in kg CO2-e):"
                            not in component.text)
            self.assertTrue("Treibhauspotenzial (Nutzung; in kg CO2-e):" not in
                            component.text)
            self.assertTrue("Treibhauspotenzial (Entsorgung; in kg CO2-e):"
                            not in component.text)

        # select english language and check if the component-attributes are translated:
        self._setLanguageToEnglish()
        components = componentsListPageObj.getAllListElements()

        randomComponent = choice(components)

        # expand the random component:
        expandElement = componentsListPageObj.getDescendantsByTagName(
            randomComponent, "a")
        self.scrollElementIntoViewAndClickIt(expandElement[0])

        self.assertTrue(
            "Total energy consumption (in W)" in randomComponent.text)
        self.assertTrue("Total greenhouse gas potential (in kg CO2-e)" in
                        randomComponent.text)
        self.assertTrue("Component weight (in kg):" in randomComponent.text)
        self.assertTrue("Lifespan (in years)" in randomComponent.text)
        self.assertTrue(
            "Active energy consumption (in W)" in randomComponent.text)
        self.assertTrue("Passive/standby energy consumption (in W)" in
                        randomComponent.text)
        self.assertTrue("Greenhouse gas potential (production; in kg CO2-e)" in
                        randomComponent.text)
        self.assertTrue("Greenhouse gas potential (usage; in kg CO2-e)" in
                        randomComponent.text)
        self.assertTrue("Greenhouse gas potential (disposal; in kg CO2-e)" in
                        randomComponent.text)
        self.assertTrue("Source" in randomComponent.text)
        self.assertTrue("Further information" in randomComponent.text)

    def _removeCookieBanner(self):
        """Remove the cookie-banner from the page"""
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerButton = cookieBannerObj.getCookieAcceptanceButton()
        self.scrollElementIntoViewAndClickIt(cookieBannerButton)

    def _setLangaugeToGerman(self):
        """Set the language of the page to german"""
        # change the language to german and check if the german heading is displayed
        footerObj = Footer(self.driver)
        selectionField = footerObj.getLanguageSelectionField()
        options = selectionField.options

        for option in options:
            if option.text == "Deutsch":
                self.scrollElementIntoViewAndClickIt(option)

                break
            elif option.text == "German":
                self.scrollElementIntoViewAndClickIt(option)
                break

    def _setLanguageToEnglish(self):
        """Set the language of the page to english"""
        # change the language to english and check if the english heading is displayed
        footerObj = Footer(self.driver)
        selectionField = footerObj.getLanguageSelectionField()
        options = selectionField.options

        for option in options:
            if option.text == "English":
                self.scrollElementIntoViewAndClickIt(option)

                break
            elif option.text == "Englisch":
                self.scrollElementIntoViewAndClickIt(option)
                break

    def _checkIfStrElementFromListIsDisplayed(self, component, elementList):
        """Check if a string-element from a list is displayed"""
        isElementFound = False
        for element in elementList:
            if element in component.text:
                isElementFound = True
                break
        self.assertTrue(isElementFound)
