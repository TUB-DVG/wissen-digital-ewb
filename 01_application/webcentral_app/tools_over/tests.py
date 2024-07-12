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
    """

    """
    
    def test_import_of_english_translation(self):
        #create test-data
        file_obj_excel = mock_excel_file() 
        data_import_app = DataImportApp(file_obj_excel.name)

        header, data = data_import_app.load()
        data_import_app.importList(header, data)
        
        imported_tools_obj = Tools.objects.get(name=data[0][header.index("name")])
        
        # check if the english translation was imported:
        self.assertEqual(imported_tools_obj.name_en, data[0][header.index("name_en")])



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
            imported_tool.shortDescription_de, df_german["shortDescription"], "German version of short description is not as expected."
        )
        self.assertEqual(
            imported_tool.shortDescription_en, df_english["shortDescription"], "English version of short description is not as expected."
        )



