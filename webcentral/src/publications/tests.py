import os

from django.test import TestCase
from django.core.management import call_command
import pandas as pd

from .data_export import DataExport
from .data_import import DataImport
from .models import Publication, History
from common.models import Focus


class TestDataImport(TestCase):
    """Class to test the data import of data from excel files."""

    appName = "publications"
    appNameClass = Publication
    importFile = "../doc/01_data/07_publication/publications.xlsx"
    appSpecificImportClass = DataImport
    numberExpectedRowsXlsx = 7

    def setUp(self):
        """ """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        )

    def testTranslationPresent(self):
        """test if the english translation is loaded into the database."""
        excelDf = pd.read_excel(
            "../doc/01_data/07_publication/publications.xlsx", sheet_name=None
        )
        germanDf = excelDf["German"]
        englishDf = excelDf["English"]

        allPublications = Publication.objects.all()

        for index, publication in germanDf.iterrows():
            publicationObj = Publication.objects.filter(
                title__icontains=publication["title"]
            )
            self.assertEqual(len(publicationObj), 1)
            abstractExcelValue = englishDf.loc[index, "abstract"]
            if pd.isna(abstractExcelValue):
                abstractExcelValue = ""
            self.assertEqual(publicationObj[0].abstract_en, abstractExcelValue)

    def testImportFile(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """

        allImportedObjs = self.appNameClass.objects.all()
        self.assertGreaterEqual(
            len(allImportedObjs), self.numberExpectedRowsXlsx
        )


class TestDataExport(TestCase):
    """Class to test the data export custom management command"""

    appName = "publications"
    appNameClass = Publication
    importFile = "../doc/01_data/07_publication/publications.xlsx"
    appSpecificExportClass = DataExport
    numberExpectedRowsXlsx = 7
    expectedColumns = [
        "type",
        "title",
        "copyright",
        "url",
        "abstract",
        "focus",
    ]

    def setUp(self):
        """ """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        )

    def testExportFile(self):
        """ """
        call_command(
            "data_export",
            self.appName,
            "test_export.xlsx",
        )

        self.assertTrue(os.path.exists("test_export.xlsx"))

        excelFileAsDf = pd.read_excel("test_export.xlsx", sheet_name=None)
        self.assertTrue(isinstance(excelFileAsDf, dict))
        self.assertTrue(set(excelFileAsDf.keys()) == set(["German", "English"]))

        for sheet in excelFileAsDf.values():
            self.assertGreaterEqual(len(sheet), self.numberExpectedRowsXlsx)
            self.assertEqual(set(sheet.keys()), set(self.expectedColumns))

        os.remove("test_export.xlsx")


class TestDataUpdate(TestCase):
    """Test if the Update algorithm works in publications app"""

    def testUpdateOneItem(self):
        """ """
        call_command(
            "data_import",
            "publications",
            "../doc/01_data/07_publication/publications.xlsx",
        )

        call_command(
            "data_import",
            "publications",
            "../doc/01_data/07_publication/test_data/test_update_one_item.xlsx",
        )

        # number of history objects should be 1:
        historyObjs = History.objects.all()
        self.assertEqual(len(historyObjs), 1)

        # test if the changes were applied:
        changedPublicationObj = Publication.objects.filter(
            title_de="Thesen zur Digitalisierung der Energiewende in Deutschland: Status Quo und Ausblick - eine Expertinnenbefragung der deutschen Forschungslandschaft"
        )
        self.assertEqual(len(changedPublicationObj), 1)

        self.assertTrue(
            "Der vorliegende Bericht Test des Moduls"
            in changedPublicationObj[0].abstract_de
        )
        self.assertTrue(
            "The present report Test by "
            in changedPublicationObj[0].abstract_en
        )

        # test if a focus of tpe operational was added:
        self.assertEqual(len(changedPublicationObj[0].focus.all()), 2)
        operationalFocus = Focus.objects.filter(focus_de="betrieblich")
        self.assertEqual(len(operationalFocus), 1)
        self.assertEqual(operationalFocus[0].focus_en, "operational")

        self.assertEqual(len(operationalFocus[0].publication_set.all()), 1)
