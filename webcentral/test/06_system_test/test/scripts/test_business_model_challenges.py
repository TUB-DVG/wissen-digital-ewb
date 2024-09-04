import sys

sys.path.append(sys.path[0] + "/...")

import time
import os
import random

from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.BusinessModels import BusinessModels


class TestBusinessModelChallenges(WebDriverSetup):
    def testStructureOfPage(self):
        """ """
        self.driver.get(
            os.environ["siteUnderTest"] + "/businessModels/challenges/"
        )  # first test if a heading and a introduction text is present:

        self._setLanguageToGerman()
        self.assertEqual(self.driver.title, "Geschäftsmodelle – Herausforderungen")

        self._setLanguageToEnglish()
        self.assertEqual(self.driver.title, "Business models - Challenges")
        self.checkNavBar("operational")
