import json

from django.test import TransactionTestCase
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
from django.core.management import call_command
from django.contrib.auth import get_user_model

from .models import Norm, History
from .admin import HistoryAdminApp

User = get_user_model()


class TestDataImport(TransactionTestCase):
    """TestCase for all tests regarding the data-import of the structured
    protocol-data.

    """

    def testImportOfExcelFile(self):
        """Test if the protocol-data excel file is imported as expected."""
        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/norms.xlsx",
        )

        allNorms = Norm.objects.all()
        self.assertGreater(len(allNorms), 67)

        for norm in allNorms:
            self.assertEqual(len(norm.focus.all()), 1)
            self.assertEqual(norm.focus.all()[0].focus_de, "technisch")
            self.assertEqual(norm.focus.all()[0].focus_en, "technical")

    def testImportWithDummyDataForAllFields(self):
        """Import the file `test_data/test_import_for_all_fields.xlsx`"""
        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/test_data/test_import_for_all_fields.xlsx",
        )

        allNorms = Norm.objects.all()
        self.assertEqual(len(allNorms), 1)
        self.assertEqual(allNorms[0].name_de, "ISO 14064")
        self.assertEqual(allNorms[0].name_en, "ISO 14064")

        allAreaOfApplications = self._checkMany2ManyObjs(
            allNorms[0], "applicationArea", 2
        )
        self._checkElementsOfM2MObjs(
            allAreaOfApplications,
            "applicationArea",
            ["Bilanzierung", "Verifizierung"],
            ["Accounting", "Verification"],
        )

        allLifeCyclePhaseObj = self._checkMany2ManyObjs(
            allNorms[0], "lifeCyclePhase", 2
        )
        self._checkElementsOfM2MObjs(
            allLifeCyclePhaseObj,
            "lifeCyclePhase",
            ["Forschung", "Entwicklung"],
            ["Research", "Development"],
        )

        targetGroupObjs = self._checkMany2ManyObjs(
            allNorms[0], "targetGroup", 2
        )
        self._checkElementsOfM2MObjs(
            targetGroupObjs,
            "targetGroup",
            ["Entwickler", "Ingenieure"],
            ["Developers", "Engineers"],
        )

        scaleObjs = self._checkMany2ManyObjs(allNorms[0], "scale", 2)
        self._checkElementsOfM2MObjs(
            scaleObjs, "scale", ["Haus", "Quartier"], ["Building", "District"]
        )

        licenseObjs = self._checkMany2ManyObjs(allNorms[0], "license", 2)

        self._checkElementsOfM2MObjs(
            licenseObjs, "license", ["MPL", "ITS"], None
        )

        accessiblitiyObjs = self._checkMany2ManyObjs(
            allNorms[0], "accessibility", 2
        )
        self._checkElementsOfM2MObjs(
            accessiblitiyObjs,
            "accessibility",
            ["Offen", "Kostenlos"],
            ["Open", "Free"],
        )
        usageObjs = self._checkMany2ManyObjs(allNorms[0], "usage", 2)
        self._checkElementsOfM2MObjs(
            usageObjs,
            "usage",
            ["Nutzung1", "Nutzung2345"],
            ["Usage1", "Usage2"],
        )

        protocolObjs = self._checkMany2ManyObjs(allNorms[0], "protocol_set", 2)
        self._checkElementsOfM2MObjs(protocolObjs, "name", ["HTTP", "IP"], None)

        connectedProjects = self._checkMany2ManyObjs(
            allNorms[0], "specificApplication", 2
        )

        projectOne = connectedProjects.filter(referenceNumber_id="03EN3013B")
        self.assertEqual(len(projectOne), 1)

        projectTwo = connectedProjects.filter(referenceNumber_id="03ET1636B")
        self.assertEqual(len(projectTwo), 1)

        self._checkRegularField(allNorms[0], "yearOfRelease", "2016", "2016")
        self._checkRegularField(
            allNorms[0], "alternatives", "ISO 14065", "ISO 14065"
        )
        self._checkRegularField(
            allNorms[0], "alternatives", "ISO 14065", "ISO 14065"
        )

        self._checkRegularField(allNorms[0], "image", "norm.jpg", None)
        self._checkRegularField(allNorms[0], "developmentState", 1, None)

        self._checkRegularField(
            allNorms[0],
            "furtherInformation",
            "hier stehen weitere Informationen zu der Norm",
            "Here are further information for the norm specified.",
        )

        allFocusElements = allNorms[0].focus.all()
        self.assertEqual(len(allFocusElements), 1)
        self.assertEqual(allFocusElements[0].focus_en, "technical")
        self.assertEqual(allFocusElements[0].focus_de, "technisch")

    def _checkMany2ManyObjs(self, normObj, m2mName, expectedM2mObjNbrs):
        """ """
        connectedM2mObjs = getattr(normObj, m2mName).all()
        self.assertEqual(len(connectedM2mObjs), 2)

        return connectedM2mObjs

    def _checkElementsOfM2MObjs(
        self, m2mObjs, fieldName, germanStrList, englishStrList
    ):
        """ """
        for index, germanName in enumerate(germanStrList):
            try:
                querysetResult = m2mObjs.filter(
                    **{f"{fieldName}_de": germanName}
                )
            except:

                querysetResult = m2mObjs.filter(**{f"{fieldName}": germanName})

            self.assertEqual(len(querysetResult), 1)

            if englishStrList is not None:
                querysetResultEn = m2mObjs.filter(
                    **{f"{fieldName}_en": englishStrList[index]}
                )
                self.assertEqual(len(querysetResultEn), 1)

    def _checkRegularField(
        self, obj, attributeName, expectedValueDe, expectedValueEn=None
    ):
        """ """
        try:
            objValueDe = getattr(obj, attributeName + "_de")
        except:
            objValueDe = getattr(obj, attributeName)
        self.assertEqual(objValueDe, expectedValueDe)

        if expectedValueEn is not None:
            self.assertEqual(
                getattr(obj, attributeName + "_en"), expectedValueEn
            )


class TestUpdate(TransactionTestCase):
    """Test if the update process works for `Norm`"""

    def setUp(self):
        """setUp method for all methods of `DbDiffAdminTest`"""

        self.site = AdminSite()
        self.historyAdmin = HistoryAdminApp(History, self.site)

        # Create a test user and request factory
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.factory = RequestFactory()

    def testUpdate(self):
        """Test if only one History object is created, if one row is changed."""
        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/norms.xlsx",
        )

        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/test_data/all_norms_with_one_diff.xlsx",
        )

        # only one History object, should have been created, since the 2 excel
        # files only differ in one row.
        self.assertEqual(len(History.objects.all()), 1)

        # the norm "BISKO" has updated values in the excel file test_data/all_norms_with_one_diff.xlsx
        # it should be tested, if these changes have been loaded into the database
        # and if the old state can be rollbackd.
        biskoNorm = Norm.objects.filter(name="BISKO")
        self.assertEqual(len(biskoNorm), 1)

        self.assertTrue("Hallo" in biskoNorm[0].description_de)
        self.assertTrue("Hello" in biskoNorm[0].description_en)

        connectedLiceCyclePhaseToBisko = biskoNorm[0].lifeCyclePhase.all()
        self.assertEqual(len(connectedLiceCyclePhaseToBisko), 2)
        needsAnalysis = connectedLiceCyclePhaseToBisko.filter(
            lifeCyclePhase_de="Bedarfsanalyse"
        )
        self.assertTrue(len(needsAnalysis), 1)
        self.assertEqual(needsAnalysis[0].lifeCyclePhase_en, "Needs analysis")

        prePlanning = connectedLiceCyclePhaseToBisko.filter(
            lifeCyclePhase_de="Vorplanung"
        )
        self.assertTrue(len(prePlanning), 1)
        self.assertEqual(prePlanning[0].lifeCyclePhase_en, "Pre-planning")

        # test if protocols are connected to norm:
        protocolsForBisko = biskoNorm[0].protocol_set.all()
        self.assertEqual(len(protocolsForBisko), 1)
        self.assertEqual(protocolsForBisko[0].name, "HTTP")

        # rollback to the old state:
        self._rollbackAllChanges()

        biskoNorm = Norm.objects.filter(name="BISKO")
        self.assertTrue("Hallo" not in biskoNorm[0].description_de)
        self.assertTrue("Hello" not in biskoNorm[0].description_en)

        self.assertEqual(len(biskoNorm[0].lifeCyclePhase.all()), 0)
        self.assertEqual(len(biskoNorm[0].protocol_set.all()), 0)

    def testUpdateJsonManyToManyRel(self):
        """When updating from a norms state, which included a protocol in the backward reference of the
        ManyToMany-Relation to protocols, the conected protocols should be included in the stringified old
        state of the Norm and should be possible to be rollbacked. This is tested, with the following test method.

        """
        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/test_data/all_norms_with_one_diff.xlsx",
        )
        call_command(
            "data_import",
            "TechnicalStandards",
            "../doc/01_data/05_technical_standards/norms.xlsx",
        )

        allHistoryObjs = History.objects.all()
        self.assertEqual(len(allHistoryObjs), 1)
        jsonObj = json.loads(allHistoryObjs[0].stringifiedObj)
        self.assertEqual(jsonObj[0]["fields"]["protocol"][0], "HTTP")

        biskoNormQuery = Norm.objects.filter(name="BISKO")
        self.assertEqual(len(biskoNormQuery), 1)
        self.assertEqual(len(biskoNormQuery[0].protocol_set.all()), 0)

        # check if the state with the backward reference to protocol can be rollbacked:
        self._rollbackAllChanges()

        biskoNormQuery = Norm.objects.filter(name="BISKO")
        self.assertEqual(len(biskoNormQuery[0].protocol_set.all()), 1)
        self.assertEqual(biskoNormQuery[0].protocol_set.all()[0].name, "HTTP")

    def _rollbackAllChanges(self):
        """Wraps the call of the rollback into a function:"""
        request = self.factory.post("/admin/TechnicalStandards/history/")
        request.user = self.user

        self.historyAdmin.rollbackHistory(request, History.objects.all())
