from io import StringIO
import os

from django.test import TestCase
from unittest.mock import patch
from django.core.management import (
    call_command,
    CommandError,
)
import pandas as pd

from common.test_utils.mock_objects import mock_excel_file
from common.models import DbDiff
from .data_export import DataExport
from .data_import import DataImportApp
from .models import Tools, Focus, History


class TestToolsDataImport(TestCase):
    """ """

    def testNewToolsExcelWithTranslation(self):
        """import the new tools excel file from May 2024, which also has a sheet "English" with the english translations.
        Check if the german and the english version is imported.

        """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_05_EWB_tools_with_english_translation.xlsx",
        )

        # test if the english translation was imported:
        technicalFocus = Focus.objects.get(focus_en="technical")

        self.assertEqual(
            len(
                Tools.objects.filter(
                    name__icontains="nPro",
                    focus=technicalFocus,
                )
            ),
            1,
        )

    def testDuplicateImport(self):
        """Test if a DbDiff-object is created when importing a dataset for a tool, which is already present in the database."""
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_05_EWB_tools_with_english_translation.xlsx",
        )

        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/test_data/test_data_testing_update_wufi.xlsx",
        )

        self.assertEqual(len(DbDiff.objects.all()), 1)
        self.assertTrue("operational" in DbDiff.objects.all()[0].diffStr)
        self.assertTrue("betrieblich" in DbDiff.objects.all()[0].diffStr)

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
            imported_tools_obj.shortDescription_en,
            data[0][header.index("shortDescription__en")],
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
        processedClassificationListEn = self.dataImportApp._correctReadInValue(
            data[0][header.index(f"{attributeName}__en")]
        )
        processedClassificationList = self.dataImportApp._correctReadInValue(
            data[0][header.index(attributeName)]
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


class TestExportClass(TestCase):
    """Test the `DataExport` class inside tools_over.data_export module."""

    def testSortIntoGermanEnglishDS(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_05_EWB_tools_with_english_translation.xlsx",
        )

        # test if the english translation was imported:
        wufiToolsQS = Tools.objects.filter(name__icontains="Wufi")
        self.assertEqual(len(wufiToolsQS), 1)
        self.assertEqual(
            wufiToolsQS[0].shortDescription_en,
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
                    "shortDescription",
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
                    "shortDescription",
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


class TestUpdate(TestCase):
    """Testclass for the update process of data for the `tools_over`-app."""

    def testUpdateOfNewDataWorks(self):
        """Test if starting the update-process and finalizing with the updated
        dataset works.

        """
        call_command(
            "data_import",
            "tools_over",
            "../doc/01_data/02_tool_over/2024_05_EWB_tools_with_english_translation.xlsx",
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
        self.assertLessEqual(len(historyObjs), 5)
        breakpoint()
        wufiTool = Tools.objects.filter(name__icontains="Wufi")
        self.assertEqual(len(wufiTool), 1)

        cSharpTool = Tools.objects.filter(name__icontains="C#")
        self.assertEqual(len(cSharpTool), 1) 


class TestTools(TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stderr", new_callable=StringIO)
    def testCallDataImportForTools(self, mock_stderr, mock_stdout):
        """Check if data-import can be called for data of tools
        data-import-functionality.
        """
        test_tool_obj = mock_excel_file()
        call_command(
            "data_import",
            "tools_over",
            test_tool_obj.name,
            ".",
        )

        # check if the tool was imported
        # english translation should also be imported
        imported_tool = Tools.objects.get(name_de=df_german["name"])
        self.assertEqual(
            imported_tool.shortDescription_de,
            df_german["shortDescription"],
            "German version of short description is not as expected.",
        )
        self.assertEqual(
            imported_tool.shortDescription_en,
            df_english["shortDescription"],
            "English version of short description is not as expected.",
        )
