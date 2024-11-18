from django.test import TestCase
from django.core.management import call_command

from common.models import License
from .models import Protocol
from .data_import import DataImportApp


class TestDataImport(TestCase):
    """Test the import of structured protocol data."""

    def testDataImportCommand(self):
        """test if the `data_import` custom management command for the protocols app includes `Protocol`-data."""
        call_command(
            "data_import",
            "protocols",
            "../doc/01_data/18_protocols/protocols_with_license.xlsx",
        )
        allProtocols = Protocol.objects.all()
        self.assertGreater(len(allProtocols), 11)

        for protocol in allProtocols:
            self.assertEqual(len(protocol.focus.all()), 1)
            self.assertEqual(protocol.focus.all()[0].focus_de, "technisch")
            self.assertEqual(protocol.focus.all()[0].focus_en, "technical")

            self.assertEqual(len(protocol.license.all()), 1)
            self.assertNotEqual(
                protocol.license.all()[0].openSourceStatus_en, None
            )
            self.assertNotEqual(
                protocol.license.all()[0].licensingFeeRequirement_en, None
            )

    def testIfLicenseObjectsAreInstanciated(self):
        """Test if `License` objects are returned from `getM2MelementsQueryset`"""
        dataImportAppObj = DataImportApp("test.xlsx")

        testStringForLicenseClass = [
            (
                None,
                "Open Source",
                "Fee Required",
                "Open Source",
                "Fee Required",
            ),
            (
                "MIT",
                "Open Source",
                "No Fee Required",
                "Open Source",
                "Fee Required",
            ),
            ("MIT", None, "No Fee Required", None, "No Fee Required"),
            ("MIT", None, None, None, None),
        ]
        returnedListOfLicenseObjs = dataImportAppObj.getM2MelementsQueryset(
            testStringForLicenseClass, License
        )
        self.assertEqual(len(returnedListOfLicenseObjs), 4)
        for index, testTuple in enumerate(testStringForLicenseClass):
            self.assertEqual(
                testTuple[0], returnedListOfLicenseObjs[index].license
            )
            self.assertEqual(
                testTuple[1], returnedListOfLicenseObjs[index].openSourceStatus
            )
            self.assertEqual(
                testTuple[2],
                returnedListOfLicenseObjs[index].licensingFeeRequirement,
            )
            self.assertEqual(
                testTuple[3],
                returnedListOfLicenseObjs[index].openSourceStatus_en,
            )
            self.assertEqual(
                testTuple[4],
                returnedListOfLicenseObjs[index].licensingFeeRequirement_en,
            )
