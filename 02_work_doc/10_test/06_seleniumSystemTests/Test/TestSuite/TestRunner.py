import argparse
from unittest import TestLoader, TestSuite, TextTestRunner
import sys
import os

sys.path.append(sys.path[0] + "/...")
sys.path.append(os.getcwd())

from Test.Scripts.TestMainPage import TestMainPage
from Test.Scripts.TestDigitalTools import TestDigitalToolsPage
from Test.Scripts.TestClickThroughAllSites import TestClickThroughSites
from Test.Scripts.TestLastProfile import TestLastProfile
from Test.Scripts.TestAboutPage import TestAboutPage
from Test.Scripts.TestAdminPage import TestAdminPage
from Test.Scripts.TestBusinessApp import TestBusinessAppPage
from Test.Scripts.TestTechnicalStandarts import TestTechnicalStandarts
from Test.Scripts.TestNormsPage import TestNormsPage
from Test.Scripts.TestProtocolsPage import TestProtocolsPage
from Test.Scripts.TestSearch import TestSearch
from Test.Scripts.TestPublications import TestPublicationPage
from Test.Scripts.TestComponentsList import TestComponentsList
from Test.Scripts.TestUserEngagement import TestUserEngagement

# from Test.Scripts.TestLastprofile import TestLastprofileTab
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
            testLoader.loadTestsFromTestCase(TestDigitalToolsPage),
            testLoader.loadTestsFromTestCase(TestMainPage),
            testLoader.loadTestsFromTestCase(TestTechnicalStandarts),
            testLoader.loadTestsFromTestCase(TestNormsPage),
            testLoader.loadTestsFromTestCase(TestProtocolsPage),
            testLoader.loadTestsFromTestCase(TestBusinessAppPage),
            testLoader.loadTestsFromTestCase(TestClickThroughSites),
            testLoader.loadTestsFromTestCase(TestLastprofile),
            testLoader.loadTestsFromTestCase(TestAboutPage),
            testLoader.loadTestsFromTestCase(TestSearch),
            testLoader.loadTestsFromTestCase(TestPublicationPage),
            testLoader.loadTestsFromTestCase(TestComponentsList),
            testLoader.loadTestsFromTestCase(TestUserEngagement),
            # testLoader.loadTestsFromTestCase(TestAdminPage),
        ))

    testRunner = TextTestRunner(verbosity=2)
    testRunner.run(testSuite)

    # Refer https://testtools.readthedocs.io/en/latest/api.html for more information
    parallelSuite = testtools.ConcurrentStreamTestSuite(
        lambda: ((case, None) for case in testSuite))
    parallelSuite.run(testtools.StreamResult())
