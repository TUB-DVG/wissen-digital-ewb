from random import choice

from django.test import TestCase
from django.core import management
from criteriaCatalog.models import (
    CriteriaCatalog,
    Topic,
)


# Create your tests here.
class AutomaticDataImport(TestCase):

    # def testLoadExcelFile(self):
    #     """
    #     """
    #     # breakpoint()
    #     management.call_command('data_import', '../../02_work_doc/01_daten/08_criteriaCatalog/Tabelle_Wissensplattform_criteriaCatalog_Personalisierung.xlsx', "tests/data")
    #
    #     self.assertEqual(CriteriaCatalog.objects.count(), 1)
    #     self.assertTrue(CriteriaCatalog.objects.filter(name="Profilbildung und Personalisierung").exists())
    #
    #     self.assertGreater(Topic.objects.count(), 0)
    #     self.assertTrue(Topic.objects.filter(text="Spezifikation der Datenkategorien").parentId.id == 1)
    #     self.assertTrue(Topic.objects.filter(text="Personenbezug der Daten").parentId.id == None)
    #
    def testLoadBetriebsoptimierung(self):
        """Test if the import of the `Betrieb and Betriebsoptimierung`-excel file
        is working as expected.
        """

        management.call_command(
            "data_import",
            "criteriaCatalog",
            "../../02_work_doc/01_daten/08_criteriaCatalog/16_07_2024_criteriaCatalog_Betriebsoptimierung.xlsx",
            "tests/data",
        )

        self.assertEqual(
            len(
                Topic.objects.filter(
                    criteriaCatalog__name__icontains="Betrieb und Betriebsoptimierung"
                )
            ),
            211,
            f"Number of topics of type Betriebsoptimierung should be 210 but is {len(Topic.objects.filter(criteriaCatalog__name__icontains='Betrieb und Betriebsoptimierung'))}",
        )
        randomTopicObject = choice(Topic.objects.all())

        try:
            randomTopicObject.__getattribute__("norms")
        except AttributeError:
            self.fail("Norms is not an attribute of Topic.")

        try:
            randomTopicObject.__getattribute__("grey")
        except AttributeError:
            self.fail("Attribute grey should be a attribute of Topic.")
