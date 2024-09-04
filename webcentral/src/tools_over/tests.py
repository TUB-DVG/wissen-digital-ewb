from io import StringIO

from django.test import TestCase
from unittest.mock import patch
from django.core.management import (
    call_command,
    CommandError,
)
import pandas as pd

from common.test_utils.mock_objects import mock_excel_file
from .data_import import DataImportApp
from .models import Tools


class TestToolsDataImport(TestCase):
    """ """

    def testNewToolsExcelWithTranslation(self):
        """import the new tools excel file from May 2024, which also has a sheet "English" with the english translations.
        Check if the german and the english version is imported.

        """
        call_command(
            "data_import",
            "tools_over",
            "../../02_work_doc/01_daten/02_toolUebersicht/2024_05_EWB_newToolsImportWithTranslation.xlsx",
            ".",
        )

        # check if nPro is part of the tools:
        nProTool = Tools.objects.get(name="nPro")

        # check focus and classification:
        # focusesForNPro = nProTool.classification.all()

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
                    # except:
                    #     breakpoint()
                    #


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
