import os

from django.test import TestCase
from django.core.management import (
    call_command,
)
import pandas as pd

from .models import Dataset, History
from .admin import HistoryAdminApp
from tools_over.models import (
    Classification,
    ApplicationArea,
)
from common.test_update import AbstractTestUpdate

class TestDataImport(TestCase):
    """Class, which wraps a TestCase for the Datasets `data_import`"""

    def testImportGemanEnglish(self):
        """Test if `data_import` imports german and english version of
        Datasets

        """
        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/datasets_with_weatherdata.xlsx",
        )
        self.assertGreater(len(Dataset.objects.all()), 52)

        classificationObjForDatasets = Classification.objects.get(
            classification_de__icontains="Gebäudegrundrisse"
        )
        self.assertEqual(
            classificationObjForDatasets.classification_en,
            "Building floor plans",
        )
        appAreaObjForDatasets = ApplicationArea.objects.get(
            applicationArea_de__icontains="Benchmark"
        )
        self.assertEqual(
            appAreaObjForDatasets.applicationArea_en,
            "Benchmark",
        )

        self.assertGreater(
            len(Dataset.objects.filter(applicationArea=appAreaObjForDatasets)),
            0,
        )

        solverBenchmarkDataset = Dataset.objects.get(
            name__icontains="Solver-Benchmark"
        )
        self.assertTrue(
            solverBenchmarkDataset.furtherInformation_de
            == "Benchmark für lineare Solver."
        )
        self.assertTrue(
            solverBenchmarkDataset.furtherInformation_en
            == "Benchmark for linear solvers."
        )

        weatherdataCategory = Classification.objects.filter(
            classification_de="Wetterdaten"
        )
        self.assertEqual(len(weatherdataCategory), 1)
        self.assertEqual(
            weatherdataCategory[0].classification_en, "Weather data"
        )

        datasetsWeatherdata = Dataset.objects.filter(
            classification=weatherdataCategory[0]
        )
        self.assertGreater(len(datasetsWeatherdata), 4)

        openDataDwd = Dataset.objects.get(name="Open Data DWD")
        licensesOfOpenDwd = openDataDwd.license.all()
        self.assertEqual(len(licensesOfOpenDwd), 1)
        self.assertEqual(licensesOfOpenDwd[0].license_de, "Open Data")
        self.assertEqual(licensesOfOpenDwd[0].license_en, "Open Data")

        centralEuropeRefinedWD = Dataset.objects.get(
            name="The Central Europe Refined analysis version 1 (CER v1)"
        )
        licensesOfCentralEuropeRefined = centralEuropeRefinedWD.license.all()

        self.assertEqual(len(licensesOfCentralEuropeRefined), 1)
        self.assertEqual(
            licensesOfCentralEuropeRefined[0].license_de, "Frei nutzbar"
        )
        self.assertEqual(
            licensesOfCentralEuropeRefined[0].license_en, "Free to use"
        )


class TestUpdate(AbstractTestUpdate):
    """ """
    historyAdminAppCls = HistoryAdminApp 
    historyModelCls = History
    def testUpdate(self):
        """Check if update with rollback feature is implemented"""
        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/datasets_with_weatherdata.xlsx",
        )

        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/test_data/update_dataset.xlsx",
        )

        self.assertEqual(len(History.objects.all()), 1)
        updatedDataset = Dataset.objects.get(
            name="Prozessorientierte Basisdaten für Umweltmanagementsysteme"
        )

        self.assertEqual(updatedDataset.lastUpdate_de, "laufend")
        self.assertEqual(updatedDataset.lastUpdate_en, "ongoing")

        # restore the old state of Dataset with the history object:
        request = self.factory.post("/admin/Datasets/history/")
        request.user = self.user

        # execute the History object rollback
        self.historyAdmin.rollbackHistory(request, History.objects.all())  
        updatedDataset = Dataset.objects.get(
            name="Prozessorientierte Basisdaten für Umweltmanagementsysteme"
        )
        self.assertTrue(updatedDataset.lastUpdate_de == "" or updatedDataset.lastUpdate_de == None)
        self.assertTrue(updatedDataset.lastUpdate_en == "" or updatedDataset.lastUpdate_en == None)

class TestDataExport(TestCase):
    """Class, which wraps a TestCase for the Datasets `data_export`"""

    def testExportGermanEnglish(self):
        """Test if a excel file with a german and english sheet are exported"""

        call_command(
            "data_export",
            "Datasets",
            "test.xlsx",
        )

        excelFile = pd.ExcelFile("test.xlsx")
        excelSheetNames = excelFile.sheet_names
        self.assertEqual(set(excelSheetNames), set(["German", "English"]))
