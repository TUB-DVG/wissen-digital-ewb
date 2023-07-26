import yaml
import pdb

import django 
django.setup()
# import DatabaseDifference
from project_listing.DatabaseDifference import DatabaseDifference
listOfDatabaseDifferences = []
with open("1690272995.yaml", "r") as stream:
    for data in yaml.load_all(stream, Loader=yaml.Loader):
        # pdb.set_trace()
        data.keepCurrentState = False
        data.keepPendingState = True
        listOfDatabaseDifferences.append(data)
with open("1690272995_edited.yaml", "w") as stream:
    yaml.dump_all(listOfDatabaseDifferences, stream)

