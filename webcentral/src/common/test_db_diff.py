"""Test the workflow to solve conflicts in data_import 
"""

from random import choice

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.core.management import call_command

from project_listing.models import (
    Address,
    Enargus,
    ExecutingEntity,
    FurtherFundingInformation,
    # GrantRecipient,
    RAndDPlanningCategory,
    Subproject,
    Person,
    # ModuleAssignment,
)

from project_listing.data_import import DataImportApp
from .models import DbDiff
from .admin import DbDiffAdmin
from .data_import import DataImport

User = get_user_model()


class DbDiffAdminTest(TestCase):
    """Definition of testclass to test if the db conflicts can be solved
    in the django admin panel.

    """

    def setUp(self):
        """setUp method for all methods of `DbDiffAdminTest`"""
        # Create test data

        self.site = AdminSite()
        self.dbDiffAdmin = DbDiffAdmin(DbDiff, self.site)

        # Create a test user and request factory
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.factory = RequestFactory()

    def testOneTableDiffStr(self):
        """test if the finalization process works if only one table if only
        one table is in the DbDiff object.

        """
        # Create a mock request
        request = self.factory.post("/admin/common/dbdiff/")
        request.user = self.user

        _ = FurtherFundingInformation.objects.create(
            furtherFundingInformation_id=1,
            fundedBy="BMWK",
            projectManagementAgency="PTJ",
            researchProgram="EnergieWEndeBauen",
            fundingProgram="Test-Project",
        )
        fundingObj2 = FurtherFundingInformation.objects.create(
            furtherFundingInformation_id=2,
            fundedBy="BundXYZ",
            projectManagementAgency="Projektträger Jülich",
            researchProgram="Klima und Energie",
            fundingProgram="Erneuerbare Energien Programm",
        )

        _ = Enargus.objects.create(
            startDate="2014-01-01",
            endDate="2024-12-31",
            topics="Hallo",
            projectLead=None,
            furtherFundingInformation=fundingObj2,
            rAndDPlanningCategory=None,
            grantRecipient=None,
            executingEntity=None,
            collaborativeProject="Kluser",
            appropriatedBudget="1000",
            shortDescriptionDe="Description",
            shortDescriptionEn="Description2",
            database="Database",
        )

        self.dbDiff1 = DbDiff.objects.create(
            identifier="12345",
            diffStr="""<class 'project_listing.models.FurtherFundingInformation
            '>:
   furtherFundingInformation_id: 1 -> 2
   fundedBy: BMWK -> BundXYZ
   projectManagementAgency: PTJ -> Projektträger Jülich
   researchProgram: EnergieWEndeBauen -> Klima und Energie
   fundingProgram: Test-Project -> Erneuerbare Energien Programm""",
        )

        # Simulate selecting books and calling the action
        queryset = DbDiff.objects.all()
        self.dbDiffAdmin.finalizeChange(request, queryset)

        fundingObjs = FurtherFundingInformation.objects.all()
        self.assertEqual(len(fundingObjs), 1)

    def testMultipleTablesInDiffStr(self):
        """Test if the `finalizeChanges` action works, if the diffStr
        contains multiple tables.

        """
        request = self.factory.post("/admin/common/dbdiff/")
        request.user = self.user

        _ = FurtherFundingInformation.objects.create(
            furtherFundingInformation_id=1,
            fundedBy="BMWK",
            projectManagementAgency="PTJ",
            researchProgram="EnergieWEndeBauen",
            fundingProgram="Test-Project",
        )
        fundingObj2 = FurtherFundingInformation.objects.create(
            furtherFundingInformation_id=2,
            fundedBy="BundXYZ",
            projectManagementAgency="Projektträger Jülich",
            researchProgram="Klima und Energie",
            fundingProgram="Erneuerbare Energien Programm",
        )

        self.dbDiff1 = DbDiff.objects.create(
            identifier="12345",
            diffStr="""<class 'project_listing.models.Address'>:
   address_id: 2 -> 4
   plz: 10123 -> 53113
   location: Berlin -> Bonn
   address: Müller-Breslau-Str. 11 -> Godesberger Allee 90
<class 'project_listing.models.ExecutingEntity'>:
   executingEntity_id: 1 -> 2
   name: CDE Gmbh -> Energie Institut
   address: 2 -> 4
<class 'project_listing.models.RAndDPlanningCategory'>:
   rAndDPlanningCategoryNumber: 1265 -> EN-20
   rAndDPlanningCategoryText: Qlter Text -> Erneuerbare Energieentwicklung
<class 'project_listing.models.Person'>:
   person_id: 1 -> 2
   surname: Meier -> Müller
   firstName: Peter -> Johann
   title:  -> Dr.
   email: m.meier@berlin.de -> johann.mueller@example.com
<class 'project_listing.models.FurtherFundingInformation'>:
   furtherFundingInformation_id: 1 -> 2
   fundedBy: BMWK -> BundXYZ
   projectManagementAgency: PTJ -> Projektträger Jülich
   researchProgram: EnergieWEndeBauen -> Klima und Energie
   fundingProgram: Test-Project -> Erneuerbare Energien Programm
        """,
        )
        oldAdress = Address.objects.create(
            address_id=2,
            plz="10123",
            location="Berlin",
            state="Deutschland",
            address="Müller-Breslau-Str. 11",
        )
        newAdress = Address.objects.create(
            address_id=4,
            plz="53113",
            location="Bonn",
            state="Deutschland",
            address="Godesberger Allee 90",
        )

        _ = ExecutingEntity.objects.create(
            executingEntity_id=1,
            name="CDE Gmbh",
            address=oldAdress,
        )
        newExecutingEntityObjNew = ExecutingEntity.objects.create(
            executingEntity_id=2,
            name="Energie Institut",
            address=newAdress,
        )

        _, _ = Person.objects.get_or_create(
            person_id=1,
            surname="Meier",
            firstName="Peter",
            title="",
            email="m.meier@berlin.de",
        )
        _, _ = Person.objects.get_or_create(
            person_id=2,
            surname="Müller",
            firstName="Johann",
            title="",
            email="johann.mueller@example.com",
        )
        _ = RAndDPlanningCategory.objects.create(
            rAndDPlanningCategoryNumber="1265",
            rAndDPlanningCategoryText="Qlter Text",
        )

        rAnDObjNew = RAndDPlanningCategory.objects.create(
            rAndDPlanningCategoryNumber="EN-20",
            rAndDPlanningCategoryText="Erneuerbare Energieentwicklung",
        )

        _ = Enargus.objects.create(
            startDate="2014-01-01",
            endDate="2024-12-31",
            topics="Hallo",
            projectLead=None,
            furtherFundingInformation=fundingObj2,
            rAndDPlanningCategory=rAnDObjNew,
            grantRecipient=None,
            executingEntity=newExecutingEntityObjNew,
            collaborativeProject="Kluser",
            appropriatedBudget="1000",
            shortDescriptionDe="Description",
            shortDescriptionEn="Description2",
            database="Database",
        )

        queryset = DbDiff.objects.all()
        self.dbDiffAdmin.finalizeChange(request, queryset)

        fundingObjs = FurtherFundingInformation.objects.all()
        self.assertEqual(len(fundingObjs), 1)

        rAndDObjects = RAndDPlanningCategory.objects.all()
        self.assertEqual(len(rAndDObjects), 1)

        executingEntities = ExecutingEntity.objects.all()
        self.assertEqual(len(executingEntities), 1)

        personObjs = Person.objects.all()
        self.assertEqual(len(personObjs), 1)

    def testFinalizeChangesWithGetOrCreateCall(self):
        """Integration test for finalization step"""
        request = self.factory.post("/admin/common/dbdiff/")
        request.user = self.user

        header = [
            "FKZ",
            "Laufzeitbeginn",
            "Laufzeitende",
            "Thema",
            "Verbundbezeichung",
            "Foerdersumme_EUR",
            "Kurzbeschreibung_de",
            "Kurzbeschreibung_en",
            "Datenbank",
            "Bundesministerium",
            "Projekttraeger",
            "Foerderprogramm",
            "Forschungsprogramm",
            "Name_pl",
            "Vorname_pl",
            "Titel_pl",
            "Email_pl",
            "Leistungsplan_Sys_Text",
            "Leistungsplan_Sys_Nr",
            "PLZ_AS",
            "Ort_AS",
            "Land_AS",
            "Adress_AS",
            "Name_AS",
            "PLZ_ZWE",
            "Ort_ZWE",
            "Land_ZWE",
            "Adress_ZWE",
            "Name_ZWE",
        ]

        row = [
            "03EWR002A",
            "2024-01-01",  # Laufzeitbeginn
            "2025-12-31",  # Laufzeitende
            "Renewable Energy Research",  # Thema
            "Energy for Future",  # Verbundbezeichung
            "5000000",  # Foerdersumme_EUR
            "Forschung zur Optimierung erneuerbarer Energiequellen.",
            "Research on optimizing renewable energy sources.",
            "ForschungDB",  # Datenbank
            "BundXYZ",  # Bundesministerium
            "Projektträger Jülich",  # Projekttraeger
            "Erneuerbare Energien Programm",  # Foerderprogramm
            "Klima und Energie",  # Forschungsprogramm
            "Müller",  # Name_pl
            "Johann",  # Vorname_pl
            "Dr.",  # Titel_pl
            "johann.mueller@example.com",  # Email_pl
            "Erneuerbare Energieentwicklung",  # Leistungsplan_Sys_Text
            "EN-20",  # Leistungsplan_Sys_Nr
            "53113",  # PLZ_AS
            "Bonn",  # Ort_AS
            "Deutschland",  # Land_AS
            "Godesberger Allee 90",  # Adress_AS
            "Energie Institut",  # Name_AS
            "10777",
            "Berlin",
            "Deutschland",
            "FasanenStr. 13",
            "Max Muster",
        ]

        row2 = [
            "03EWR002A",
            "2024-01-02",  # Laufzeitbeginn
            "2025-11-30",  # Laufzeitende
            "Renewable Energy",  # Thema
            "Energy for Future",  # Verbundbezeichung
            "5000000",  # Foerdersumme_EUR
            "Forschung zur Optimierung erneuerbarer Energiequellen.",
            "Research on optimizing renewable energy sources.",
            "ForschungDB",  # Datenbank
            "Hallo",  # Bundesministerium
            "Projektträger Jülich2",  # Projekttraeger
            "Erneuerbare Energien Programm",  # Foerderprogramm
            "Klima und Energie",  # Forschungsprogramm
            "Müller",  # Name_pl
            "Johannes",  # Vorname_pl
            "Dr.",  # Titel_pl
            "johann.mueller@example1.com",  # Email_pl
            "Erneuerbare Energieentwicklung",  # Leistungsplan_Sys_Text
            "EN-20",  # Leistungsplan_Sys_Nr
            "53113",  # PLZ_AS
            "Bonn",  # Ort_AS
            "Deutschland",  # Land_AS
            "Godesberger Allee 91",  # Adress_AS
            "Energie Institut",  # Name_AS
            "10777",
            "Berlin",
            "Deutschland",
            "FasanenStr. 12",
            "Max Muster",
        ]

        data = [row, row2]
        importObj = DataImportApp("dummy.csv")
        enargusDataOne, _ = importObj.getOrCreate(row, header, data)

        subprojectForReferenceNumber = Subproject.objects.get(
            referenceNumber_id=row[header.index("FKZ")]
        )
        self.assertEqual(
            subprojectForReferenceNumber.enargusData, enargusDataOne
        )

        enargusDataTwo, _ = importObj.getOrCreate(row2, header, data)
        subprojectForReferenceNumber = Subproject.objects.get(
            referenceNumber_id=row[header.index("FKZ")]
        )
        self.assertEqual(
            subprojectForReferenceNumber.enargusData, enargusDataTwo
        )

    def testForAllEnargusData(self):
        """Import 2 snapshots of the enargus data and execute the
        dbDiffs afterwards.

        """

        call_command(
            "data_import",
            "project_listing",
            "../../02_work_doc/01_daten/01_prePro/enargus_csv_20230403.csv",
        )

        call_command(
            "data_import",
            "project_listing",
            "../../02_work_doc/01_daten/01_prePro/enargus_csv_20240606.csv",
        )

        request = self.factory.post("/admin/common/dbdiff/")
        request.user = self.user

        dbDiffs = DbDiff.objects.all()
        self.dbDiffAdmin.finalizeChange(request, dbDiffs)

        # import the enargus dataset, and check a random row:
        dataImportObj = DataImport(
            "../../02_work_doc/01_daten/01_prePro/enargus_csv_20240606.csv"
        )
        header, data = dataImportObj.load()

        randomRow = choice(data)
        correspondingSubproject = Subproject.objects.get(
            referenceNumber_id=randomRow[header.index("FKZ")]
        )
        enargusDataObj = correspondingSubproject.enargusData

        self.assertEqual(
            randomRow[header.index("Laufzeitbeginn")],
            str(enargusDataObj.startDate),
        )
        self.assertEqual(
            randomRow[header.index("Laufzeitende")], str(enargusDataObj.endDate)
        )
        self.assertEqual(
            randomRow[header.index("Thema")], enargusDataObj.topics
        )
        self.assertEqual(
            randomRow[header.index("Verbundbezeichung")],
            enargusDataObj.collaborativeProject,
        )
        self.assertEqual(
            randomRow[header.index("Kurzbeschreibung_de")],
            enargusDataObj.shortDescriptionDe,
        )
        self.assertEqual(
            randomRow[header.index("Kurzbeschreibung_en")],
            enargusDataObj.shortDescriptionEn,
        )
        self.assertEqual(
            randomRow[header.index("Datenbank")], enargusDataObj.database
        )
        self.assertEqual(
            randomRow[header.index("Foerdersumme_EUR")],
            str(enargusDataObj.appropriatedBudget),
        )

        personObj = enargusDataObj.projectLead
        self.assertEqual(randomRow[header.index("Name_pl")], personObj.surname)
        self.assertEqual(
            randomRow[header.index("Vorname_pl")], personObj.firstName
        )
        self.assertEqual(randomRow[header.index("Titel_pl")], personObj.title)
        self.assertEqual(randomRow[header.index("Email_pl")], personObj.email)

        furtherFundingInformationObj = enargusDataObj.furtherFundingInformation
        self.assertEqual(
            randomRow[header.index("Bundesministerium")],
            furtherFundingInformationObj.fundedBy,
        )
        self.assertEqual(
            randomRow[header.index("Projekttraeger")],
            furtherFundingInformationObj.projectManagementAgency,
        )
        self.assertEqual(
            randomRow[header.index("Foerderprogramm")],
            furtherFundingInformationObj.fundingProgram,
        )
        self.assertEqual(
            randomRow[header.index("Forschungsprogramm")],
            furtherFundingInformationObj.researchProgram,
        )

        rAndDObj = enargusDataObj.rAndDPlanningCategory
        self.assertEqual(
            randomRow[header.index("Leistungsplan_Sys_Nr")],
            rAndDObj.rAndDPlanningCategoryNumber,
        )
        self.assertEqual(
            randomRow[header.index("Leistungsplan_Sys_Text")],
            rAndDObj.rAndDPlanningCategoryText,
        )

        grantRecipientObj = enargusDataObj.grantRecipient
        self.assertEqual(
            randomRow[header.index("Name_ZWE")], grantRecipientObj.name
        )
        self.assertEqual(
            randomRow[header.index("PLZ_ZWE")], grantRecipientObj.address.plz
        )
        self.assertEqual(
            randomRow[header.index("Ort_ZWE")],
            grantRecipientObj.address.location,
        )
        self.assertEqual(
            randomRow[header.index("Land_ZWE")], grantRecipientObj.address.state
        )
        self.assertEqual(
            randomRow[header.index("Adress_ZWE")],
            grantRecipientObj.address.address,
        )

        newNumberOfEnargusObj = len(Enargus.objects.all())

        self.assertLessEqual(newNumberOfEnargusObj, 2100)
