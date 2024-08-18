import importlib
import os

from django.test import TestCase
import pandas as pd

from .translator import Translator

class TestTranslator(TestCase):
    """

    """

    def setUp(self):
        """Setup method, is called before every testcase.
        
        """
        self.translator = Translator("test_excel.xlsx")

    def testTranslate(self):
        """

        """
        
        header = ["ueberschrift", "ueberschrift__en"]
        row = ["Dies ist eine Überschrift", ""]
        mapping = {
            "ueberschrift__en": "name_en",
        }

        returnedRow = self.translator._translate(header, row, mapping)
        self.assertTrue(returnedRow[header.index("ueberschrift__en")] != "")
       
    def testProcessTranslation(self):
        """Test of the `processTranslation`-method

        """
        header = [
            "name",
            "ueberschrift",
            "ueberschrift__en",
            "text",
            "text__en",
        ]
        data = [
            ["Thema 1", "Dies ist eine Überschrift", "", "In diesem Abschnitt wird etwas erklärt", ""],
            ["Thema 2", "Dies ist die zweite Überschrift", "", "Noch eine Erklärung", ""],
        ]
        mapping = {
            "ueberschrift__en": "heading_en",
            "text__en": "text_en",
        }

        dataTranslated = self.translator.processTranslation(header, data, mapping)

        self.assertEqual(len(dataTranslated), 2)
        self.assertEqual(len(dataTranslated[0]), 5)
        breakpoint()
        self.assertTrue(dataTranslated[header.index("ueberschrift__en")] != "")
        self.assertTrue(dataTranslated[header.index("text__en")] != "")
        
        self.translator._writeToExcel("testExcelFile.xlsx", header, dataTranslated, mapping)
        
        excelDict = pd.read_excel("testExcelFile.xlsx", sheet_name=None)
        self.assertEqual(set(excelDict.keys()), set(["German", "English"]))

        # the german sheet should only contain one column "ueberschrift"
        germanDF = excelDict["German"]
        self.assertEqual(len(germanDF.columns), 4)
        self.assertTrue("ueberschrift" in germanDF.columns)
        self.assertTrue("name" in germanDF.columns)
        self.assertTrue("text" in germanDF.columns)

        self.assertEqual(len(germanDF), 2) 

        englishDF = excelDict["English"]
        self.assertEqual(len(englishDF.columns), 3)
        self.assertTrue("ueberschrift" in englishDF.columns)
        self.assertTrue("text" in englishDF.columns)
        self.assertEqual(len(germanDF), 2) 

        os.system("rm -f testExcelFile.xlsx")
    
    def testWriteToExcel(self):
        """Test if _writeToExcel works as expected

        """
        
        header = [
            "ueberschrift",
            "ueberschrift__en",
        ]
        data = [
            ["Überschrift 1", "heading 1"],
            ["Überschrift 2", "heading 2"],
        ]
        mapping = {
            "ueberschrift__en": "heading_en",
        }
        self.translator._writeToExcel("testExcelFile.xlsx", header, data, mapping)
        
        # open the created excel file and check if it contains 2 sheets
        excelDict = pd.read_excel("testExcelFile.xlsx", sheet_name=None)
        self.assertEqual(set(excelDict.keys()), set(["German", "English"]))

        # the german sheet should only contain one column "ueberschrift"
        germanDF = excelDict["German"]
        self.assertEqual(len(germanDF.columns), 2)
        self.assertTrue("ueberschrift" in germanDF.columns)

        englishDF = excelDict["English"]
        self.assertEqual(len(englishDF.columns), 2)
        self.assertTrue("ueberschrift" in englishDF.columns)
        
        os.system("rm -f testExcelFile.xlsx") 
