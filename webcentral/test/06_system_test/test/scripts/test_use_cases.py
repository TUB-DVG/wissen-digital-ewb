import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.BusinessModels import BusinessModels


class TestUseCases(WebDriverSetup):
    def testStructureOfPage(self):
        """ """
        self.driver.get(
            os.environ["siteUnderTest"] + "/useCases_list/"
        )  # first test if a heading and a introduction text is present:

        self._setLanguageToGerman()
        self.assertEqual(self.driver.title, "Überblick über die Use Cases")

        self._setLanguageToEnglish()
        self.assertEqual(self.driver.title, "Overview of use cases")
        self.checkNavBar("global")
