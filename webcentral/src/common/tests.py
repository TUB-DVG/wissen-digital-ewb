from django.test import TestCase

from .test_utils.mock_objects import mock_excel_file
from .data_import import DataImport

from tools_over.models import (
    Focus,
    Tools,
    Classification,
    ApplicationArea,
)
from component_list.models import (
    Category,
    Component,
    ComponentClass,
)
from project_listing.models import Subproject


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

    def testCSVdataImport(self):
        """Test if the load-data emthod of `common.data_import` returns
        headers and data rows as lists.

        """
        enargusCSVdataFile = (
            "../doc/01_data/01_pre_pro/enargus_csv_20240606.csv"
        )
        dataImportObj = DataImport(enargusCSVdataFile)

        header, data = dataImportObj.load()

        self.assertEqual(len(header), 30)
        self.assertEqual(len(data[0]), 30)
        self.assertEqual(len(data), 2068)

    def testBuildLiteratureName(self):
        """Test the function `_buildLiteratureName`"""
        temp_file_obj = mock_excel_file()
        data_import_obj = DataImport(temp_file_obj.name)

        dummyLitStr = "Althaus, Philipp, Florian Redder, Eziama Ubachukwu, Maximilian Mork, André Xhonneux und Dirk Müller (2022)"
        litLinkName = data_import_obj._buildLiteratureIdentifier(dummyLitStr)

        self.assertEqual(litLinkName, "Althaus,_Philipp,_Florian_2022")

    def testImportSpecificApplications(self):
        """Test if a Subproject object is created from a reference number string and holds the right reference number string."""
        dataImportObj = DataImport("test.csv")

        header = [
            "specificApplication",
        ]
        data = ["03EGB0021H;;03EN3018A"]

        processedSpecificApplicationList = dataImportObj._processListInput(
            data[header.index("specificApplication")], separator=";;"
        )
        specificApplicationList = dataImportObj._iterateThroughListOfStrings(
            processedSpecificApplicationList, Subproject
        )
        allSubprojects = Subproject.objects.all()
        self.assertEqual(len(allSubprojects), 2)

        listOfSubprojectIds = data[header.index("specificApplication")].split(
            ";;"
        )
        for referenceIdStr in listOfSubprojectIds:
            self.assertEqual(
                len(
                    Subproject.objects.filter(referenceNumber_id=referenceIdStr)
                ),
                1,
            )

    def testImportOfEnglishTranslationForTools(self):
        """ """
        temp_file_obj = mock_excel_file()

        dataImportObj = DataImport(temp_file_obj.name)

        header = [
            "description",
            "description__en",
            "focus",
            "focus__en",
            "classification",
            "classification__en",
        ]
        data = [
            "Dies ist ein Test",
            "This is a test",
            "betrieblich;;rechtlich",
            "operational;;legal",
            "Werkzeug;;Digitale Anwendung",
            "Tool;;digital application",
        ]

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
            description="Dies ist ein Test",
        )[0]

        toolObj.focus.add(focusOperational)
        toolObj.focus.add(focusLegal)

        toolObj.classification.add(classificationObjOne)
        toolObj.classification.add(classificationObjTwo)

        toolAfterEdit = dataImportObj._importEnglishManyToManyRel(
            toolObj, header, data, "focus", "focus"
        )
        toolAfterEdit = dataImportObj._importEnglishManyToManyRel(
            toolAfterEdit, header, data, "classification", "classification"
        )

        toolOperationalAfterEdit = toolAfterEdit.focus.get(focus="betrieblich")
        self.assertEqual(
            toolOperationalAfterEdit.focus_en,
            "operational",
            "Focus operational object should include the english translation",
        )

        toolOperationalAfterEdit = toolAfterEdit.focus.get(focus="rechtlich")
        self.assertEqual(
            toolOperationalAfterEdit.focus_en,
            "legal",
            "Focus legal object should include the english translation",
        )

        classificationOneAfterEdit = toolAfterEdit.classification.get(
            classification="Werkzeug"
        )
        self.assertEqual(
            classificationOneAfterEdit.classification_en,
            "Tool",
            "Classification Tool object should include the english translation",
        )

        toolOperationalAfterEdit = toolObj.classification.get(
            classification="Digitale Anwendung"
        )
        self.assertEqual(
            toolOperationalAfterEdit.classification_en,
            "digital application",
            "classification digital application object should include the english translation",
        )

        # test if import of classification works:

        # test import of regular attribute:
        toolObj = dataImportObj._importEnglishAttr(
            toolObj, header, data, "description", "description"
        )
        self.assertEqual(
            toolObj.description_en,
            data[header.index("description__en")],
        )

    def testGetMany2ManyElements(self):
        """Test `getM2MelementsQueryset` returns a list of objects, which corresponds to `listOfStrings` for the provided `djangoModel`"""

        temp_file_obj = mock_excel_file()

        dataImportObj = DataImport(temp_file_obj.name)

        # check if 2 Focus objects are created, when calling the method:
        listOfStringsOne = [
            "technisch",
            "betrieblich",
        ]

        returnedQueryset = dataImportObj.getM2MelementsQueryset(
            listOfStringsOne, Focus
        )
        self.assertEqual(len(returnedQueryset), 2)
        self.assertTrue(
            returnedQueryset[0].focus_de == "technisch"
            or returnedQueryset[0].focus_de == "betrieblich"
        )
        self.assertTrue(
            returnedQueryset[1].focus_de == "technisch"
            or returnedQueryset[1].focus_de == "betrieblich"
        )

        # one of the elements is already present in the database the other is not
        listOfStringsTwo = [
            "technisch",
            "ökologisch",
        ]
        returnedQueryset = dataImportObj.getM2MelementsQueryset(
            listOfStringsTwo, Focus
        )
        self.assertEqual(len(returnedQueryset), 2)
        self.assertTrue(
            returnedQueryset[0].focus_de == "technisch"
            or returnedQueryset[0].focus_de == "ökologisch"
        )
        self.assertTrue(
            returnedQueryset[1].focus_de == "technisch"
            or returnedQueryset[1].focus_de == "ökologisch"
        )

        listOfAppArea = [
            "Gebäude",
            "Sprache",
            "Forschung",
        ]
        returnedQueryset = dataImportObj.getM2MelementsQueryset(
            listOfAppArea, ApplicationArea
        )
        self.assertEqual(len(returnedQueryset), 3)

        stringOfM2Mobj = [obj.applicationArea_de for obj in returnedQueryset]
        self.assertEqual(set(listOfAppArea), set(stringOfM2Mobj))

        listOfSpecificApplications = [
            "03EWR020N",
            "03EWR0201",
        ]
        returnedQueryset = dataImportObj.getM2MelementsQueryset(
            listOfSpecificApplications, Subproject
        )
        self.assertEqual(len(returnedQueryset), 2)

    def testForeignKeyEnglishTranslationImport(self):
        """ """
        temp_file_obj = mock_excel_file()
        dataImportObj = DataImport(temp_file_obj.name)

        header = [
            "Kategorie",
            "Kategorie__en",
            "Komponente",
            "Komponente__en",
            "Beschreibung",
            "Beschreibung__en",
        ]
        data = [
            "TestKategorie",
            "Test category",
            "Testkomponente",
            "Test component",
            "Dies ist eine Beschreibung.",
            "This is a description.",
        ]

        # create a component obj with the german contnent:
        categoryObj = Category.objects.get_or_create(
            category=data[header.index("Kategorie")],
        )[0]
        componentClassObj = ComponentClass.objects.get_or_create(
            componentClass=data[header.index("Komponente")],
        )[0]
        componentObj = Component.objects.get_or_create(
            category=categoryObj,
            componentClass=componentClassObj,
        )[0]
        componentObjReturned = dataImportObj._importEnglishForeignKeyRel(
            componentObj, header, data, "Komponente", "componentClass"
        )
        componentObjReturned = dataImportObj._importEnglishForeignKeyRel(
            componentObj, header, data, "Kategorie", "category"
        )

        self.assertEqual(
            componentObjReturned.category.category_en,
            data[header.index("Kategorie__en")],
        )
        self.assertEqual(
            componentObjReturned.componentClass.componentClass_en,
            data[header.index("Komponente__en")],
        )

        componentObjReturned = dataImportObj._importEnglishAttr(
            componentObjReturned, header, data, "Beschreibung", "description"
        )
        self.assertEqual(
            componentObjReturned.description_en,
            data[header.index("Beschreibung__en")],
        )
