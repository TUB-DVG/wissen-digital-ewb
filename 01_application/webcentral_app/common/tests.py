from django.test import TestCase

from .test_utils.mock_objects import mock_excel_file
from .data_import import DataImport
class TestDataImport(TestCase):
    """Test the Base `DataImport`-Class, which provides general
    functionality for the app specific data-import classes.

    """

    def test_read_excel(self):
        """Test the read-excel function. Check if multiple sheets are 
        recocgnized and if german and english versions are concatenated.

        """
        
        temp_file_obj = mock_excel_file()

        data_import_obj = DataImport(temp_file_obj.name)

        # the returned table should have the english values concatenated

