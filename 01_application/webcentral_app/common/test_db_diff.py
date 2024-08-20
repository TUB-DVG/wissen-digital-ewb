from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from project_listing.models import FurtherFundingInformation, Enargus
from .models import DbDiff
from .admin import DbDiffAdmin

User = get_user_model()

class DbDiffAdminTest(TestCase):
    def setUp(self):
        # Create test data
        
        self.site = AdminSite()
        self.dbDiffAdmin = DbDiffAdmin(DbDiff, self.site)

        # Create a test user and request factory
        self.user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.factory = RequestFactory()

    def testOneTableDiffStr(self):
        # Create a mock request
        request = self.factory.post('/admin/common/dbdiff/')
        request.user = self.user
    
        fundingObj1 = FurtherFundingInformation.objects.create(
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
        
        enargusDataObj = Enargus.objects.create(
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

        self.dbDiff1 = DbDiff.objects.create(identifier="12345", diffStr="""<class 'project_listing.models.FurtherFundingInformation'>:
   furtherFundingInformation_id: 1 -> 2
   fundedBy: BMWK -> BundXYZ
   projectManagementAgency: PTJ -> Projektträger Jülich
   researchProgram: EnergieWEndeBauen -> Klima und Energie
   fundingProgram: Test-Project -> Erneuerbare Energien Programm""")
    
        # Simulate selecting books and calling the action
        queryset = DbDiff.objects.all()
        self.dbDiffAdmin.finalizeChange(request, queryset)
        
        fundingObjs = FurtherFundingInformation.objects.all()
        self.assertEqual(len(fundingObjs), 1)
        breakpoint()
