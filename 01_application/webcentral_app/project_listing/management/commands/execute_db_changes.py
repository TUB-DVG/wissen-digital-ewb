"""This file executes the user specified changes in 'schlagwort_register_diff.md' file.

"""

import csv
import pdb

from django.core.management.base import BaseCommand
from encodings import utf_8
from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from schlagwoerter.models import *

class Command(BaseCommand):
    """
    
    """

    def __init__(self, filename):
        """
        
        """

        self.filename = filename
    
    def executeChanges(self):
        """
        
        """
        #pdb.set_trace()
        listOfNotUpdatedSchlagwortregisterIDs = []

        with open(self.filename, "r") as f:
            reader = csv.reader(f, delimiter='|')
            
            for row in reader:
                #pdb.set_trace()
                fkz = row[1] 
                currentSchlagwortregisterId = int(row[2])
                newSchlagwortregisterId = int(row[3])
                if row[4] == "U":

                    Teilprojekt.objects.filter(
                        fkz=fkz, 
                        schlagwortregister_erstsichtung_id=currentSchlagwortregisterId,
                    ).update(schlagwortregister_erstsichtung_id=newSchlagwortregisterId)

                    # check if currentSchlagwortregisterId is used by other fkz and deletes it, if not:
                    if len(Teilprojekt.objects.filter(schlagwortregister_erstsichtung_id=currentSchlagwortregisterId)) == 0:
                        Schlagwortregister_erstsichtung.objects.filter(schlagwortregister_id=currentSchlagwortregisterId).delete()

                if row[4] == "K":
                    listOfNotUpdatedSchlagwortregisterIDs.append(newSchlagwortregisterId)
            
            for notUpdatedSchlagwortRegisterId in listOfNotUpdatedSchlagwortregisterIDs:
                queryForNotUpdatedID = Teilprojekt.objects.filter(schlagwortregister_erstsichtung_id=notUpdatedSchlagwortRegisterId)

                if len(queryForNotUpdatedID) == 0:
                    Schlagwortregister_erstsichtung.objects.filter(schlagwortregister_id=notUpdatedSchlagwortRegisterId).delete()


    def testIfChangesAreExecuted(self):
        """This method tests if the changes specified in "filename" were successfull.
        
        """
        with open(self.filename, "r") as f:
            reader = csv.reader(f, delimiter='|')
            for rowNumber, row in enumerate(reader):
                print(f"Check if row number {rowNumber} in .csv file has been executed...")
                #pdb.set_trace()
                fkz = row[1] 
                currentSchlagwortregisterId = int(row[2])
                newSchlagwortregisterId = int(row[3])
                if row[4] == "U":
                    if len(Teilprojekt.objects.filter(fkz=fkz, schlagwortregister_erstsichtung_id=newSchlagwortregisterId)) == 0:
                        assert False, f"Teilprojekt with Förderkennziffer {fkz} and SchlagwortregisterId {newSchlagwortregisterId} doesn't exist!"
                
                if row[4] == "K":
                    pdb.set_trace()
                    if len(Teilprojekt.objects.filter(fkz=fkz, schlagwortregister_erstsichtung_id=currentSchlagwortregisterId)) == 0:
                        assert False, f"Teilprojekt with Förderkennziffer {fkz} and SchlagwortregisterId {currentSchlagwortregisterId} doesn't exist!"                    

