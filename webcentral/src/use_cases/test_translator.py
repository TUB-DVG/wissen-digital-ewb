"""test for the translator class works for use cases app.

"""

import os

from django.core.management import call_command
from django.test import TestCase
import pandas as pd

from common.translator import Translator


class TestTranslatorUseCases(TestCase):
    """Class defintion of TestTranslator"""
    
    def testStructureOfCreatedTransFile(self):
        """

        """
        call_command(
            "translate",
            "use_cases",
            "../doc/01_data/14_use_cases/test_use_cases.xlsx",
            "test_translation_use_cases.xlsx",
        )

        df = pd.read_excel("test_translation_use_cases.xlsx", sheet_name=["German", "English"])

        self.assertEqual(
            set(df["English"].columns), 
            set(
                [
                    "Item-Code",
                    "Use-Case",
                    "SRI-Zuordnung",
                    "Wirkebene",
                    "Detailgrad",
                    "Perspektive",
                    "Lfd Nr. Effekte dieser Perspektive bei dem jeweiligen Detailgrad",
                    "Wertung des Effektes",
                    "Name des Effekts",
                    "Kurzbeschreibung der Wirkung",
                    "Quelle / Hinweise",
                    "ICON"
                ]
            )
        )
        self.assertEqual(
            set(df["German"].columns), 
            set(
                [
                    "Item-Code",
                    "Use-Case",
                    "SRI-Zuordnung",
                    "Wirkebene",
                    "Detailgrad",
                    "Perspektive",
                    "Lfd Nr. Effekte dieser Perspektive bei dem jeweiligen Detailgrad",
                    "Wertung des Effektes",
                    "Name des Effekts",
                    "Kurzbeschreibung der Wirkung",
                    "Quelle / Hinweise",
                    "ICON"
                ]
            )
        )
