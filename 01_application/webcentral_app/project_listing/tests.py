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
 
    def testgetOrCreateExecutingEntity(self):
        """

        """
        importObj = DataImportApp("hallo.csv")

        header = ["PLZ_AS", "Ort_AS", "Land_AS", "Adress_AS", "Name_AS"]
        row = ["12345", "Brandenburg", "Deutschland", "Mecklenburgische Str. 12a", "ABC Gmbh"]
        
        oldAdress = Address.objects.create(
            plz="10123",
            location="Berlin",
            state="Deutschland",
            address="Müller-Breslau-Str. 11",
        )
        

        oldExecutingEntityObj = ExecutingEntity.objects.create(
            name="CDE Gmbh",
            address=oldAdress,
        )
         
        newExecutingEntityObj, created = importObj.getOrCreateExecutingEntity(row, header, oldExecutingEntityObj)
        newAddress = newExecutingEntityObj.address
        expectedDiffStr = f"{Address}:\n"
        expectedDiffStr += f"   address_id: {oldAdress.address_id} -> {newAddress.address_id}\n"
        expectedDiffStr += f"    plz: {oldAdress.plz} -> {newAddress.plz}\n"
        expectedDiffStr += f"   location: {oldAdress.location} -> {newAddress.location}\n"
        expectedDiffStr += f"    address: {oldAdress.address} -> {newAddress.address}\n"

       
        expectedDiffStr += f"{ExecutingEntity}:\n"
        expectedDiffStr += f"executingEntity_id: {oldExecutingEntityObj.executingEntity_id} -> {newExecutingEntityObj.executingEntity_id}\n"
        expectedDiffStr += f"name: {oldExecutingEntityObj.name} -> {newExecutingEntityObj.name}\n"
        expectedDiffStr += f"address: {oldExecutingEntityObj.address.address_id} -> {newExecutingEntityObj.address.address_id}\n"
        
        self.assertEqual(importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", ""))

    def testGetOrCreateRAndDPlanningCategory(self):
        """

        """
        importObj = DataImportApp("hallo.csv")

        header = ["Leistungsplan_Sys_Text", "Leistungsplan_Sys_Nr"]
        row = ["Dies ist ein Beispieltext", "12365"]

        rAnDObj = RAndDPlanningCategory.objects.create(
            rAndDPlanningCategoryNumber="1265g",
            rAndDPlanningCategoryText="Qlter Text",
        )

        newRandDObj, created = importObj.getOrCreateRAndDPlanningCategory(row, header, rAnDObj)
        expectedDiffStr = f"{RAndDPlanningCategory}:\n"
        expectedDiffStr += f"   rAndDPlanningCategoryNumber: {rAnDObj.rAndDPlanningCategoryNumber} -> {newRandDObj.rAndDPlanningCategoryNumber}\n" 
        expectedDiffStr += f"   rAndDPlanningCategoryText: {rAnDObj.rAndDPlanningCategoryText} -> {newRandDObj.rAndDPlanningCategoryText}\n" 

        self.assertEqual(importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", ""))


    def testGetOrCreatePerson(self):
        """

        """
        importObj = DataImportApp("hallo.csv")

        header = ["Name_pl", "Vorname_pl", "Titel_pl", "Email_pl"]
        row = ["Müller", "Peter", "Dr Ing.", "p.mueller@tu-berlin.de"]

        oldPersonObj, created = Person.objects.get_or_create(
            surname="Meier",
            firstName="Peter",
            title="",
            email="m.meier@berlin.de",
        )

        newPersonObj, created = importObj.getOrCreatePerson(row, header, oldPersonObj)
        expectedDiffStr = f"{Person}:\n"
        expectedDiffStr += f"   person_id: {oldPersonObj.person_id} -> {newPersonObj.person_id}\n" 
        expectedDiffStr += f"   surname: {oldPersonObj.surname} -> {newPersonObj.surname}\n" 
        expectedDiffStr += f"   firstName: {oldPersonObj.firstName} -> {newPersonObj.firstName}\n" 
        expectedDiffStr += f"   title: {oldPersonObj.title} -> {newPersonObj.title}\n" 
        expectedDiffStr += f"   email: {oldPersonObj.email} -> {newPersonObj.email}\n" 

        self.assertEqual(importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", ""))

    
    def testGetOrCreateFurtherFundingInformation(self):
        """

        """
        pass
