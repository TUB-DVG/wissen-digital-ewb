from django.test import TestCase
from django.core.manangement import call_command
import pandas as pd

class TestDataImport(TestCase):
    """Class, which wraps a TestCase for the Datasets `data_import`

    """
    def testImportGemanEnglish(self):
        """Test if `data_import` imports german and english version of 
        Datasets
        
        """
        call_command(
            "import_data",
            "Datasets",
            "../doc/01_data/17_datasets/20230623_datasets.xlsx",
        )


class TestDataExport(TestCase):
    """Class, which wraps a TestCase for the Datasets `data_export`

    """

    def testExportGermanEnglish(self):
        """Test if a excel file with a german and english sheet are exported

        """
        
        call_command(
            "data_export",
            "Datasets",
            "test.xlsx",
        )
        
        excelFile = pd.ExcelFile("test.xlsx")
        excelSheetNames = excelFile.sheet_names
        self.assertEqual(set(excelSheetNames), set(["German", "English"]))






