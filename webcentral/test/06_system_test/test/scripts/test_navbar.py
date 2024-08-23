
from src.page_obj.pages.navbar import NavBar 

class TestNavbar(WebDriverSetup):
    """This class holds tests for the Navbar.

    """

    def testIfLinksInNavbarWork(self):
        """Test if the elements in the navbar redirect to the right pages.

        """

        self.navbarObj = NavBar(self.driver)


    def _checkTechnicalFocus(self):
        """Check the technical-focus navbar-item.

        """
        technicalDopdownLink = self.navbarObj.getDropdownOfType("technical")
        technicalDopdownLink.click()
        
        technicalLinkElements = self.navbarObj.getDropdownLiElements("technical")

        translationDict = {
            "en": [
                "Overview of digital tools",
                "Overview of digital applications",

            ],
            "de": [
                "Überblick über digitale Werkzeuge",
                "Überblick über digitale Anwendungen",

            ],

        }

        for technicalLink in technicalLinkElements:

        
