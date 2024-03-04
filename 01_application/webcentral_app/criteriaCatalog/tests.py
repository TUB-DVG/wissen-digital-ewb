from django.test import TestCase
from django.core import management
from criteriaCatalog.models import (
    CriteriaCatalog,
    Topic,
)
# Create your tests here.
class AutomaticDataImport(TestCase):
    
    def testLoadExcelFile(self):
        """
        """
        # breakpoint()
        management.call_command('data_import', '../../02_work_doc/01_daten/08_criteriaCatalog/Tabelle_Wissensplattform_criteriaCatalog_Personalisierung.xlsx', "tests/data")

        self.assertEqual(CriteriaCatalog.objects.count(), 1)
        self.assertTrue(CriteriaCatalog.objects.filter(name="Profilbildung und Personalisierung").exists())

        self.assertGreater(Topic.objects.count(), 0)
        self.assertTrue(Topic.objects.filter(text="Spezifikation der Datenkategorien").parentId.id == 1)
        self.assertTrue(Topic.objects.filter(text="Personenbezug der Daten").parentId.id == None)