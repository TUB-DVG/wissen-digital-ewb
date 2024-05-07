import os
from random import choice
import sys
sys.path.append(sys.path[0] + "/...")

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.NavBar import NavBar
from Src.PageObject.Pages.NegativeEnvironmentalImpacts import NegativeEnvironmentalImpacts

class TestComponentsList(WebDriverSetup):
    """Represent the Selenium-Test of the Components-List Page 

    """
    def testComponentPageExists(self):
        """Test if the Components-List Page exists and is accessible via url and navbar

        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ")
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative Umweltwirkungen" in self.driver.title) 
        
        self.driver.get(os.environ["siteUnderTest"])
        navBar = NavBar(self.driver)
        linkToPage = navBar.returnNegativeEnvironmentalImpactLink()
        # breakpoint()
        self.scrollElementIntoView(linkToPage[1])
        linkToPage[1].click()
        self.assertTrue("Negative environmental impacts" in self.driver.title or "Negative Umweltwirkungen" in self.driver.title)

    def testStructureOfPage(self):
        """Test if a div-element is present, in which the content is wraped

        This test-method is part of the test-first-dev cycle. It tests if a outer 
        div exists, which is of css-class `content`. Inside this div, there should be
        a div-wrapper for the description text, which is again composed of a heading and the
        text. In the bottom part of the page, there should be 2 boxes, which further contents.
        """

        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ")
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

        image1NaturalWidth = imageInDivBox1.get_attribute('naturalWidth')
        self.assertNotEqual(image1NaturalWidth, '0', 'Image 1 is not displayed, only alt-text is shown')

        boxHeading2 = impactsObj.getBoxHeading(boxes1and2[1])
        self.assertIsNotNone(boxHeading2)

        boxContent2 = impactsObj.getBoxDescription(boxes1and2[1])
        self.assertIsNotNone(boxContent2)

        boxImage2 = impactsObj.getBoxImage(boxes1and2[1])
        self.assertIsNotNone(boxImage2)

        imageInDivBox2 = impactsObj.getImageInBox(boxes1and2[1])
        self.assertIsNotNone(imageInDivBox2)

        image2NaturalWidth = imageInDivBox2.get_attribute('naturalWidth')
        self.assertNotEqual(image2NaturalWidth, '0', 'Image 2 is not displayed, only alt-text is shown')

        borderColor1 = boxes1and2[0].value_of_css_property('border-color')
        borderColor2 = boxes1and2[1].value_of_css_property("border-color")
        self.assertEqual(borderColor1, 'rgb(143, 222, 151)', 'Div box 1 does not have a green border')
        self.assertEqual(borderColor2, 'rgb(143, 222, 151)', 'Div box 1 does not have a green border')

    def testLinksFromOverviewPage(self):
        """Test if the links from the negative environmental impacts page leads to a working page.

        """
        self.driver.get(os.environ["siteUnderTest"] + "/pages/environmentalIntegrityNegativ")
        impactsObj = NegativeEnvironmentalImpacts(self.driver)
