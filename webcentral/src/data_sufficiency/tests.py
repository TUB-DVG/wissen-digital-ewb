from random import choice

from django.test import TestCase
from django.core.management import call_command

from .models import DataSufficiency


class TestDataSufficiencyDataImport(TestCase):
    """ """

    def testExcelDataImport(self):
        """Test if the import of the data file works
        as expected.

        """

        call_command(
            "data_import",
            "data_sufficiency",
            "../../02_work_doc/01_daten/13_data_sufficiency/20240613_Datenmodel_DataSufficiency.xlsx",
            ".",
        )
        self.assertEqual(
            len(DataSufficiency.objects.all()),
            4,
            "4 objects should have been imported.",
        )

        randomDataSufficiencyObj = choice(DataSufficiency.objects.all())
        attributes = [
            "example1Heading",
            "example2Heading",
            "literature",
        ]
        for attribute in attributes:
            self.assertTrue(hasattr(randomDataSufficiencyObj, attribute))
