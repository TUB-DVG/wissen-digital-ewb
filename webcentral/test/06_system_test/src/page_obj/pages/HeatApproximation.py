from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from Src.PageObject.Locators import Locator


class HeatApproximation(object):
    """ """

    def __init__(self, driver):
        """ """
        self.driver = driver

    def getHeadingOfPage(self):
        """Returns the h1-heading of the page."""
        return self.driver.find_element(
            By.XPATH,
            Locator.headingOfHeatApproxSite,
        )

    def switchToIFrame(self):
        """Switches to the Iframe in which the react app is located."""
        wait = WebDriverWait(self.driver, timeout=2)
        iframeObj = wait.until(
            EC.presence_of_element_located((By.XPATH, Locator.currentLoadIFrame))
        )

        self.driver.switch_to.frame(iframeObj)

    def getBottomParagraph(self):
        """Returns the bottom paragraph of the page."""
        return self.driver.find_element(
            By.XPATH,
            Locator.bottomParagraph,
        )
