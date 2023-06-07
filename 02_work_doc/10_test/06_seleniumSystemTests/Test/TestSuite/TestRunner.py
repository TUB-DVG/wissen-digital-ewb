import sys
import os
sys.path.append(sys.path[0] + "/...")
sys.path.append(os.getcwd())
 
from unittest import TestLoader, TestSuite, TextTestRunner
from Test.Scripts.testDigitalTools import TestDigitalToolsTab
from Test.Scripts.testClickThroughAllSites import TestClickThroughSites
from Test.Scripts.testLastprofile import TestLastprofileTab
 
import testtools as testtools
 
if __name__ == "__main__":
 
    testLoader = TestLoader()
    # Test Suite is used since there are multiple test cases
    testSuite = TestSuite((
        # testLoader.loadTestsFromTestCase(TestDigitalToolsTab),
        # testLoader.loadTestsFromTestCase(TestClickThroughSites),
        testLoader.loadTestsFromTestCase(TestLastprofileTab),
        ))
 
    testRunner = TextTestRunner(verbosity=2)
    testRunner.run(testSuite)
 
    # Refer https://testtools.readthedocs.io/en/latest/api.html for more information
    parallelSuite = testtools.ConcurrentStreamTestSuite(lambda: ((case, None) for case in testSuite))
    parallelSuite.run(testtools.StreamResult())
