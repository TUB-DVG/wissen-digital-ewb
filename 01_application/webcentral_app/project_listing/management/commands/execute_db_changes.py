"""This file executes the user specified changes in 
'schlagwort_register_diff.md' file.

"""
import pdb

from django.core.management.base import BaseCommand
from encodings import utf_8
import yaml

# from project_listing.DatabaseDifference import DatabaseDifference
from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from schlagwoerter.models import *

class Command(BaseCommand):
    """
    
    """
    def handle(self, *args, **options):
        """Called from Django, when executing Class as Django-Command.

        This method gets called by the manage.py, when executing the 
        Django-Admin-Command:
        ```
            python3 manage.py execute_db_changes pathToYAMLFile
        ```

        Parameters: tuple
        *args:   tuple of optional parameters, which is unpacked with
            * operator.     
        **options:  dict
            optional parameters in key:value format.
        
        Returns:
        None
        """
        pathDiffFile = options["pathDiffFile"][0]
        listOfParsedConflicts = self.parseFile(pathDiffFile)
        for databaseDiffObj in listOfParsedConflicts:
            if databaseDiffObj.checkIfUserInputIsValid():
                tupleOrNone = databaseDiffObj.checkIfConflictIsConsistentWithDatabase()
                if tupleOrNone is not None:
                    self.executeAction(
                        tupleOrNone, 
                        databaseDiffObj.differencesSortedByTable
                    )


    def add_arguments(self, parser) -> None:
        """Called by Django, when parsing the CLI-Call 

        This method gets called by Django, when it parses the command-
        line-execution of the user-defined Django-Admin-Command and 
        additional arguments are present. The additional argument 
        is then parsed to string and given to the options-parameter
        in the handle-method.

        Parameters:
        parser: django-obj
            object, which parses the CLI-Input. 
        
        Returns:
        None
        """
        parser.add_argument('pathDiffFile', nargs='+', type=str) 

    
    def executeAction(
            self, 
            listOfDatabaseObjs: list,
            diffDataStructure: dict,
        ) -> None:
        """Executes the user-specified Action for a Dataset-Conflict.
        
        This method executes an valid user-specified Action from 
        the database Difference Logfile. Therefore it gets a list with
        all needed objects, which where extracted by the parseConflict 
        method. Depending on the specified action the current state is 
        kept and the pending state deleted from the database 
        (optionCurrent == 1) or the pending state is set as the new 
        dataset, while the old dataset is deleted from the database 
        (else-branch). 
        For the Schlagwortregister-Case special-code has to be 
        executed, to check if the `Schlagwort` is used by another
        tuple of type `schlagwortregister_erstsichtung`.

        Parameters:
        listOfDatabaseObj:  list(obj)
            list of different objects, which are needed to solve the 
            database conflict.
        diffDataStructure:  dict
            Nested Dictionary containing all Differences, sorted 
            by Table.
        
        Returns:
        None
        """
        
        optionCurrent = listOfDatabaseObjs[0]  
        currentStateObj = listOfDatabaseObjs[1]
        pendingObj = listOfDatabaseObjs[2]   
        currentStateRow = listOfDatabaseObjs[3]
        nameOfFieldRelatesToTable = listOfDatabaseObjs[4]
        diffDataStructure
        if optionCurrent:
            for currentTable in list(diffDataStructure.keys()):
                if "Teilprojekt" in currentTable:
                    #pass
                    parent = currentTable.split(".")[1]
                else:
                    if parent in currentTable.split(".")[0]:
                        deleteSchlagwort = True
                        if parent == "schlagwortregister_erstsichtung":
                            for tagNumber in range(1, 7):
                                dictForFilter = {
                                    f"schlagwort_{tagNumber}_id": 
                                    diffDataStructure[currentTable]["pendingState"]["schlagwort_id"]
                                }
                                
                                if len(
                                    Schlagwortregister_erstsichtung\
                                        .objects.filter(**dictForFilter)
                                    ) > 1:
                                    deleteSchlagwort = False
                            if deleteSchlagwort:
                                
                                query = Schlagwort\
                                    .objects.filter(
                                    schlagwort_id=diffDataStructure[currentTable]["pendingState"]["schlagwort_id"]
                                    )
                                query[0].delete()
            pendingObj.delete()
        
        else:
            currentStateObj.__setattr__(
                nameOfFieldRelatesToTable.name, 
                pendingObj,
            )
            currentStateObj.save()

            currentStateRow.delete()
            for currentTable in list(diffDataStructure.keys()):
                if "Teilprojekt" in currentTable:
                    parent = currentTable.split(".")[1]
                else:
                    if parent in currentTable.split(".")[0]:
                        deleteSchlagwort = True
                        if parent == "schlagwortregister_erstsichtung":
                            for tagNumber in range(1, 7):
                                dictForFilter = {
                                    f"schlagwort_{tagNumber}_id": 
                                    diffDataStructure[currentTable]["currentState"]["schlagwort_id"]
                                }
                                #pdb.set_trace()
                                if len(
                                    Schlagwortregister_erstsichtung.objects.filter(**dictForFilter)
                                    ) > 1:
                                    deleteSchlagwort = False
                            if deleteSchlagwort:
                                
                                query = Schlagwort\
                                    .objects.filter(
                                    schlagwort_id=diffDataStructure[currentTable]["currentState"]["schlagwort_id"]
                                    )
                                query[0].delete()

            




    def parseFile(self, filename):
        """Parses the given .YAML-file to a list of DatabaseDifference-objects.

        Parameters:
        filename:   str
            filename of the .YAML-file, which holds the database-Differences

        Returns:
        listOfParsedConflicts:  list
            List of parsed Database-Conflicts, represented as 
            database-Difference Objects.
        
        """
        listOfParsedConflicts = []
        with open(filename, "r") as stream:
            for databaseDifferenceObj in yaml.load_all(stream, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()
                listOfParsedConflicts.append(databaseDifferenceObj)

        return listOfParsedConflicts












