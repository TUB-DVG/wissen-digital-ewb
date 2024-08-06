from random import choice

from django.test import TestCase
from django.core.management import call_command

from .models import EnvironmentalImpact

class DataImportTest(TestCase):
    """This class collects all test methods, which test the data import of 
    positive environmental impact data.
    """

    def testImportOfGermanAndEnglishVersion(self):
        """Test if german and english version of the positive environmental data are imported

        In general it should be possible to import the german structured datasets and its
        english translation from one excel file. The excel file has the 2 sheets `German`
        and `English`.
        The data is imported into an empty database, so no collision with existing data can occur.
        """
        
        call_command("data_import", "positive_environmental_impact", "../../02_work_doc/01_daten/16_positive_environmental_impact/Vorlage_Datenmodel_environmentalImpact_08204.xlsx", ".")

        environmnetalImpactObjects = EnvironmentalImpact.objects.all()
        self.assertGreaterEqual(len(environmnetalImpactObjects), 3, "There should be 3 or 4 positive environmental impact objects")
        
        # check if the english translation is present of a environmnetalImpactObject:
        randomEnvImpactObj = choice(environmnetalImpactObjects)
        self.assertTrue(hasattr(randomEnvImpactObj, "category_en"))
        self.assertTrue(hasattr(randomEnvImpactObj, "category_de"))
        # self.assertTrue(hasattr(randomEnvImpactObj, "literature__de"))
        # self.assertTrue(hasattr(randomEnvImpactObj, "literature__en"))
        



