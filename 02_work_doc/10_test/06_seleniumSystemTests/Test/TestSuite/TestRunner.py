import argparse
from unittest import TestLoader, TestSuite, TextTestRunner
import sys
import os
sys.path.append(sys.path[0] + "/...")
sys.path.append(os.getcwd())
 
from Test.Scripts.TestMainPage import TestMainPage
from Test.Scripts.TestDigitalTools import TestDigitalToolsPage
from Test.Scripts.TestClickThroughAllSites import TestClickThroughSites
from Test.Scripts.TestLastprofile import TestLastprofileTab
from Test.Scripts.TestAboutPage import TestAboutPage
from Test.Scripts.TestAdminPage import TestAdminPage
from Test.Scripts.TestBusinessApp import TestBusinessAppPage
from Test.Scripts.TestTechnicalStandarts import TestTechnicalStandarts
from Test.Scripts.TestNormsPage import TestNormsPage
from Test.Scripts.TestProtocolsPage import TestProtocolsPage
from Test.Scripts.TestSearch import TestSearch
from Test.Scripts.TestPublications import TestPublicationPage
from Test.Scripts.TestCriteriaCatalog import TestCriteriaCatalog
 
import testtools as testtools

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an optional argument
    parser.add_argument("--test_file", help="add a Test-file, which should be executed.")

    # Parse the command line arguments
    args = parser.parse_args()

    # Access the value of the optional argument
    testFileName = args.optional_arg

    testLoader = TestLoader()

    if testFileName is not None:
        testClass = getattr(sys.modules[__name__], testFileName)
        testSuite = TestSuite(
            (testLoader.loadTestsFromTestCase(testClass)),
        )
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
            testLoader.loadTestsFromTestCase(TestLastprofileTab),
            testLoader.loadTestsFromTestCase(TestAboutPage),
            testLoader.loadTestsFromTestCase(TestSearch),
            testLoader.loadTestsFromTestCase(TestPublicationPage),
            # testLoader.loadTestsFromTestCase(TestAdminPage),
            ))
 
    testRunner = TextTestRunner(verbosity=2)
    testRunner.run(testSuite)
 
    # Refer https://testtools.readthedocs.io/en/latest/api.html for more information
    parallelSuite = testtools.ConcurrentStreamTestSuite(lambda: ((case, None) for case in testSuite))
    parallelSuite.run(testtools.StreamResult())
