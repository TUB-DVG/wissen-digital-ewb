import os
from random import choice
import sys

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

        # change the language to english and check if the english heading is displayed
        footerObj = Footer(self.driver)
        selectionField = footerObj.getLanguageSelectionField()
        options = selectionField.options

        # click the cookie-banner away
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerButton = cookieBannerObj.getCookieAcceptanceButton()

        self.scrollElementIntoViewAndClickIt(cookieBannerButton)

        for option in options:
            if option.text == "English":
                self.scrollElementIntoViewAndClickIt(option)

                break
            elif option.text == "Englisch":
                self.scrollElementIntoViewAndClickIt(option)
                break

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

        # check if a search-input field is present
        searchInputField = componentsListPageObj.getSearchInputField()
        self.assertIsNotNone(searchInputField)

        # check if 2 selection-fields are present and if they contain the
        # data for Category and ComponentClass
        selectionFields = componentsListPageObj.getSelectionFields()
        self.assertEqual(
            len(selectionFields),
            2,
            "There are not 2 selection-fields present",
        )

        # check if the selection-fields contain the correct data
        categorySet = set([
            "Aktuatoren",
            "Signaleverarbeitung",
            "Infrastruktur",
            "Sensorik",
        ])
        categoryOptionsSet = set(selectionFields[0].options)
        self.assertTrue(categorySet.issubset(categoryOptionsSet))

        componentsSet = set([
            "Volumenstromregler",
            "Datenlogger",
            "Luftleitung",
            "Umwälzpumpe",
            "Präsenzmelder",
        ])
        componentClassSelectionField = set(selectionFields[1].options)
        self.assertTrue(componentsSet.issubset(componentClassSelectionField))
