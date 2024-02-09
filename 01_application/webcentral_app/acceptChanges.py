import yaml
import pdb
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcentral_app.settings')
import django 
django.setup()
# import DatabaseDifference
from project_listing.DatabaseDifference import DatabaseDifference
listOfDatabaseDifferences = []
with open("2024_02_06_EWB_Tools_Uebersicht_reclassified_v2_09022024_085514.yaml", "r") as stream:
    for data in yaml.load_all(stream, Loader=yaml.Loader):
        # pdb.set_trace()
        data.keepCurrentState = False
        data.keepPendingState = True
        listOfDatabaseDifferences.append(data)
with open("2024_02_06_EWB_Tools_Uebersicht_reclassified_v2_09022024_085514.yaml", "w") as stream:
    yaml.dump_all(listOfDatabaseDifferences, stream)

