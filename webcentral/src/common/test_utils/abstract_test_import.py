from django.test import TestCase
from django.core.management import call_command
import pandas as pd


class AbstractTestImport(TestCase):
    """ """

    def setUp(self):
        """ """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        )

    def testImportFile(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """

        allImportedObjs = self.appNameClass.objects.all()
        self.assertGreaterEqual(
            len(allImportedObjs), self.numberExpectedRowsXlsx
        )
