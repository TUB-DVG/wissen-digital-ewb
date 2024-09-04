import os
from random import choice
import sys
import time
import re

sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from Src.PageObject.Pages.cookieBanner import CookieBanner
from Src.PageObject.Pages.Footer import Footer
from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.NegativeEnvironmentalImpacts import (
    NegativeEnvironmentalImpacts,
)
from Src.PageObject.Pages.ComponentListPage import ComponentListPage
from Src.PageObject.Pages.ComparisonPageSection import ComparisonPageSection
from Src.PageObject.Pages.DetailsPage import DetailsPage


class TestNegativeEnvironmentalImpacts(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page"""

    def TestNegativeEnvironmentalImpactsLinks(self):
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

        # check structure of the data-processing page:
        # there should be a conten container present:
        detailsPageObj = DetailsPage(self.driver)
        contentDiv = detailsPageObj.getLinkNavigatorDiv()
        self.assertIsNotNone(contentDiv)

        # check if secondaryNavBar container is present in contentDiv
        secondaryNavBar = detailsPageObj.getSecondaryNavBar()

        # he secondary navbar should contain to divs:
        divsInSecondaryNavBar = detailsPageObj.getDescendantsByTagName(
            secondaryNavBar, "div"
        )
        self.assertEqual(len(divsInSecondaryNavBar), 2)

        # the first div should contain a a-tag and the arrow image:
        imgInLeftSecondaryNavBar = detailsPageObj.getDescendantsByTagName(
            divsInSecondaryNavBar[0], "img"
        )
        self.assertEqual(len(imgInLeftSecondaryNavBar), 1)

        # the img should be shown and no alt-text should be present:
        imgNaturalWidth = imgInLeftSecondaryNavBar[0].get_attribute("naturalWidth")
        self.assertNotEqual(
            imgNaturalWidth,
            "0",
            "Arrow image is not displayed, only alt-text is shown",
        )

        aTagInFirstSecondaryNavBarDiv = detailsPageObj.getDescendantsByTagName(
            divsInSecondaryNavBar[0], "a"
        )
        self.assertEqual(len(aTagInFirstSecondaryNavBarDiv), 1)

        # the a-tag should contain a link to the components list page:
        href = aTagInFirstSecondaryNavBarDiv[0].get_attribute("href")
        self.assertTrue(re.search(r"/component_list/components$", href))

        # the text of the a-tag should be in green color:
        color = aTagInFirstSecondaryNavBarDiv[0].value_of_css_property("color")
        self.assertEqual(color, "rgb(143, 222, 151)")

        self.checkIfElementIsTranslated(
            self.self.getLanguage(),
            aTagInFirstSecondaryNavBarDiv[0].text,
            {
                "de": "Negative Umweltwirkungen",
                "en": " Negative environmental impacts",
            },
        )

        # the second div should contain a a-tag and the arrow image:
        imgInRightSecondaryNavBar = detailsPageObj.getDescendantsByTagName(
            divsInSecondaryNavBar[1], "img"
        )
        self.assertEqual(len(imgInRightSecondaryNavBar), 1)

        # the img should be shown and no alt-text should be present:
        self.assertTrue("" == imgInRightSecondaryNavBar.text)

        aTagInSecondSecondaryNavBarDiv = detailsPageObj.getDescendantsByTagName(
            divsInSecondaryNavBar[1], "a"
        )

        # the a-tag should contain a link to the data processing page:
        href = aTagInSecondSecondaryNavBarDiv[0].get_attribute("href")
        self.assertTrue(re.search(r"/data_processing$", href))

        # the text of the a-tag should be black color and should have a green border:
        color = aTagInSecondSecondaryNavBarDiv[0].value_of_css_property("color")
        self.assertEqual(color, "rgb(0, 0, 0)")
