from io import StringIO
import os

from django.db import models
from django.test import TestCase
from unittest.mock import patch
from django.core.management import (
    call_command,
    CommandError,
)
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory
import pandas as pd

from common.test_utils.mock_objects import mock_excel_file
from common.test_update import AbstractTestUpdate
from common.models import DbDiff, License
from .data_export import DataExport
from .data_import import DataImportApp
from .models import Tools, Focus, History
from .admin import HistoryAdminApp

User = get_user_model()


class TestToolsDataImport(TestCase):
    """ """

    def addM2MThroughExcel(self):
        """ """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/test_data/test_data_testing_update_wufi.xlsx",
        )

        # test if a new focus object ("kulturell", "cultural") was imported
        self.assertGreater(len(Focus.objects.filter(focus_de="kulturell")), 0)

    def testNewToolsExcelWithTranslation(self):
        """import the new tools excel file from May 2024, which also has a sheet "English" with the english translations.
        Check if the german and the english version is imported.

        """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )

        # test if the english translation was imported:
        technicalFocus = Focus.objects.get(focus_en="technical")
        firstTool = Tools.objects.filter(name="MasterSim")[0]
        self.assertEqual(len(firstTool.applicationArea.all()), 3)
        for applicationAreaObj in firstTool.applicationArea.all():
            self.assertTrue(applicationAreaObj.applicationArea_en is not None)

        allFields = Tools._meta.get_fields()
        allTools = Tools.objects.all()
        for tool in allTools:
            for field in allFields:
                if isinstance(field, models.ManyToManyField):
                    allM2Mobjs = getattr(tool, field.name).all()
                    for m2mObj in allM2Mobjs:
                        fieldsInM2Mtable = m2mObj._meta.get_fields()
                        for m2mField in fieldsInM2Mtable:
                            if "_de" in m2mField.name or "_en" in m2mField.name:
                                self.assertTrue(
                                    getattr(m2mObj, m2mField.name) != None
                                    or getattr(m2mObj, m2mField.name) != ""
                                )

        self.assertEqual(
            len(
                Tools.objects.filter(
                    name__icontains="nPro",
                    focus=technicalFocus,
                )
            ),
            1,
        )

        self.assertGreater(len(License.objects.all()), 32)

    def testImportOfNewToolsTable(self):
        """Test the import of the new tools table, espacially `lastUpdate`-attribute"""
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )
        geoTool = Tools.objects.get(name="GEO-HANDlight")
        self.assertEqual(geoTool.lastUpdate_de, "2024-10-17 00:00:00")
        self.assertEqual(
            Tools.objects.get(name="MonKey").lastUpdate_de, "unbekannt"
        )
        self.assertEqual(
            Tools.objects.get(name="MonKey").lastUpdate_en, "unknown"
        )

    def test_import_of_english_translation(self):
        # create test-data
        file_obj_excel = mock_excel_file()
        self.dataImportApp = DataImportApp(file_obj_excel.name)

        header, data = self.dataImportApp.load()
        self.dataImportApp.importList(header, data)

        imported_tools_obj = Tools.objects.get(
            name=data[0][header.index("name")]
        )
        # check if the english translation was imported:
        # self.assertEqual(imported_tools_obj.name_en, data[0][header.index("name__en")])

        self.assertEqual(
            imported_tools_obj.description_en,
            data[0][header.index("description__en")],
        )
        self.assertEqual(
            imported_tools_obj.userInterfaceNotes_en,
            data[0][header.index("userInterfaceNotes__en")],
        )
        self.assertEqual(
            imported_tools_obj.lastUpdate_en,
            data[0][header.index("lastUpdate__en")],
        )
        self.assertEqual(
            imported_tools_obj.furtherInformation_en,
            data[0][header.index("furtherInformation__en")],
        )
        self.assertEqual(
            imported_tools_obj.provider_en,
            data[0][header.index("provider__en")],
        )
        self.assertEqual(
            str(imported_tools_obj.yearOfRelease_en),
            str(data[0][header.index("yearOfRelease__en")]),
        )

        manyToManyAttrList = [
            "classification",
            "applicationArea",
            "focus",
            "targetGroup",
            "usage",
            "userInterface",
            "accessibility",
            "scale",
        ]

        for manyToManyAttr in manyToManyAttrList:
            self._checkManyToManyRel(
                imported_tools_obj, data, header, manyToManyAttr
            )

    def _checkManyToManyRel(
        self, importedToolsObj, data, header, attributeName
    ):
        """Holds the checking logic fo ManyToManyRelation translation checking."""

        listOfClassificationObj = getattr(importedToolsObj, attributeName).all()
        processedClassificationListEn = self.dataImportApp._processListInput(
            data[0][header.index(f"{attributeName}__en")], separator=";;"
        )
        processedClassificationList = self.dataImportApp._processListInput(
            data[0][header.index(attributeName)], separator=";;"
        )
        self._searchinManyToManyRelation(
            listOfClassificationObj,
            processedClassificationList,
            processedClassificationListEn,
            attributeName,
        )

    def _searchinManyToManyRelation(
        self,
        manyToManyElements,
        listOfExpectedElements,
        listOfExpectedTranslations,
        attributeNameStr,
    ):
        """Compare if all expected values are matches with all present elements in a ManyToMany-relation"""
        for expectedIndex, expectedGermanElement in enumerate(
            listOfExpectedElements
        ):
            for manyToManyElement in manyToManyElements:

                if expectedGermanElement in getattr(
                    manyToManyElement, f"{attributeNameStr}_de"
                ):
                    self.assertEqual(
                        listOfExpectedTranslations[expectedIndex],
                        getattr(manyToManyElement, f"{attributeNameStr}_en"),
                        f"English translation for {attributeNameStr} is not {listOfExpectedTranslations[expectedIndex]}",
                    )

    def testLastUpdateProcessing(self):
        """Test if the processing of `lastUpdate`-field works"""
        file_obj_excel = mock_excel_file()
        dataImportApp = DataImportApp(file_obj_excel.name)

        self.assertEqual(dataImportApp._processDate("2024-11-15"), "2024-11-15")
        self.assertEqual(
            dataImportApp._processDate(" 2024-11-15"), "2024-11-15"
        )
        self.assertEqual(dataImportApp._processDate("2024.11.15"), "2024-11-15")
        self.assertEqual(
            dataImportApp._processDate(" 2024.11.15"), "2024-11-15"
        )
        self.assertEqual(
            dataImportApp._processDate("'2024-11-15"), "2024-11-15"
        )

        self.assertEqual(
            dataImportApp._processDate("'2024.11.15"), "2024-11-15"
        )
        self.assertEqual(dataImportApp._processDate("laufend"), "laufend")
        self.assertEqual(dataImportApp._processDate("unbekannt"), "unbekannt")


class TestExportClass(TestCase):
    """Test the `DataExport` class inside tools_over.data_export module."""

    def testSortIntoGermanEnglishDS(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )

        # test if the english translation was imported:
        wufiToolsQS = Tools.objects.filter(name__icontains="Wufi")
        self.assertEqual(len(wufiToolsQS), 1)
        self.assertEqual(
            wufiToolsQS[0].description_en,
            "WUFI (Wärme Und Feuchte Instationär) is a software family for the realistic transient calculation of heat and moisture transport in multi-layer components and buildings under natural climatic conditions.",
        )

        exportObj = DataExport("hi")
        bimTools = Tools.objects.filter(name__icontains="nPro")

        germanData, englishData = exportObj._sortObjectsIntoGermanAndEnglishDs(
            bimTools
        )
        self.assertTrue(
            set(germanData.keys()),
            set(
                (
                    "name",
                    "resources",
                    "description",
                    "applicationArea",
                    "provider",
                    "usage",
                    "lifeCyclePhase",
                    "targetGroup",
                    "userInterface",
                    "userInterfaceNotes",
                    "programmingLanguages",
                    "frameworksLibraries",
                    "databaseSystem",
                    "classification",
                    "focus",
                    "scale",
                    "lastUpdate",
                    "accessibility",
                    "license",
                    "licenseNotes",
                    "furtherInformation",
                    "alternatives",
                    "specificApplication",
                    "released",
                    "releasedPlanned",
                    "yearOfRelease",
                    "developmentState",
                    "technicalStandardsNorms",
                    "technicalStandardsProtocols",
                    "image",
                )
            ),
        )

        self.assertTrue(
            set(englishData.keys()),
            set(
                (
                    "name",
                    "resources",
                    "description",
                    "applicationArea",
                    "provider",
                    "usage",
                    "lifeCyclePhase",
                    "targetGroup",
                    "userInterface",
                    "userInterfaceNotes",
                    "programmingLanguages",
                    "frameworksLibraries",
                    "databaseSystem",
                    "classification",
                    "focus",
                    "scale",
                    "lastUpdate",
                    "accessibility",
                    "license",
                    "licenseNotes",
                    "furtherInformation",
                    "alternatives",
                    "specificApplication",
                    "released",
                    "releasedPlanned",
                    "yearOfRelease",
                    "developmentState",
                    "technicalStandardsNorms",
                    "technicalStandardsProtocols",
                    "image",
                )
            ),
        )

        exportObjTwo = DataExport("testTools.xlsx")
        exportObjTwo.exportToXlsx()

        self.assertTrue(os.path.exists("testTools.xlsx"))
        os.remove("testTools.xlsx")


class TestUpdate(AbstractTestUpdate):
    """Testclass for the update process of data for the `tools_over`-app."""

    # def setUpAdmin(self):
    #     """setUp method for all methods of `DbDiffAdminTest`"""
    #
    #     self.site = AdminSite()
    #     self.historyAdmin = HistoryAdminApp(History, self.site)
    #
    #     # Create a test user and request factory
    #     self.user = User.objects.create_superuser(
    #         username="admin", password="password", email="admin@example.com"
    #     )
    #     self.factory = RequestFactory()
    historyAdminAppCls = HistoryAdminApp
    historyModelCls = History

    def testUpdateOfNewDataWorks(self):
        """Load the full tools list and update it with the full tool list, which
        has one differing tool. Check if only one History object is created.

        """
        # call_command(
        #     "data_import",
        #     "project_listing",
        #
        # )

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )

        self.assertGreater(len(Tools.objects.all()), 100)

        idOfWufiTool = Tools.objects.get(name__icontains="Wufi").id

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/test_data/test_data_full_tool_list.xlsx",
        )

        # one History object should be present:
        historyObjs = History.objects.all()
        self.assertEqual(len(historyObjs), 1)

        wufiTool = Tools.objects.filter(name__icontains="Wufi")

        self.assertEqual(len(wufiTool), 1)
        self.assertTrue("Hallo" in wufiTool[0].description_de)
        self.assertTrue("Hello" in wufiTool[0].description_en)

    def testUpdateWithSameData(self):
        """Loading the same data 2 times should create no History objects"""
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/tools_with_weatherdata.xlsx",
        )

        numberOfTools = len(Tools.objects.all())

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )

        self.assertEqual(len(History.objects.all()), 0)
        self.assertEqual(numberOfTools, len(Tools.objects.all()))

    def testUpdateM2M(self):
        """Test if it is pssible to update a Many2Many-Relation."""

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_12_tools_with_weatherdata.xlsx",
        )

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/test_data/test_data_m2m_update.xlsx",
        )

        cSharp = Tools.objects.get(name__icontains="C#")

        self.assertEqual(
            len(
                Tools.objects.filter(
                    name__icontains="C#",
                    applicationArea__applicationArea_de="Test-Kategorie",
                )
            ),
            1,
        )
        self.assertEqual(len(History.objects.all()), 1)

        request = self.factory.post("/admin/tools_over/history/")
        request.user = self.user

        # execute the History object rollback

        self.historyAdmin.rollbackHistory(request, History.objects.all())
        cSharp = Tools.objects.get(name__icontains="C#")
        self.assertEqual(len(cSharp.applicationArea.all()), 2)
