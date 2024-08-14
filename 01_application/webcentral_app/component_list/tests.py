from django.test import TestCase
from django.core.management import call_command

from .models import (
    Category,   
    Component,
    ComponentClass,
)

from component_list.data_import import DataImportApp

# Create your tests here.
class TestRounding(TestCase):
    """This testclass tests the rounding functionality when 
    FloatFields are displayed.

    """
    def testFindLastDecimalPlaces(self):
        """

        """
        categoryObj = Category.objects.create(
            category="testCategory",
        )
        
        componentClassObj = ComponentClass.objects.create(
            componentClass="TestComponentClass",
        )

        exampleFloatOne = 1.00020
        componentObj = Component.objects.create(
            category=categoryObj,
            componentClass=componentClassObj,
        )

        returnValueFloatOne = componentObj._findLastDecimalPlaces(str(exampleFloatOne))
        self.assertEqual(returnValueFloatOne, 5)
    
        exampleFloatTwo = 1.00021
        returnValueFloatTwo = componentObj._findLastDecimalPlaces(str(exampleFloatTwo))
        self.assertEqual(returnValueFloatTwo, 5)

        exampleFloatThree = 1.8396
        returnValueFloatThree = componentObj._findLastDecimalPlaces(str(exampleFloatThree))
        self.assertEqual(returnValueFloatThree, 2)

        exampleFloatFour = 10
        returnValueFloatFour = componentObj._findLastDecimalPlaces(str(exampleFloatFour))
        self.assertEqual(returnValueFloatFour, 0)

class TestDataImport(TestCase):
    """Class to test the data-import of a component-list-excel-file.
    
    """
    def testImportWholeExcel(self):
        """Integration test to check if the excel file holding the
        production data can be imported.

        """
        
        call_command("data_import", "component_list", "../../02_work_doc/01_daten/12_component_list/componentList_oneSheet.xlsx", ".")

        importedComponents = Component.objects.all()
        self.assertGreaterEqual(len(importedComponents), 44, "After import of the production-data file, there should be at least 44 Components in the database.")
        
        # check if the english translations were also imported:
        sensorComponents = Component.objects.filter(category__category_de="Sensorik")
        self.assertGreaterEqual(len(sensorComponents), 9)

        componentListDataImport = DataImportApp("../../02_work_doc/01_daten/12_component_list/componentList_oneSheet.xlsx")
        
        header, data = componentListDataImport.load() 

        self.assertEqual(sensorComponents[0].category.category_en, "Sensor Technology")
        for row in data:
            self.assertGreaterEqual(len(Component.objects.filter(description_en=row[header.index("Beschreibung__en")])), 1)
            self.assertGreaterEqual(len(Component.objects.filter(furtherInformationNotes_en=row[header.index("Weitere Informationen / Anmerkungen__en")])), 1)

