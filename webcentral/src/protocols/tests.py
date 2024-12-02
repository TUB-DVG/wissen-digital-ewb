from django.test import TestCase
from django.core.management import call_command

from common.models import License
from common.test_update import AbstractTestUpdate
from .models import Protocol, History
from .data_import import DataImportApp
from .admin import HistoryAdminApp


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


class TestUpdate(AbstractTestUpdate):
    """Class to group together all the tests for the update process."""

    historyAdminAppCls = HistoryAdminApp
    historyModelCls = History

    def test2TimesSameData(self):
        """Test if loading 2 times the same data produces sideeffects like:
        - dublicated protocol items
        - History items

        """
        call_command(
            "data_import",
            "protocols",
            "../doc/01_data/18_protocols/protocols_with_license.xlsx",
        )
        call_command(
            "data_import",
            "protocols",
            "../doc/01_data/18_protocols/protocols_with_license.xlsx",
        )
        self.assertEqual(len(History.objects.all()), 0)
        self._checkElementsUnique()

    def testUpdateoneProtocol(self):
        """Test if a protocol item is updated, if a test excel file is loaded containing the new data.
        Furthermore test if a history objects is created and if a rollback is possible.
        """
        call_command(
            "data_import",
            "protocols",
            "../doc/01_data/18_protocols/protocols_with_license.xlsx",
        )
        call_command(
            "data_import",
            "protocols",
            "../doc/01_data/18_protocols/test_data/test_update_dali.xlsx",
        )
        self._checkElementsUnique()

        allObjs = History.objects.all()
        self.assertEqual(len(allObjs), 1)

        # check if the Dali protocol is updated to the data in ``test_update_dali.xlsx
        daliObj = Protocol.objects.get(name="DALI")
        self.assertEqual(
            daliObj.communicationMediumCategory_de,
            "Verkabelt, Drahtlos & getestet",
        )
        # test if the old state of the protocol can be restored
        request = self.factory.post("/admin/protocols/history/")
        request.user = self.user
        self.historyAdmin.rollbackHistory(request, History.objects.all())
        daliObj = Protocol.objects.get(name="DALI")
        self.assertEqual(
            daliObj.communicationMediumCategory_de, "Verkabelt & Drahtlos"
        )

    def _checkElementsUnique(self):
        """Check if each protocol is only represented one time."""
        allProtocols = Protocol.objects.all()
        for protocol in allProtocols:
            searchForDuplicate = Protocol.objects.filter(name=protocol.name)
            self.assertEqual(len(searchForDuplicate), 1)
