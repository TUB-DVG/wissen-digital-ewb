
"""The following module aims to provide a system-test of the navbar page component.
This test should ensure the correct functionality of the navigation bar.

"""
import os

from src.test_base.webdriver_setup import WebDriverSetup
from src.page_obj.pages.navbar import NavBar 

class TestNavbar(WebDriverSetup):
    """This class holds tests for the Navbar.

    """
    
    TRANSLATION_DICT_OF_PAGE_TITLE = {
        "technical": {
            "en": [
                "Overview of digital tools",
                "Overview of digital applications",
                "Overview of technical standards",
                "Overview of weatherdata services",
                "Overview of the load profile generator",   
                "Overview of datasets",
            ],
            "de": [
                "Überblick über digitale Werkzeuge",
                "Überblick über digitale Anwendungen",
                "Überblick über technische Standards",
                "Überblick über Wetterdaten-Dienste",
                "Überblick über den Lastprofilgenerator",
                "Überblick über Datensätze",
            ],

        },
        "operational": {
            "en": [
                "Business models – good practice",
                "User integration",
            ],
            "de": [
                "Geschäftsmodelle – good-practice",
                "Nutzendenintegration",
            ],
        },
        "ecological": {
            "en": [
                "Negative environmental impacts",
                "Positive environmental impacts",
            ],
            "de": [
                "Negative Umweltwirkungen",
                "Positive Umweltwirkungen",
            ],
        },
        "legal": {
            "de": [
                "Datenschutzübersicht",   
                "Kriterienkatalog - Übersicht",
                "Icons und Visualisierung",
            ],
            "en": [
                "Privacy Overview",
                "Catalog of criteria",
                "Icons and visualization",
            ],
        },
        "global": {
            "de": [
                "Überblick über die Use Cases",
                "Überblick über die Publikationen",
            ],
            "en": [
                "Overview of use cases",
                "Overview of publications",
            ],
        }


    }


    def testIfLinksInNavbarWork(self):
        """Test if the elements in the navbar redirect to the right pages.

        This test goes to all focuses and clicks all links in each dropdown focus navigation bar.
        The browser is then redirected to the page. The expected page title is then compared to the
        present page title. The expected page titles are stored in a nested dictionary `TRANSLATION_DICT_OF_PAGE_TITLE`,
        which holds the german and the english page title categorized by focus name.

        """
        self.driver.get(os.environ["siteUnderTest"])

        self.navbarObj = NavBar(self.driver)
        focuses = [
            "technical",
            "operational",
            "ecological",
            "legal",
            "global",
        ]
        for focus in focuses:
            self._checkFocus(focus)


    def _checkFocus(self, focusName: str):
        """Check the technical-focus navbar-item.

        """
        focusDopdownLink = self.navbarObj.getDropdownOfType(focusName)
        
        focusLinkElements = self.navbarObj.getDropdownLiElements(focusName)

        translationDict = self.TRANSLATION_DICT_OF_PAGE_TITLE[focusName]

        for indexItem, focusLink in enumerate(focusLinkElements):
            focusDopdownLink = self.navbarObj.getDropdownOfType(focusName)
            focusDopdownLink.click()
        
            focusLinkElements = self.navbarObj.getDropdownLiElements(focusName)
            self.item = focusLinkElements[indexItem]
            self.checkInGermanAndEnglish(self._checkNavBarElement, {"en": translationDict["en"][indexItem], "de": translationDict["de"][indexItem]})      
    def _checkNavBarElement(self, expectedValue):
        """

        """

        self.scrollElementIntoViewAndClickIt(self.item)
        self.assertEqual(expectedValue, self.driver.title)
