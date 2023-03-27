"""

"""

#import unittest
import pdb

from django.core import management
from django.test import TransactionTestCase
# from project_listing.models import *
# from tools_over.models import *
# from weatherdata_over.models import *
# from schlagwoerter.models import *
#from django.core.management.commands import data_import_update

class checkDifferencesInDatabase(TransactionTestCase):
    """
    
    """

    def test_Database(self):
        """
        
        """

        #pdb.set_trace()
        # at first at a dataset to the empty database, which will be modified later:
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testOneDataSet.csv")
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testModifiedDataSet.csv")

        with open("dbDiffs.csv", "r") as f:
            pdb.set_trace()



# if __name__ == "__main__":
#     unittest.main()