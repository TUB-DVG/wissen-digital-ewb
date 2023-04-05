"""This file executes the user specified changes in 'schlagwort_register_diff.md' file.

"""

import csv
import pdb

from django.core.management.base import BaseCommand
from encodings import utf_8
import yaml

from project_listing.DatabaseDifference import DatabaseDifference
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
        listOfParsedConflicts = self.parseFile(pathDiffFile)
        for databaseDiffObj in listOfParsedConflicts:
            if databaseDiffObj.checkIfUserInputIsValid():
                tupleOrNone = databaseDiffObj.checkIfConflictIsConsistentWithDatabase()
                if tupleOrNone is not None:
                    self.executeAction(tupleOrNone)
                    self.testIfChangesAreExecuted(databaseDiffObj, tupleOrNone)


    def add_arguments(self, parser):
        """
        
        """
        parser.add_argument('pathDiffFile', nargs='+', type=str) 

    
    def executeAction(self, listOfDatabaseObjs: list):
        """This method executes an valid user-specified Action from the database Difference Logfile. Therefore it gets 
        a list with all needed objects, which where extracted by the parseConflict method. Depending on the specified action
        the current state is kept and the pending state deleted from the database (optionCurrent == 1) or 
        the pending state is set as the new dataset, while the old dataset is deleted from the database (else-branch)

        listOfDatabaseObj:  list(obj)
            list of different objects, which are needed to solve the database conflict.
        
        """

        optionCurrent = listOfDatabaseObjs[0]  
        currentStateObj = listOfDatabaseObjs[1]
        pendingObj = listOfDatabaseObjs[2]   
        currentStateRow = listOfDatabaseObjs[3]
        nameOfFieldRelatesToTable = listOfDatabaseObjs[4]
        
        if optionCurrent:
            pendingObj.delete()
        
        else:
            currentStateObj.__setattr__(nameOfFieldRelatesToTable.name, pendingObj)
            currentStateObj.save()

            currentStateRow.delete()


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
        listOfParsedConflicts = []
        with open(filename, "r") as stream:
            for databaseDifferenceObj in yaml.load_all(stream, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()
                pdb.set_trace()
                listOfParsedConflicts.append(databaseDifferenceObj)

        return listOfParsedConflicts


    def testIfChangesAreExecuted(self, databaseConflictObj: DatabaseDifference, tupleOfDjangoDBObjs: tuple):
        """Tests, if the changes, specified in databaseConflictObj were executed in the Database.

        databaseConflictObj:    DatabaseDifference
            Object of type DatabaseDifference, containing all data relevant for the database conflict.
        
        tupleOfDjangoDBObjs: tuple

        """
        rootTableObj = tupleOfDjangoDBObjs[5]
        if databaseConflictObj.keepCurrentState:
            
            
            # check if state in Databade is current
            assert rootTableObj.__getattribute__(tupleOfDjangoDBObjs[4].name) == tupleOfDjangoDBObjs[1]

            # check if pendingObject has been deleted

        else:
            # check if pendingObject is the new current Object...
            assert rootTableObj.__getattribute__(tupleOfDjangoDBObjs[4].name) == tupleOfDjangoDBObjs[2]










