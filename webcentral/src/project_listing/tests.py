"""Tests for the `project_listing`-app

"""
from csv import writer
from tempfile import NamedTemporaryFile

from django.test import TestCase
from django.core.management import call_command

from common.models import DbDiff
from .models import (
    Address,
    Enargus,
    ExecutingEntity,
    FurtherFundingInformation,
    GrantRecipient,
    RAndDPlanningCategory,
    Subproject,
    Person,
    # ModuleAssignment,
)
from .data_import import DataImportApp


class TestImportEnargusData(TestCase):
    """This TestCase-class tests if the import of the enargus data works as
    expected.
    """

    def testImportEnargusCSV(self):
        """import the newest enargus-data csv-version and check the
        database afterwards

        """


        call_command(
            "data_import",
            "project_listing",
            "../doc/01_data/01_pre_pro/enargus_csv_20240606.csv",
        )
        
        personObjects = Person.objects.all()
        for personObj in personObjects:
            self.assertEqual(personObj.surname, "Schmidt")
            self.assertEqual(personObj.firstName, "Robin")
            self.assertEqual(personObj.email, "Robin.Schmidt@email.de")
            self.assertEqual(personObj.title, "")
    
    def testKeepPersonalData(self):
        """

        """

        with NamedTemporaryFile(
            mode='w+',
            newline='',
            suffix='.csv',
            delete=True) as tempCsv:
            writerObj = writer(tempCsv, delimiter=';')
            headerRow = [
                "FKZ", 
                "Laufzeitbeginn", 
                "Laufzeitende", 
                "Datenbank", 
                "Thema", 
                "Foerdersumme_EUR", 
                "Verbundbezeichung", 
                "Leistungsplan_Sys_Nr", 
                "Leistungsplan_Sys_Text", 
                "Name_ZWE", 
                "PLZ_ZWE", 
                "Ort_ZWE", 
                "Adress_ZWE", 
                "Land_ZWE", 
                "Bundesministerium", 
                "Projekttraeger", 
                "Forschungsprogramm", 
                "Foerderprogramm", 
                "Kurzbeschreibung_de", 
                "Kurzbeschreibung_en", 
                "Person_pl", 
                "Titel_pl", 
                "Vorname_pl", 
                "Name_pl", 
                "Email_pl", 
                "Name_AS", 
                "PLZ_AS", 
                "Ort_AS", 
                "Adress_AS", 
                "Land_AS",
            ]

            dataRow = [
                "03EWR002A",
                "2021-05-01",
                "2026-04-30",
                "PROFI",
                "Reallabor: DELTA – Darmstädter Energie-Labor für Technologien in der Anwendung; Teilvorhaben: Entwicklung und Erprobung von Werkzeugen zur urbanen Energiesystemoptimierung",
                12361193.0,
                "Reallabor:DELTA",
                "EA2112",
                "Regionale Versorgungskonzepte",
                "Technische Universität Darmstadt",
                "64289",
                "Darmstadt",
                "Karolinenplatz 5",
                "Hessen",
                "BMWK",
                "Forschungszentrum Jülich GmbH",
                "Energietechnologien (BMWi)",
                "Energie",
                "Das Darmstädter Energie-Labor für Technologien in der Anwendung (DELTA) agiert als Schaufenster für die urbane Energiewende zur Demonstration interagierender energieoptimierter Quartiere. Im Reallabor DELTA soll demonstriert werden, dass die technisch nachgewiesenen Potenziale zur Steigerung der Energieeffizienz und -flexibilisierung von urbanen Quartieren wirtschaftlich umsetzbar sind und diese auch gesellschaftlich akzeptiert werden. Hierfür sollen Methoden erprobt und weiterentwickelt werden, um erfolgreiche technische Pilotprojekte in die breite Anwendung zu bringen. Elementar ist hierzu die Entwicklung innovativer (kooperativer) Geschäftsmodelle, um das entstehende Energiesystem einerseits ohne Subventionen betreiben zu können und andererseits alle Stakeholder des Energiesystems an den energetischen und wirtschaftlichen Potenzialen partizipieren zu lassen. Innerhalb des Projekts wird ein mehrschichtiger, sektorenübergreifender Ansatz verfolgt. Im Fokus steht hierbei die konsequente Steigerung der Energieeffizienz aller Sektoren, welche bereits heute als größtes nutzbares Potenzial der Energiewende gesehen wird. Weiterhin sollen Potenziale zur zeitlichen Verschiebung elektrischer Lasten identifiziert und zur Optimierung des städtischen Stromsystems sowie zur optimalen Ausnutzung erneuerbarer Energiequellen eingesetzt werden. Beides wird durch eine intelligente Verknüpfung einzelner Quartiere des betrachteten städtischen Energiesystems sowie durch Sektorenkopplung erzielt. Hierfür ist die Einbindung aller relevanten Stakeholder vorgesehen, die in erprobten Dialogformaten umsetzbare Lösungen erarbeiten werden.",
                "The Darmstadt Energy Laboratory for Technologies in Application (DELTA) represents a showcase for the urban energy transition through interacting energy-optimized districts. In the LivingLab DELTA, it is to be demonstrated that the technically proven potential for increasing energy efficiency and flexibility in urban districts can be implemented economically and is also accepted by society. To achieve this, methods are to be tested and further developed in order to bring successful technical pilot projects into broad application. Elementary for this is the development of innovative (cooperative) business models in order to be able to operate the emerging energy system without subsidies on the one hand and to allow all stakeholders of the energy system to participate in the energetic and economic potentials. Within the project, a multi-layered, cross-sectoral approach is pursued. The focus is on the consistent increase in energy efficiency in all sectors, which is already seen as the greatest usable potential for the overall energy system transformation. Furthermore, potentials for shifting electrical loads over time are to be identified and used to optimise the urban electricity system and to make optimum use of renewable energy sources. Both will be achieved through intelligent linking of individual elements (districts) of the urban energy system and through sector coupling. The involvement of all relevant stakeholders is planned for this purpose, who will develop feasible solutions in proven dialogue formats. Within the LivingLab DELTA, various locations in and around Darmstadt are selected and a wide range of technological innovations are tested on a real scale. These include in particular: • The mainly climate-neutral energy supply of residential buildings with optimised use of available CO2-free electricity, heat and waste heat sources (Energy-optimised residential district, sub-project 1)",
                "Test Person",
                "",
                "Test",
                "Person",
                "Test.Person@email.de",
                "Technische Universität Darmstadt - Fachbereich Bau- und Umweltingenieurwissenschaften",
                "64287",
                "Darmstadt",
                "Franziska-Braun-Str. 3",
                "Hessen"
            ]
            writerObj.writerow(headerRow)
            writerObj.writerow(dataRow)
            # Flush the file to ensure it's written
            tempCsv.flush()
            
            # Rewind the file pointer to the beginning of the file
            tempCsv.seek(0)
            call_command(
                "data_import",
                "project_listing",
                tempCsv.name,
                "--personalData",
            )

        personObjs = Person.objects.all()
        self.assertEqual(len(personObjs), 1)
        self.assertEqual(personObjs[0].surname, "Person")
        self.assertEqual(personObjs[0].firstName, "Test")
        self.assertEqual(personObjs[0].title, "")
        self.assertEqual(personObjs[0].email, "Test.Person@email.de")


#     def testGetOrCreateAddress(self):
#         """Test if the creation of a Address object works as expected"""
#
#         importObj = DataImportApp("hallo.csv")
#
#         oldAdress = Address.objects.create(
#             plz="10123",
#             location="Berlin",
#             state="Deutschland",
#             address="Müller-Breslau-Str. 11",
#         )
#
#         # create a enargusObj
#         _ = GrantRecipient.objects.create(name="TUB DVG", address=oldAdress)
#
#         header = ["PLZ_ZWE", "Ort_ZWE", "Land_ZWE", "Adress_ZWE", "Name_ZWE"]
#         row = [
#             "10777",
#             "Berlin",
#             "Deutschland",
#             "FasanenStr. 13",
#             "Max Muster",
#         ]
#         importObj.dictIdentifier = "1"
#         importObj.diffStrDict["1"] = ""
#         _, _ = importObj.getOrCreateAdress(row, header, "zwe", oldAdress)
#
#         expectedDiffStr = f"{Address}:\n"
#         expectedDiffStr += "   address_id: 1 -> 2\n"
#         expectedDiffStr += "    plz: 10123 -> 10777\n"
#         expectedDiffStr += (
#             "    address: Müller-Breslau-Str. 11 -> FasanenStr. 13\n"
#         )
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testGetOrCreateGrantRecipient(self):
#         """Test the method getOrCreateGrantRecipient in data_import"""
#         importObj = DataImportApp("hallo.csv")
#         header = ["PLZ_ZWE", "Ort_ZWE", "Land_ZWE", "Adress_ZWE", "Name_ZWE"]
#         row = [
#             "10777",
#             "Berlin",
#             "Deutschland",
#             "FasanenStr. 13",
#             "Max Muster",
#         ]
#
#         oldAdress = Address.objects.create(
#             plz="10123",
#             location="Berlin",
#             state="Deutschland",
#             address="Müller-Breslau-Str. 11",
#         )
#
#         # create a GrantRecipient-obj:
#         oldGrantRecipientObj = GrantRecipient.objects.create(
#             name="Maxime Muster",
#             address=oldAdress,
#         )
#         importObj.dictIdentifier = "1"
#         importObj.diffStrDict["1"] = ""
#
#         newGrantRecipientObj, _ = importObj.getOrCreateGrantRecipient(
#             row, header, oldGrantRecipientObj
#         )
#         expectedDiffStr = f"{Address}:\n"
#         expectedDiffStr += "   address_id: 1 -> 2\n"
#         expectedDiffStr += "    plz: 10123 -> 10777\n"
#         expectedDiffStr += (
#             "    address: Müller-Breslau-Str. 11 -> FasanenStr. 13\n"
#         )
#
#         expectedDiffStr += f"{GrantRecipient}:\n"
#         expectedDiffStr += f"""grantRecipient_id:
#         {oldGrantRecipientObj.grantRecipient_id} ->
#          {newGrantRecipientObj.grantRecipient_id}\n"""
#         expectedDiffStr += f"""name: {oldGrantRecipientObj.name} ->
#         {newGrantRecipientObj.name}\n"""
#         expectedDiffStr += f"""address:
#         {oldGrantRecipientObj.address.address_id}->
#         {newGrantRecipientObj.address.address_id}\n"""
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testgetOrCreateExecutingEntity(self):
#         """test the method getOrCreateExecutingEntity in data_import"""
#         importObj = DataImportApp("hallo.csv")
#
#         header = ["PLZ_AS", "Ort_AS", "Land_AS", "Adress_AS", "Name_AS"]
#         row = [
#             "12345",
#             "Brandenburg",
#             "Deutschland",
#             "Mecklenburgische Str. 12a",
#             "ABC Gmbh",
#         ]
#
#         oldAdress = Address.objects.create(
#             plz="10123",
#             location="Berlin",
#             state="Deutschland",
#             address="Müller-Breslau-Str. 11",
#         )
#
#         oldExecutingEntityObj = ExecutingEntity.objects.create(
#             name="CDE Gmbh",
#             address=oldAdress,
#         )
#         importObj.dictIdentifier = "1"
#         importObj.diffStrDict["1"] = ""
#
#         newExecutingEntityObj, _ = importObj.getOrCreateExecutingEntity(
#             row, header, oldExecutingEntityObj
#         )
#         newAddress = newExecutingEntityObj.address
#         expectedDiffStr = f"{Address}:\n"
#         expectedDiffStr += f"""   address_id: {oldAdress.address_id} ->
#         {newAddress.address_id}\n"""
#         expectedDiffStr += f"    plz: {oldAdress.plz} -> {newAddress.plz}\n"
#         expectedDiffStr += (
#             f"   location: {oldAdress.location} -> {newAddress.location}\n"
#         )
#         expectedDiffStr += (
#             f"    address: {oldAdress.address} -> {newAddress.address}\n"
#         )
#
#         expectedDiffStr += f"{ExecutingEntity}:\n"
#         expectedDiffStr += f"""executingEntity_id:
#         {oldExecutingEntityObj.executingEntity_id} ->
#         {newExecutingEntityObj.executingEntity_id}\n"""
#         expectedDiffStr += f"""name: {oldExecutingEntityObj.name} ->
#         {newExecutingEntityObj.name}\n"""
#         expectedDiffStr += f"""address:
#         {oldExecutingEntityObj.address.address_id} ->
#         {newExecutingEntityObj.address.address_id}\n"""
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testGetOrCreateRAndDPlanningCategory(self):
#         """Test the method getOrCreateRAndDPlanningCategory from data_import"""
#         importObj = DataImportApp("hallo.csv")
#
#         header = ["Leistungsplan_Sys_Text", "Leistungsplan_Sys_Nr"]
#         row = ["Dies ist ein Beispieltext", "12365"]
#
#         rAnDObj = RAndDPlanningCategory.objects.create(
#             rAndDPlanningCategoryNumber="1265g",
#             rAndDPlanningCategoryText="Qlter Text",
#         )
#         importObj.dictIdentifier = "1"
#         importObj.diffStrDict["1"] = ""
#
#         newRandDObj, _ = importObj.getOrCreateRAndDPlanningCategory(
#             row, header, rAnDObj
#         )
#         expectedDiffStr = f"{RAndDPlanningCategory}:\n"
#         expectedDiffStr += f"""
#         rAndDPlanningCategoryNumber: {rAnDObj.rAndDPlanningCategoryNumber} ->
#         {newRandDObj.rAndDPlanningCategoryNumber}\n"""
#         expectedDiffStr += f"""
#         rAndDPlanningCategoryText: {rAnDObj.rAndDPlanningCategoryText} ->
#         {newRandDObj.rAndDPlanningCategoryText}\n"""
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testGetOrCreatePerson(self):
#         """Test the getOrCreatePerson method from data_import"""
#         importObj = DataImportApp("hallo.csv")
#
#         header = ["Name_pl", "Vorname_pl", "Titel_pl", "Email_pl"]
#         row = ["Müller", "Peter", "Dr Ing.", "p.mueller@tu-berlin.de"]
#
#         oldPersonObj, _ = Person.objects.get_or_create(
#             surname="Meier",
#             firstName="Peter",
#             title="",
#             email="m.meier@berlin.de",
#         )
#         importObj.dictIdentifier = "1"
#         importObj.diffStrDict["1"] = ""
#
#         newPersonObj, _ = importObj.getOrCreatePerson(row, header, oldPersonObj)
#         expectedDiffStr = f"{Person}:\n"
#         expectedDiffStr += f"""
#         person_id: {oldPersonObj.person_id} -> {newPersonObj.person_id}\n"""
#         expectedDiffStr += (
#             f"   surname: {oldPersonObj.surname} -> {newPersonObj.surname}\n"
#         )
#         expectedDiffStr += f"""
#         firstName: {oldPersonObj.firstName} -> {newPersonObj.firstName}\n"""
#         expectedDiffStr += (
#             f"   title: {oldPersonObj.title} -> {newPersonObj.title}\n"
#         )
#         expectedDiffStr += (
#             f"   email: {oldPersonObj.email} -> {newPersonObj.email}\n"
#         )
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testGetOrCreateFurtherFundingInformation(self):
#         """Test the method getOrCreateFurtherFundingInformation from
#         data_import.
#         """
#         importObj = DataImportApp("hallo.csv")
#
#         header = [
#             "Bundesministerium",
#             "Projekttraeger",
#             "Foerderprogramm",
#             "Forschungsprogramm",
#         ]
#         row = ["BMWK", "PTJ", "EWB", "New Test Project"]
#
#         oldTestObj, _ = FurtherFundingInformation.objects.get_or_create(
#             fundedBy="BMWK",
#             projectManagementAgency="PTJ",
#             researchProgram="EnergieWEndeBauen",
#             fundingProgram="Test-Project",
#         )
#         importObj.dictIdentifier = "1"
#
#         importObj.diffStrDict["1"] = ""
#
#         newFundingObj, _ = importObj.getOrCreateFurtherFundingInformation(
#             row, header, oldTestObj
#         )
#         expectedDiffStr = f"{FurtherFundingInformation}:\n"
#         expectedDiffStr += f"""
#         furtherFundingInformation_id:
#         {oldTestObj.furtherFundingInformation_id} ->
#         {newFundingObj.furtherFundingInformation_id}\n"""
#         expectedDiffStr += f"""
#         researchProgram: {oldTestObj.researchProgram} ->
#         {newFundingObj.researchProgram}\n"""
#         expectedDiffStr += f"""
#         fundingProgram: {oldTestObj.fundingProgram} ->
#         {newFundingObj.fundingProgram}\n"""
#
#         self.assertEqual(
#             importObj.diffStr.replace(" ", ""), expectedDiffStr.replace(" ", "")
#         )
#
#     def testGetOrCreate(self):
#         """Test if a difference string is created,
#         which includes all connected tables.
#         """
#         header = [
#             "FKZ",
#             "Laufzeitbeginn",
#             "Laufzeitende",
#             "Thema",
#             "Verbundbezeichung",
#             "Foerdersumme_EUR",
#             "Kurzbeschreibung_de",
#             "Kurzbeschreibung_en",
#             "Datenbank",
#             "Bundesministerium",
#             "Projekttraeger",
#             "Foerderprogramm",
#             "Forschungsprogramm",
#             "Name_pl",
#             "Vorname_pl",
#             "Titel_pl",
#             "Email_pl",
#             "Leistungsplan_Sys_Text",
#             "Leistungsplan_Sys_Nr",
#             "PLZ_AS",
#             "Ort_AS",
#             "Land_AS",
#             "Adress_AS",
#             "Name_AS",
#             "PLZ_ZWE",
#             "Ort_ZWE",
#             "Land_ZWE",
#             "Adress_ZWE",
#             "Name_ZWE",
#         ]
#
#         row = [
#             "03EWR002A",
#             "2024-01-01",  # Laufzeitbeginn
#             "2025-12-31",  # Laufzeitende
#             "Renewable Energy Research",  # Thema
#             "Energy for Future",  # Verbundbezeichung
#             "5000000",  # Foerdersumme_EUR
#             "Forschung zur Optimierung erneuerbarer Energiequellen.",
#             "Research on optimizing renewable energy sources.",
#             "ForschungDB",  # Datenbank
#             "BundXYZ",  # Bundesministerium
#             "Projektträger Jülich",  # Projekttraeger
#             "Erneuerbare Energien Programm",  # Foerderprogramm
#             "Klima und Energie",  # Forschungsprogramm
#             "Müller",  # Name_pl
#             "Johann",  # Vorname_pl
#             "Dr.",  # Titel_pl
#             "johann.mueller@example.com",  # Email_pl
#             "Erneuerbare Energieentwicklung",  # Leistungsplan_Sys_Text
#             "EN-20",  # Leistungsplan_Sys_Nr
#             "53113",  # PLZ_AS
#             "Bonn",  # Ort_AS
#             "Deutschland",  # Land_AS
#             "Godesberger Allee 90",  # Adress_AS
#             "Energie Institut",  # Name_AS
#             "10777",
#             "Berlin",
#             "Deutschland",
#             "FasanenStr. 13",
#             "Max Muster",
#         ]
#
#         importObj = DataImportApp("test.xlsx")
#
#         rAnDObj = RAndDPlanningCategory.objects.create(
#             rAndDPlanningCategoryNumber="1265",
#             rAndDPlanningCategoryText="Qlter Text",
#         )
#
#         oldFurtherFundingObj, _ = (
#             FurtherFundingInformation.objects.get_or_create(
#                 fundedBy="BMWK",
#                 projectManagementAgency="PTJ",
#                 researchProgram="EnergieWEndeBauen",
#                 fundingProgram="Test-Project",
#             )
#         )
#         oldPersonObj, _ = Person.objects.get_or_create(
#             surname="Meier",
#             firstName="Peter",
#             title="",
#             email="m.meier@berlin.de",
#         )
#         oldAdress = Address.objects.create(
#             plz="10123",
#             location="Berlin",
#             state="Deutschland",
#             address="Müller-Breslau-Str. 11",
#         )
#
#         # create a enargusObj
#         oldGrantRecipientObj = GrantRecipient.objects.create(
#             name="TUB DVG", address=oldAdress
#         )
#
#         oldAdressExecutingEntity = Address.objects.create(
#             plz="10123",
#             location="Berlin",
#             state="Deutschland",
#             address="Müller-Breslau-Str. 11",
#         )
#
#         oldExecutingEntityObj = ExecutingEntity.objects.create(
#             name="CDE Gmbh",
#             address=oldAdressExecutingEntity,
#         )
#
#         oldEnargusObj, _ = Enargus.objects.get_or_create(
#             startDate="2023-01-01",  # Laufzeitbeginn
#             endDate="2025-12-31",
#             topics="Erstellung von Tests",
#             projectLead=oldPersonObj,
#             furtherFundingInformation=oldFurtherFundingObj,
#             rAndDPlanningCategory=rAnDObj,
#             grantRecipient=oldGrantRecipientObj,
#             executingEntity=oldExecutingEntityObj,
#             collaborativeProject="Kluster",
#             appropriatedBudget="100000",
#             shortDescriptionDe="Dieses Projekt erstellt Testfälle",
#             shortDescriptionEn="This project creates testcases",
#             database="Enargus",
#         )
#
#         _ = Subproject.objects.create(
#             referenceNumber_id=row[header.index("FKZ")],
#             enargusData=oldEnargusObj,
#         )
#
#         _ = importObj.getOrCreate(row, header, [])
#         self.assertTrue(
#             "<class 'project_listing.models.Address'>" in importObj.diffStr
#         )
#         self.assertTrue(
#             "<class 'project_listing.models.ExecutingEntity'>"
#             in importObj.diffStr
#         )
#         self.assertTrue(
#             "<class 'project_listing.models.RAndDPlanningCategory'>"
#             in importObj.diffStr
#         )
#
#     def testWriteDiffStr(self):
#         """Test if a created diffStr is correctly written to the database."""
#
#         diffStr = """
# <class 'project_listing.models.Address'>:
#    address_id: 2 -> 4
#    plz: 10123 -> 53113
#    location: Berlin -> Bonn
#    address: Müller-Breslau-Str. 11 -> Godesberger Allee 90
# <class 'project_listing.models.ExecutingEntity'>:
#    executingEntity_id: 1 -> 2
#    name: CDE Gmbh -> Energie Institut
#    address: 2 -> 4
# <class 'project_listing.models.RAndDPlanningCategory'>:
#    rAndDPlanningCategoryNumber: 1265 -> EN-20
#    rAndDPlanningCategoryText: Qlter Text -> Erneuerbare Energieentwicklung
# <class 'project_listing.models.Person'>:
#    person_id: 1 -> 2
#    surname: Meier -> Müller
#    firstName: Peter -> Johann
#    title:  -> Dr.
#    email: m.meier@berlin.de -> johann.mueller@example.com
# <class 'project_listing.models.FurtherFundingInformation'>:
#    furtherFundingInformation_id: 1 -> 2
#    fundedBy: BMWK -> BundXYZ
#    projectManagementAgency: PTJ -> Projektträger Jülich
#    researchProgram: EnergieWEndeBauen -> Klima und Energie
#    fundingProgram: Test-Project -> Erneuerbare Energien Programm
# <class 'project_listing.models.Enargus'>:
#    enargus_id: 1 -> 2
#    startDate: 2023-01-01 -> 2024-01-01
#    endDate: 2025-12-31 -> 2025-12-31
#    topics: Erstellung von Tests -> Renewable Energy Research
#    collaborativeProject: Kluster -> Energy for Future
#    furtherFundingInformation: 1 -> 2
#    projectLead: 1 -> 2
#    database: Enargus -> ForschungDB
#    shortDescriptionDe: Dieses Projekt erstellt Testfälle -> 
#    Forschung zur Optimierung erneuerbarer Energiequellen.
#    shortDescriptionEn: This project creates testcases -> 
#    Research on optimizing renewable energy sources.
#    rAndDPlanningCategory: 1265 -> EN-20
#    grantRecipient: 1 -> 2
#    executingEntity: 1 -> 2
#    appropriatedBudget: 100000.00 -> 5000000.0
#         """
#
#         diffDictStr = {"12345": diffStr}
#         importObj = DataImportApp("hallo.csv")
#         importObj.diffStrDict = diffDictStr
#         importObj.diffStrDict[diffDictStr] = ""
#
#         importObj._writeDiffStrToDB()
#
#         dbDiffObjs = DbDiff.objects.all()
#         self.assertEqual(len(dbDiffObjs), 1)
#         self.assertEqual(dbDiffObjs[0].identifier, "12345")
#         self.assertTrue(dbDiffObjs[0].diffStr != "")
