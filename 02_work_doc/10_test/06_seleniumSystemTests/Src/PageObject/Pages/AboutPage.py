from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator


class AboutPage(object):
    """Class, which represents the About-Page-FrontEnd."""

    def __init__(self, driver):
        """Constructor of AboutPage"""
        self.driver = driver

    def getTopHeading(self):
        """Returns the h1-heading of the about page."""
        return self.driver.find_element(By.XPATH, Locator.aboutPageTopHeading)

    def getSubHeading(self):
        """Returns the Sub-Heading below the top heading."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageSubHeading,
        )

    def getEWBImage(self):
        """Returns the EWB-Image"""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageEWBImage,
        )

    def getEinsteinCenterLink(self):
        """Returns the Einstein-Center Link."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageEinsteinCenterLink,
        )

    def getUDKLink(self):
        """Returns the Einstein-Center Link."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageUDKLink,
        )

    def getIOeWLink(self):
        """Returns Link to UDK-Desciption Site"""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageLinkToIOeW,
        )

    def getImgOfEinsteinCenter(self):
        """Returns the Image of the Einstein-Center."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageImgOfEinsteinCenter,
        )

    def getImgOfTUBerlin(self):
        """Returns the Image of the TU-Berlin."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageImgOfTUBerlin,
        )

    def getImgOfUDK(self):
        """Returns the Image of the UDK."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageImgOfUDK,
        )

    def getImgOfIOEW(self):
        """Returns the Image of the IOEW."""
        return self.driver.find_element(
            By.XPATH,
            Locator.aboutPageImgOfIOEW,
        )
