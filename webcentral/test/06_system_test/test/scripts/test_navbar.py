"""The following module aims to provide a system-test of the navbar page component.
This test should ensure the correct functionality of the navigation bar.

"""

import os

from src.test_base.webdriver_setup import WebDriverSetup
from src.page_obj.pages.navbar import NavBar


class TestNavbar(WebDriverSetup):
    """This class holds tests for the Navbar."""

    TRANSLATION_DICT_OF_PAGE_TITLE = {
        "technical": {
            "en": [
                "Overview of digital tools",
                "Overview of digital applications",
                "Overview of technical standards",
                "Overview of weather data services",
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
                "Data sufficiency",
            ],
            "de": [
                "Negative Umweltwirkungen",
                "Positive Umweltwirkungen",
                "Datensuffizenz",
            ],
        },
        "legal": {
            "de": [
                "Kriterienkatalog - Übersicht",
                "Datenschutzübersicht",
                "Icons und Visualisierung",
            ],
            "en": [
                "Catalog of criteria - Overview",
                "Privacy Overview",
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
        },
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
            self.focus = focus
            self._checkFocus(focus)

    # def testLegalNavbar(self):
    #     """This method is moved from `TestMainPage`, maybe it can be extended
    #     to test all navbar focus elements.
    #
    #     """
    #     self.driver.get(os.environ["siteUnderTest"])
    #
    #     navBarObj = NavBar(self.driver)
    #     dropDownElements = navBarObj.getDropDownElements()
    #     self.assertEqual(
    #         len(dropDownElements),
    #         5,
    #         "Number of dropdown-elements in the navbar should be 5.",
    #     )
    #     self.checkNavBar()
    #
    #     # get elements in the global navbar dropbox:
    #     liElementsOfGlobalDropdown = navBarObj.getGlobalDropdownElements()
    #     self.assertTrue(len(liElementsOfGlobalDropdown) >= 2)
    #
    #     self.checkInGermanAndEnglish(
    #         self._checkLegalNavbarCriteriaCatalog,
    #         {
    #             "de": "Kriterienkatalog",
    #             "en": "Catalog of criteria",
    #         },
    #     )
    #
    # def _checkLegalNavbarCriteriaCatalog(self, expectedValue):
    #     """
    #     check if criteria catalog is inside legal focus navbar dropdown:
    #
    #     """
    #     navBarObj = NavBar(self.driver)
    #     liElementsOfLegalFocus = navBarObj.getLegalDropdownElements()
    #     legalDopdownLink = navBarObj.getDropdownOfType("legal")
    #     legalDopdownLink.click()
    #
    #     self.assertTrue(
    #         len(liElementsOfLegalFocus) == 3,
    #         "The navbar of legal focus should contain 3 elements.",
    #     )
    #
    #     self.assertEqual(liElementsOfLegalFocus[1].text, expectedValue)
    #
    #     liElementsOfLegalFocus[1].click()
    #
    #     self.assertTrue(
    #         "Kriterienkatalog - Übersicht" == self.driver.title
    #         or "Catalog of criteria - Overview" == self.driver.title
    #     )

    def _checkFocus(self, focusName: str):
        """Check the dropdown elements of the `focusName`-focus navbar-item.

        Parameters
        ----------
        focusName: str
            name of the current focus. Possible are 'technical', 'operational', 'ecological', 'legal', 'global'

        Returns
        -------
        None

        """
        self.focusName = focusName
        focusDopdownLink = self.navbarObj.getDropdownOfType(focusName)

        self.focusLinkElements = self.navbarObj.getDropdownLiElements(focusName)

        translationDict = self.TRANSLATION_DICT_OF_PAGE_TITLE[focusName]

        for self.indexItem, focusLink in enumerate(self.focusLinkElements):

            self.checkInGermanAndEnglish(
                self._checkNavBarElement,
                {
                    "en": translationDict["en"][self.indexItem],
                    "de": translationDict["de"][self.indexItem],
                },
            )

    def _checkNavBarElement(self, expectedValue):
        """ """
        focusDopdownLink = self.navbarObj.getDropdownOfType(self.focusName)
        focusDopdownLink.click()

        self.focusLinkElements = self.navbarObj.getDropdownLiElements(
            self.focusName
        )
        self.item = self.focusLinkElements[self.indexItem]
        self.scrollElementIntoViewAndClickIt(self.item)
        self.assertEqual(expectedValue, self.driver.title)
