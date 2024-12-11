from django.test import TestCase
from django.core.management import call_command

class TestDataExport(TestCase):
    """This class wraps all tests for the `data_export` custom management command
    for the BusimessModels app.
    """
    def setUp(self):
        """Load a businessModel-excel file, so that the test database includes
        BusinessModel-objects, which can be exported to excel.

        """
        call_command(
            "data_import",
            "businessModel",
            "../doc/01_data/10_business_models/business-model-new.xlsx",
        )
    

    def testExportedExcelStructure(self):
        """Test, if the exported excel file has tje right structure. It should
        consist 2 worksheets named "German" and "English".

        """
        self.numberExpectedRowsXlsx = 5
        self.expectedColumns = [
            "challenge",
            "shortDescription",
            "property1",
            "property1Text",
            "property2",
            "property2Text",
            "property3",
            "property3Text",
            "property4",
            "property4Text",
            "property5",
            "property5Text"
            "imageIcon",
            "imageIconSelected"
        ]

        call_command(
            "data_export",
            "businessModel",
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

        
