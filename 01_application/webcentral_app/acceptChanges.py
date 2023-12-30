import yaml
import pdb

import django 
django.setup()
# import DatabaseDifference
from project_listing.DatabaseDifference import DatabaseDifference
listOfDatabaseDifferences = []
with open("testFiles/2023_12_01_EWB_Tools_Uebersicht_v1_30122023_104604.yaml", "r") as stream:
    for data in yaml.load_all(stream, Loader=yaml.Loader):
        # pdb.set_trace()
        data.keepCurrentState = False
        data.keepPendingState = True
        listOfDatabaseDifferences.append(data)
with open("testFiles/2023_12_01_EWB_Tools_Uebersicht_v1_30122023_104604_modified.yaml", "w") as stream:
    yaml.dump_all(listOfDatabaseDifferences, stream)

