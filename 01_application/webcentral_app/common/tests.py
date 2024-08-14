from django.test import TestCase

from .test_utils.mock_objects import mock_excel_file
from .data_import import DataImport

from tools_over.models import (
    Focus, 
    Tools,
    Classification,
)
from component_list.models import (
    Category,
    Component,
    ComponentClass,
)

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
        header, data = data_import_obj.load()

        self.assertEqual(len(header), 60)

        # no header element should be doubled
        self.assertEqual(len(set(header)), 60)

        # half of the header fields should have the suffix "__en"
        foundEnglishHeaders = []
        for headerItem in header:
            if "__en" in headerItem:
                foundEnglishHeaders.append(headerItem)

        self.assertEqual(len(foundEnglishHeaders), 30)
    

    def testBuildLiteratureName(self):
        """Test the function `_buildLiteratureName`

        """
        temp_file_obj = mock_excel_file()
        data_import_obj = DataImport(temp_file_obj.name)
        
        dummyLitStr = "Althaus, Philipp, Florian Redder, Eziama Ubachukwu, Maximilian Mork, André Xhonneux und Dirk Müller (2022)"
        litLinkName = data_import_obj._buildLiteratureIdentifier(dummyLitStr)

        self.assertEqual(litLinkName, "Althaus,_Philipp,_Florian_2024")

    def testImportOfEnglishTranslationForTools(self):
        """

        """
        temp_file_obj = mock_excel_file()

        dataImportObj = DataImport(temp_file_obj.name)

        header = ["shortDescription", "shortDescription__en", "focus", "focus__en", "classification", "classification__en"]
        data = ["Dies ist ein Test", "This is a test", "betrieblich, rechtlich", "operational, legal", "Werkzeug, Digitale Anwendung", "Tool, digital application"]

        focusOperational = Focus.objects.get_or_create(focus="betrieblich")[0]
        focusLegal = Focus.objects.get_or_create(focus="rechtlich")[0]

        classificationObjOne = Classification.objects.get_or_create(
            classification="Werkzeug",
        )[0]
        classificationObjTwo = Classification.objects.get_or_create(
            classification="Digitale Anwendung",
        )[0]


        toolObj = Tools.objects.get_or_create(
            name="TestTool",
            shortDescription="Dies ist ein Test",

        )[0]

        toolObj.focus.add(focusOperational)
        toolObj.focus.add(focusLegal)

        toolObj.classification.add(classificationObjOne)
        toolObj.classification.add(classificationObjTwo)
        
        toolAfterEdit = dataImportObj._importEnglishManyToManyRel(toolObj, header, data, "focus")
        toolAfterEdit = dataImportObj._importEnglishManyToManyRel(toolAfterEdit, header, data, "classification")
 
        toolOperationalAfterEdit = toolAfterEdit.focus.get(focus="betrieblich")
        self.assertEqual(toolOperationalAfterEdit.focus_en, "operational", "Focus operational object should include the english translation")

        toolOperationalAfterEdit = toolAfterEdit.focus.get(focus="rechtlich")
        self.assertEqual(toolOperationalAfterEdit.focus_en, "legal", "Focus legal object should include the english translation")

        classificationOneAfterEdit = toolAfterEdit.classification.get(classification="Werkzeug")
        self.assertEqual(classificationOneAfterEdit.classification_en, "Tool", "Classification Tool object should include the english translation")

        toolOperationalAfterEdit = toolObj.classification.get(classification="Digitale Anwendung")
        self.assertEqual(toolOperationalAfterEdit.classification_en, "digital application", "classification digital application object should include the english translation")


        # test if import of classification works:

        # test import of regular attribute:
        toolObj = dataImportObj._importEnglishAttr(toolObj, header, data, "shortDescription")
        self.assertEqual(toolObj.shortDescription_en, data[header.index("shortDescription__en")])

    
    def testForeignKeyEnglishTranslationImport(self):
        """

        """
        temp_file_obj = mock_excel_file()
        dataImportObj = DataImport(temp_file_obj.name)
        
        header = ["Kategorie", "Kategorie__en", "Komponente", "Komponente__en"]
        data = ["TestKategorie", "Test category", "Testkomponente", "Test component"]

        # create a component obj with the german contnent:
        categoryObj = Category.objects.get_or_create(
            category=data[header.index("Kategorie")],
        )[0]
        componentClassObj = ComponentClass.objects.get_or_create(
            componentClass=data[header.index("Komponente")],
        )[0]
        componentObj = Component.objects.get_or_create(
            category=categoryObj,
            component=componentClassObj,
        )[0]
        componentClassField = Component._meta.get_field("component")
        categoryField = Component._meta.get_field("category")

        componentObjReturned = dataImportObj._importEnglishForeignKeyRel(componentObj, header, data, "Komponente", "component")
        componentObjReturned = dataImportObj._importEnglishForeignKeyRel(componentObj, header, data, "Kategorie", "category")

        self.assertEqaul(componentObjReturned.category.category_en, data[header.index("Kategorie__en")])
        self.assertEqaul(componentObjReturned.componentClass.componentClass_en, data[header.index("Komponente__en")])


