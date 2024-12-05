from django.test import TestCase
from django.core.mangement import call_command
import pandas as pd


class AbstractTestExport(TestCase):
    """

    """
    def setUp(self):
        """

        """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        )

    def testExportFile(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """
        
        exportObj = self.appSpecificExportClass("hi")
        
        exportObjTwo = self.appSpecificExportClass("test_export.xlsx")
        exportObjTwo.exportToXlsx()

        self.assertTrue(os.path.exists("test_export.xlsx"))
        
        excelFileAsDf = pd.read_excel("test_export.xlsx", sheets=None)
        self.assertTrue(isinstance(excelFileAsDf, dict))
        self.assertTrue(
            set(excelFileAsDf.keys()) == set("German", "English")
        )
        
        for sheet in excelFileAsDf.values()
            self.assertGreaterEqual(len(sheet), self.numberExpectedRowsXlsx)
            self.assertEqual(set(sheet.keys()), set(self.expectedColumns))

        os.remove("test_export.xlsx")

