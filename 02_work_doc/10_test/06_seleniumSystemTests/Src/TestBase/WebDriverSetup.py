"""

"""
import time
import os
import unittest
import urllib3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Src.PageObject.Pages.cookieBanner import CookieBanner
from Src.PageObject.Pages.Footer import Footer
from Src.PageObject.Pages.NavBar import NavBar

# Create tmp_dir
temp_dir = "~/_tmp"
try:
    os.makedirs(temp_dir)
except:
    pass
os.environ["TMPDIR"] = temp_dir

class WebDriverSetup(unittest.TestCase):
    PATH_TO_TRANSLATION_FILE = "../../../01_application/webcentral_app/locale/"

    ECOLOGICAL_COLOR = "rgb(143, 171, 247)"
    GLOBAL_COLOR = "rgb(120, 117, 117)"
    TECHNICAL_COLOR = "rgb(143, 171, 247)" 
    
    def setUp(self):
        """Start a webdriver-instance for every test in headless-mode.
        The headles browser instance is a firefox-instance and has the
        dimensions 1920x1080.

        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        firefoxOptions = Firefox_Options()
        firefoxOptions.add_argument("--window-size=1920,1080")
        firefoxOptions.add_argument("start-maximised")
        # firefoxOptions.add_argument("--width=1920")
        # firefoxOptions.add_argument("--height=1080")
        if os.environ.get("HEADLESS") == "1":
            firefoxOptions.headless = True
        self.driver = webdriver.Firefox(options=firefoxOptions)
        # self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self):
        """Close the browser Window of every test."""
        if self.driver != None:
            print("Cleanup of test environment")
            self.driver.close()
            self.driver.quit()

    def scrollElementIntoView(self, element):
        """Scroll the element into the view of the browser-window."""
        window_height = self.driver.execute_script("return window.innerHeight")
        middle_y_coordinate = element.location["y"] - (window_height / 2)
        self.driver.execute_script(
            f"window.scrollTo(0, {middle_y_coordinate})")
        time.sleep(1)

    def scrollElementIntoViewAndClickIt(self, element):
        """Scroll the element into the view of the browser-window."""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.element = element
        try:
            wait = WebDriverWait(self.driver, 10)  # waits for 10 seconds
            wait.until(self._elementIsClickable)
        except:
            pass

    def _elementIsClickable(self, driver):
        """Check if the element is clickable."""
        try:
            self.element.click()
        except:
            return False
        return True

    def _checkForPageError(self, errorMessage):
        """Check if the Django-ValueError-Page or the nginx Server-Error Page appears

        errorMessage: str
          this is a string, which contains the error-message, which is displayed if the assert-statement fails
        """
        self.assertTrue(
            self.driver.title != "Server Error (500)"
            or "ValueError" not in self.driver.title,
            errorMessage,
        )

    def getLanguage(self):
        """Get the language of the page."""

        element = self.driver.find_element(By.XPATH,
                                           "//select[@name='language']")
        return element.get_attribute("value")

    def checkIfImageIsDisplayed(self, image):
        """Check if the image is displayed."""
        naturalWidth = image.get_attribute("naturalWidth")
        self.assertNotEqual(naturalWidth, "0",
                            "Image is not displayed, only alt-text is shown")

    def checkIfSvgIsDisplayed(self, svgElement):
        try:
            # Check if the SVG element is present and has child elements
            children = svgElement.find_elements(By.XPATH, "./*")
            if len(children) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def _removeCookieBanner(self):
        """Remove the cookie-banner from the page"""
        cookieBannerObj = CookieBanner(self.driver)
        cookieBannerButton = cookieBannerObj.getCookieAcceptanceButton()
        if cookieBannerButton.is_displayed():
            self.scrollElementIntoViewAndClickIt(cookieBannerButton)

    def _setLanguageToGerman(self):
        """Set the language of the page to german"""
        # change the language to german and check if the german heading is displayed
        try:
            self._removeCookieBanner()
        except:
            pass

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
        try:
            self._removeCookieBanner()
        except:
            pass

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

    def checkInGermanAndEnglish(self, funcHandler, translationsDict):
        """Execute the function `funcHandler` when language is set to german and english."""

        self._setLanguageToGerman()
        funcHandler(translationsDict["de"])

        self._setLanguageToEnglish()
        funcHandler(translationsDict["en"])

    def checkIfElementIsTranslated(self, language, elementText,
                                   translationDict):
        """Change the language of the page and check if the language is changed."""
        if language == "en":
            self._setLanguageToGerman()
            self.assertEqual(self.getLanguage(), "de")
            self.assertEqual(translationDict["de"], elementText)
        elif language == "de":
            self._setLanguageToEnglish()
            self.assertEqual(self.getLanguage(), "en")
            self.assertEqual(translationDict["en"], elementText)
        else:
            self.assertEqual(self.getLanguage(), "en")

    def checkNavBar(self, currentFocus=None):
        """test if on the current page the image icons in the navbar are only colored
        for the current focus.

        currentFocus: str
            string representing the current focus color.

        Returns:
        None
        """

        navBarObj = NavBar(self.driver)
        listOfIcons = navBarObj.getIcons()
        if currentFocus is None:
            currentFocus = "undefined"
        for icon in listOfIcons:
            self.assertTrue(icon.text == "", "No alt text should be present for icon")
            srcOfImage =  icon.get_attribute("src")
            if currentFocus in srcOfImage:
                self.assertTrue("_no.svg" not in srcOfImage)
            else:
                self.assertTrue("_no.svg" in srcOfImage)

    def checkPageTitle(self, germanTitle, englishTitle):
        """Test if the page title on the english and german version of the app is 
        as expected.

        germanTitle:    str
            The german title as a string.
        englishTitle:   str
            The english title of the page as a string.
        
        Returns:
            None
        """
        self._setLanguageToEnglish()
        self.waitUntilPageIsLoaded()
        self.assertEqual(self.driver.title, englishTitle)
        self._setLanguageToGerman()
        self.waitUntilPageIsLoaded()
        self.assertEqual(self.driver.title, germanTitle)

    def waitUntilPageIsLoaded(self, elementId=None):
        """Explicitly wait until page is loaded.

        """
        
        wait = WebDriverWait(self.driver, timeout=10)
        if elementId is None:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div")))

        else:    
            wait.until(EC.presence_of_element_located((By.ID, f'{elementId}')))
        

