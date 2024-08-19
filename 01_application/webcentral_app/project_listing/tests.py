from django.test import TestCase
from django.core.management import call_command


class TestImportEnargusData(TestCase):
    """This TestCase-class tests if the import of the enargus data works as expected.
    """

    def testImportEnargusCSV(self):
        """import the newest enargus-data csv-version and check the
        database afterwards

        """
        
        call_command(
            "data_import",
            "project_listing",
            "../../02_work_doc/01_daten/01_prePro/enargus_csv_20240606.csv",
            ".",
        )
        
