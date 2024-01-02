import yaml
import pdb

import django 
django.setup()
# import DatabaseDifference
from project_listing.DatabaseDifference import DatabaseDifference
listOfDatabaseDifferences = []
with open("../../postgres/2023_12_15_EWB_Tools_Uebersicht_v2_02012024_140347.yaml", "r") as stream:
    for data in yaml.load_all(stream, Loader=yaml.Loader):
        # pdb.set_trace()
        data.keepCurrentState = False
        data.keepPendingState = True
        listOfDatabaseDifferences.append(data)
with open("../../postgres/2023_12_15_EWB_Tools_Uebersicht_v2_02012024_140347_modified.yaml", "w") as stream:
    yaml.dump_all(listOfDatabaseDifferences, stream)

