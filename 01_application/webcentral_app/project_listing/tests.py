from django.test import TestCase
from django.core.management import call_command
from .models import *

from .data_import import DataImportApp

class TestImportEnargusData(TestCase):
    """This TestCase-class tests if the import of the enargus data works as expected.
    """

    def testImportEnargusCSV(self):
        """import the newest enargus-data csv-version and check the
        database afterwards

        """
        
        call_command(
            "data_import",
            "project_listing",
            "../../02_work_doc/01_daten/01_prePro/enargus_csv_20240606.csv",
            ".",
        )

    def testGetOrCreateAddress(self):
        """
        
        """

        importObj = DataImportApp("hallo.csv")

        oldAdress = Address.objects.create(
            plz="10123",
            location="Berlin",
            state="Deutschland",
            address="Müller-Breslau-Str. 11",
        )

        # create a enargusObj
        oldGrantRecipientObj = GrantRecipient.objects.create(
            name="TUB DVG",
            address=oldAdress
        )
 
        header = ["PLZ_ZWE", "Ort_ZWE", "Land_ZWE", "Adress_ZWE", "Name_ZWE"]
        row = ["10777", "Berlin", "Deutschland", "FasanenStr. 13", "Max Muster", ]
        
        newAddressObj, created = importObj.getOrCreateAdress(row, header, "zwe", oldAdress)
        
        expectedDiffStr = f"{Address}:\n"
        expectedDiffStr +=  "   address_id: 1 -> 2\n"
        expectedDiffStr += "    plz: 10123 -> 10777\n"
        expectedDiffStr += "    address: Müller-Breslau-Str. 11 -> FasanenStr. 13\n"

        self.assertEqual(importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", ""))
    
    def testGetOrCreateGrantRecipient(self):
        """

        """
        importObj = DataImportApp("hallo.csv")
        header = ["PLZ_ZWE", "Ort_ZWE", "Land_ZWE", "Adress_ZWE", "Name_ZWE"]
        row = ["10777", "Berlin", "Deutschland", "FasanenStr. 13", "Max Muster", ]

        oldAdress = Address.objects.create(
            plz="10123",
            location="Berlin",
            state="Deutschland",
            address="Müller-Breslau-Str. 11",
        )

        # create a GrantRecipient-obj:
        oldGrantRecipientObj = GrantRecipient.objects.create(
            name="Maxime Muster",
            address=oldAdress,
        )

        newGrantRecipientObj, created = importObj.getOrCreateGrantRecipient(row, header, oldGrantRecipientObj)
        expectedDiffStr = f"{Address}:\n"
        expectedDiffStr +=  "   address_id: 1 -> 2\n"
        expectedDiffStr += "    plz: 10123 -> 10777\n"
        expectedDiffStr += "    address: Müller-Breslau-Str. 11 -> FasanenStr. 13\n"

       
        expectedDiffStr += f"{GrantRecipient}:\n"
        expectedDiffStr += f"grantRecipient_id: {oldGrantRecipientObj.grantRecipient_id} -> {newGrantRecipientObj.grantRecipient_id}\n"
        expectedDiffStr += f"name: {oldGrantRecipientObj.name} -> {newGrantRecipientObj.name}\n"
        expectedDiffStr += f"address: {oldGrantRecipientObj.address.address_id} -> {newGrantRecipientObj.address.address_id}\n"
        
        self.assertEqual(importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", ""))
 

        
