from django.test import TestCase
from django.core.management import call_command
import pandas as pd

from common.test_utils.abstract_test_export import AbstractTestExport  
from common.test_utils.abstract_test_import import AbstractTestImport
from .data_export import DataExport
from .data_import import DataImport  
from .models import Publication

class TestDataImport(TestCase):
    """Class to test the data import of data from excel files."""
    
    appName = "publications"
    appNameClass = Publication
    importFile = "../doc/01_data/07_publication/publictions.xlsx"   
    appSpecificImportClass = DataImport
    numberExpectedRowsXlsx = 7

    def setUp(self):
        """ """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        )      

    def testTranslationPresent(self):
        """test if the english translation is loaded into the database.
        """
        excelDf = pd.read_excel("../doc/01_data/07_publication/publictions.xlsx", sheet_name=None)
        germanDf = excelDf["German"]
        englishDf = excelDf["English"]

        allPublications = Publication.objects.all()
        
        for index, publication in enumerate(germanDf):
            publicationObj = Publication.objects.filter(title_icontains=publication["title"])
            self.assertEqual(len(publicationObj), 1)
            self.assertEqual(publicationObj[0].abstract_en, englishDf[index]["abstract"])


    def testImportFile(self):
        """Test if the sorting into the two dictionaries representanting the english
        and german table are working as expected.

        """

        allImportedObjs = self.appNameClass.objects.all()
        self.assertGreaterEqual(
            len(allImportedObjs), self.numberExpectedRowsXlsx
        ) 

class TestDataExport(AbstractTestExport):
    """Class to test the data export custom management command
    """
    
    appName = "publications"
    appNameClass = Publication
    importFile = "../doc/01_data/07_publication/publictions.xlsx"
    appSpecificExportClass = DataExport 
    numberExpectedRowsXlsx = 8
    expectedColumns = [
        'type',
        'title',
        'copyright',
        'url',
        'abstract',
    ] 
   
    def setUp(self):
        """ """
        call_command(
            "data_import",
            self.appName,
            self.importFile,
        ) 
