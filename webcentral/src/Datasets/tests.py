import os

from django.test import TestCase
from django.core.management import (
    call_command,
)
import pandas as pd

from .models import Dataset


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
        
        classificationObjForDatasets = Classification.objects.get(classification_de__icontains="Gebäudegrundrisse")
        
        self.assertGreater(len(Dataset.objects.filter(classification=classificationObjForDatasets)), 0)

        solverBenchmarkDataset = Dataset.objects.get(
            name__icontains="Solver-Benchmark"
        )
        self.assertTrue(
            solverBenchmarkDataset.includesNonResidential_de
            == "Benchmark für lineare Solver."
        )
        self.assertTrue(
            solverBenchmarkDataset.includesNonResidential_en
            == "Benchmark for linear solvers."
        )


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
