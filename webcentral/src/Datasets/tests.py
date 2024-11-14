import os

from django.test import TestCase
from django.core.management import (
    call_command,
)
import pandas as pd

from .models import Dataset
from tools_over.models import (
        Classification,
        ApplicationArea,
)

class TestDataImport(TestCase):
    """Class, which wraps a TestCase for the Datasets `data_import`"""

    def testImportGemanEnglish(self):
        """Test if `data_import` imports german and english version of
        Datasets

        """
        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/20230623_datasets.xlsx",
        )
        self.assertGreater(len(Dataset.objects.all()), 48)

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
            len(
                Dataset.objects.filter(
                    applicationArea=appAreaObjForDatasets
                )
            ),
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

class TestDataUpdate(TestCase):
    """

    """
    def testUpdate(self):
        """Check if update with rollback feature is implemented

        """
        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/20230623_datasets.xlsx",
        )

        call_command(
            "data_import",
            "Datasets",
            "../doc/01_data/17_datasets/test_data/update_dataset.xlsx",
        )

        self.assertEqual(len(HistoryDataset.objects.all()), 1)
        updatedDataset = Dataset.objects.get(name="Prozessorientierte Basisdaten für Umweltmanagementsysteme")

        self.assertEqual(len(updatedDataset.focus.all()), 2)
        self.assertEqual(updatedDataset.lastUpdate_de, "laufend")
        self.assertEqual(updatedDataset.lastUpdate_en, "ongoing")

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
