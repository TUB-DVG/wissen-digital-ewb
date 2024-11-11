from django.test import TestCase
from django.core.manangement import call_command

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




