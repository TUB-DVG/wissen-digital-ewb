"""

"""

import unittest
import pdb

from django.core import management
#from django.core.management.commands import data_import_update

class checkDifferencesInDatabase(unittest.TestCase):
    """
    
    """

    def testDatabase(self):
        """
        
        """

        pdb.set_trace()
        # at first at a dataset to the empty database, which will be modified later:
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testOneDataSet.csv")
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testModifiedDataSet.csv")

        # with open("dbDiffs.csv", "a") as f:
        #     pdb.set_trace()



if __name__ == "__main__":
    unittest.main()