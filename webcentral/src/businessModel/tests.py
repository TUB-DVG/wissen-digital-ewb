import os

from django.test import TestCase
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
import pandas as pd

from .models import BusinessModel, History
from .admin import HistoryAdminApp

User = get_user_model()

NUMBER_EXPECTED_BUSINESS_MODELS = 5


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
            "property5Text",
            "imageIcon",
            "imageIconSelected",
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

        for sheetName in ["German", "English"]:
            sheet = excelFileAsDf[sheetName]
            self.assertGreaterEqual(len(sheet), self.numberExpectedRowsXlsx)
            self.assertEqual(set(sheet.keys()), set(self.expectedColumns))

        os.remove("test_export.xlsx")


class TestDataImport(TestCase):
    """Class, which wraps all tests related to data import of businessModel data."""

    pathToExcel = "../doc/01_data/10_business_models/business-model-new.xlsx"

    def testDataImport(self):
        """ """

        call_command(
            "data_import",
            "businessModel",
            self.pathToExcel,
        )

        businessModelObjs = BusinessModel.objects.all()
        excelDf = pd.read_excel(self.pathToExcel, sheet_name=None)

        germanSheet = excelDf["German"]
        self.assertEqual(len(businessModelObjs), len(germanSheet))

        # check if all fields are imported:


class TestDataUpdate(TestCase):
    """Wrap the test class"""

    def setUp(self):
        """setUp method for all methods of `DbDiffAdminTest`"""

        self.site = AdminSite()
        self.historyAdmin = HistoryAdminApp(History, self.site)

        # Create a test user and request factory
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.factory = RequestFactory()

    def testSimpleUpdate(self):
        """ """
        call_command(
            "data_import",
            "businessModel",
            "../doc/01_data/10_business_models/business-model-new.xlsx",
        )

        call_command(
            "data_import",
            "businessModel",
            "../doc/01_data/10_business_models/test_data/test_data_one_item_changed.xlsx",
        )

        historyObjs = History.objects.all()
        self.assertEqual(len(historyObjs), 1)

        allBusinessModelObjs = BusinessModel.objects.all()
        self.assertEqual(
            len(allBusinessModelObjs), NUMBER_EXPECTED_BUSINESS_MODELS
        )
        updatedBusinessModelObj = BusinessModel.objects.filter(
            challenge_de="Organisatorische Faktoren"
        )
        self.assertEqual(len(updatedBusinessModelObj), 1)
        self.assertTrue(
            "Bei der Übersetzung in ein Test "
            in updatedBusinessModelObj[0].shortDescription_de
        )
        self.assertTrue(
            "Organizational barriers Test"
            in updatedBusinessModelObj[0].shortDescription_en
        )

        self._rollbackAllChanges()
        historyObjs = History.objects.all()
        self.assertEqual(len(historyObjs), 0)

        allBusinessModelObjs = BusinessModel.objects.all()
        self.assertEqual(
            len(allBusinessModelObjs), NUMBER_EXPECTED_BUSINESS_MODELS
        )
        updatedBusinessModelObj = BusinessModel.objects.filter(
            challenge_de="Organisatorische Faktoren"
        )
        self.assertEqual(len(updatedBusinessModelObj), 1)
        self.assertTrue(
            "Bei der Übersetzung in ein Geschäftsmodell"
            in updatedBusinessModelObj[0].shortDescription_de
        )
        self.assertTrue(
            "Organizational barriers sometimes arise"
            in updatedBusinessModelObj[0].shortDescription_en
        )

    def _rollbackAllChanges(self):
        """Wraps the call of the rollback into a function:"""
        request = self.factory.post("/admin/TechnicalStandards/history/")
        request.user = self.user

        self.historyAdmin.rollbackHistory(request, History.objects.all())
