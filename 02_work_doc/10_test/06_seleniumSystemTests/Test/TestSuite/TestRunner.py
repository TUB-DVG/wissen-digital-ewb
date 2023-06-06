import sys
import os
import pdb
sys.path.append(sys.path[0] + "/...")
# Uncomment if the above example gives you a relative path error
sys.path.append(os.getcwd())
 
from unittest import TestLoader, TestSuite, TextTestRunner
from Test.Scripts.testDigitalTools import TestDigitalToolsTab
from Test.Scripts.testClickThroughAllSites import TestClickThroughSites
#from test.Scripts.test_Google_Search import Google_Search
 
import testtools as testtools
 
if __name__ == "__main__":
 
    test_loader = TestLoader()
    # Test Suite is used since there are multiple test cases
    test_suite = TestSuite((
        test_loader.loadTestsFromTestCase(TestDigitalToolsTab),
        test_loader.loadTestsFromTestCase(TestClickThroughSites),
        #test_loader.loadTestsFromTestCase(Google_Search),
        ))
 
    test_runner = TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
 
    # Refer https://testtools.readthedocs.io/en/latest/api.html for more information
    parallel_suite = testtools.ConcurrentStreamTestSuite(lambda: ((case, None) for case in test_suite))
    parallel_suite.run(testtools.StreamResult())
