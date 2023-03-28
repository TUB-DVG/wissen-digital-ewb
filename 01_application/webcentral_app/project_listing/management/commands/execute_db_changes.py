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
    def handle(self, *args, **options):
        """
        
        """
        pathDiffFile = options["pathDiffFile"][0]
        self.parseFile(pathDiffFile)

    def add_arguments(self, parser):
        """
        
        """
        parser.add_argument('pathDiffFile', nargs='+', type=str) 

    
    def executeDiff(self, lineList):
        """This method parses a list of strings, which represents one difference 
        from the database-difference-logfile, and keeps the user-specified state,
        while discarding the other one.
        
        For that it first makes a consistency check: Only one state should be kept (user specified 1)
        and only one state should be discarded (user specified 0). If the user did not change the 
        default (10), the current differnce is ignored.

        lineList:   List(str)
            List of the lines of one Database-Difference. 
            It ends with the option Current: 1/0 and Pending: 1/0
            which indicate, which state should be kept.
        """

        pendingLine = lineList[-1]
        currentLine = lineList[-2]

        optionCurrent = currentLine.split(" ")[1].strip()
        optionPending = pendingLine.split(" ")[1].strip()

        

        identiferForConflictingObj = lineList[0].split("Conflict found for:")[1].strip().split(":")

        if "10" in optionPending or "10" in optionCurrent:
            print("Detected default-value (10). No changes in the DB will be made for current Difference!")
            return
        else:
            if (optionCurrent == "1" and optionPending == "0") or (optionCurrent == "0" and optionPending == "1"):
                
                tableName = lineList[1].split(".")[1].lower().strip()
                parentTable = lineList[1].split(".")[0].strip()
                currentStateRow = lineList[2].strip().split("|")
                pendingStateRow = lineList[3].strip().split("|")
                idAttributeStr = tableName + "_id"
                for cellInRow in pendingStateRow:
                    
                    if idAttributeStr in cellInRow:
                        idOfPendingState = int(cellInRow.split(":")[1].strip())
                        nameOfIdColumn = cellInRow.split(":")[0].strip()
                        pendingObj = globals()[tableName[0].upper() + tableName[1:].lower()].objects.filter(**{nameOfIdColumn: idOfPendingState})[0]
                        #pdb.set_trace()
                        if optionCurrent == "1":
                            
                            pendingObj.delete()
                        else:
                            currentStateObj = globals()[parentTable].objects.filter(**{identiferForConflictingObj[0]: identiferForConflictingObj[1].strip()})[0]
                            
                            tableNameUpper = tableName[0].upper() + tableName[1:].lower()
                            nameOfFieldRelatesToTable = self.findFieldNameRelatingToForeignTable(globals()[parentTable], globals()[tableNameUpper])
                            currentStateRow = currentStateObj.__getattribute__(nameOfFieldRelatesToTable.name)
                            pdb.set_trace()
                            
                            currentStateObj.__setattr__(nameOfFieldRelatesToTable.name, pendingObj)
                            currentStateObj.save()
                             
                            #globals()[parentTable].objects.filter
                            currentStateRow.delete()

                                #globals()[parentTable].objects.filter(**identiferForConflictingObj[0]=identiferForConflictingObj[1].strip(), cellInRow[0]=int(idOfPendingState))
                            

                


    def findFieldNameRelatingToForeignTable(self, parentTable, tableObj):
        """
        
        """
        listOfFields = parentTable._meta.get_fields()

        for field in listOfFields:
            if field.is_relation:
                if field.related_model == tableObj:
                    return field

    def parseFile(self, filename):
        """
        
        """

        with open(filename, "r") as f:
            lines = f.readlines()
            currentDiffList = []
            for line in lines:
                if not ("Pending: 1" in line or "Pending: 0" in line):
                    currentDiffList.append(line)
                else:
                    currentDiffList.append(line)
                    self.executeDiff(currentDiffList)
                    currentDiffList = []
            #reader = csv.reader(f, delimiter='|')
            
            # for row in reader:
            #     #pdb.set_trace()
            #     fkz = row[1] 
            #     currentSchlagwortregisterId = int(row[2])
            #     newSchlagwortregisterId = int(row[3])
            #     if row[4] == "U":

            #         Teilprojekt.objects.filter(
            #             fkz=fkz, 
            #             schlagwortregister_erstsichtung_id=currentSchlagwortregisterId,
            #         ).update(schlagwortregister_erstsichtung_id=newSchlagwortregisterId)

            #         # check if currentSchlagwortregisterId is used by other fkz and deletes it, if not:
            #         if len(Teilprojekt.objects.filter(schlagwortregister_erstsichtung_id=currentSchlagwortregisterId)) == 0:
            #             Schlagwortregister_erstsichtung.objects.filter(schlagwortregister_id=currentSchlagwortregisterId).delete()

            #     if row[4] == "K":
            #         listOfNotUpdatedSchlagwortregisterIDs.append(newSchlagwortregisterId)
            
            # for notUpdatedSchlagwortRegisterId in listOfNotUpdatedSchlagwortregisterIDs:
            #     queryForNotUpdatedID = Teilprojekt.objects.filter(schlagwortregister_erstsichtung_id=notUpdatedSchlagwortRegisterId)

            #     if len(queryForNotUpdatedID) == 0:
            #         Schlagwortregister_erstsichtung.objects.filter(schlagwortregister_id=notUpdatedSchlagwortRegisterId).delete()


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

