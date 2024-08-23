import argparse
from unittest import TestLoader, TestSuite, TextTestRunner
import sys
import os

sys.path.append(sys.path[0] + "/...")
sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test.scripts.test_main_page import TestMainPage
from test.scripts.test_navbar import TestNavbar
# from test.scripts.test_tools import TestDigitalToolsPage
# from test.scripts.test_click_sites import TestClickThroughSites
# from test.scripts.test_lastprofile import TestLastProfile
# from test.scripts.test_about_page import TestAboutPage
# from test.scripts.test_admin_page import TestAdminPage
# from test.scripts.test_business_app import TestBusinessAppPage
# from test.scripts.test_technical_standards import TestTechnicalStandards
# from test.scripts.TestNormsPage import TestNormsPage
# from test.scripts.TestProtocolsPage import TestProtocolsPage
# from test.scripts.TestSearch import TestSearch
# from test.scripts.TestPublications import TestPublicationPage
# from test.scripts.TestComponentsList import TestComponentsList
# from test.scripts.TestUserEngagement import TestUserEngagement
# from test.scripts.TestNegativeEnvironmentalImpacts import (
#     TestNegativeEnvironmentalImpacts, )
# from test.scripts.TestBusinessModels import TestBusinessModels
# from test.scripts.TestBusinessModelChallenges import TestBusinessModelChallenges
# from test.scripts.TestCriteriaCatalog import TestCriteriaCatalog
# from test.scripts.TestUseCases import TestUseCases
# from test.scripts.TestPositiveEnvironmentalImpact import TestPositiveEnvironmentalImpact
# from test.scripts.TestDataSufficiency import TestDataSufficiency
# # from test.scripts.TestLastprofile import TestLastprofileTab
import testtools as testtools

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an optional argument for the test file and test method
    parser.add_argument("--test_file",
                        help="add a Test-file, which should be executed.")
    parser.add_argument("--test_method",
                        help="add a Test-method, which should be executed.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the value of the optional arguments
    testFileName = args.test_file
    testMethodName = args.test_method

    testLoader = TestLoader()

    if testFileName is not None and testMethodName is not None:
        # Load the specific test method from the test file
        # breakpoint()
        testSuite = testLoader.loadTestsFromName(testMethodName,
                                                 module=getattr(
                                                     sys.modules[__name__],
                                                     testFileName))
    elif testFileName is not None:
        # Load all test methods from the test file
        testClass = getattr(sys.modules[__name__], testFileName)
        testSuite = TestSuite((testLoader.loadTestsFromTestCase(testClass)), )
    else:
        # Test Suite is used since there are multiple test cases
        testSuite = TestSuite((
            # testLoader.loadTestsFromTestCase(TestDigitalToolsPage),
            testLoader.loadTestsFromTestCase(TestMainPage),
            testLoader.loadTestsFromTestCase(TestNavbar),
            # testLoader.loadTestsFromTestCase(TestTechnicalStandarts),
            # testLoader.loadTestsFromTestCase(TestNormsPage),
            # testLoader.loadTestsFromTestCase(TestProtocolsPage),
            # testLoader.loadTestsFromTestCase(TestBusinessAppPage),
            # testLoader.loadTestsFromTestCase(TestClickThroughSites),
            # testLoader.loadTestsFromTestCase(TestLastProfile),
            # testLoader.loadTestsFromTestCase(TestAboutPage),
            # testLoader.loadTestsFromTestCase(TestSearch),
            # testLoader.loadTestsFromTestCase(TestPublicationPage),
            # testLoader.loadTestsFromTestCase(TestComponentsList),
            # testLoader.loadTestsFromTestCase(TestUserEngagement),
            # testLoader.loadTestsFromTestCase(TestNegativeEnvironmentalImpacts),
            # testLoader.loadTestsFromTestCase(TestBusinessModels),
            # testLoader.loadTestsFromTestCase(TestBusinessModelChallenges),
            # testLoader.loadTestsFromTestCase(TestCriteriaCatalog),
            # testLoader.loadTestsFromTestCase(TestUseCases),
            # testLoader.loadTestsFromTestCase(TestPositiveEnvironmentalImpact),
            # testLoader.loadTestsFromTestCase(TestDataSufficiency), 
            # # testLoader.loadTestsFromTestCase(TestAdminPage),
        ))

    testRunner = TextTestRunner(verbosity=2)
    testRunner.run(testSuite)

    # Refer https://testtools.readthedocs.io/en/latest/api.html for more information
    parallelSuite = testtools.ConcurrentStreamTestSuite(
        lambda: ((case, None) for case in testSuite))
    parallelSuite.run(testtools.StreamResult())
