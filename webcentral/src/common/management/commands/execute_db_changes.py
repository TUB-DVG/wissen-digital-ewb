"""Executes Changes from User-edited .YAML-DatabaseDifference-File.

This module solves Database-Conflicts by executing User specified 
actions on a Database-Conflict. A conflict is present, if two different
Datasets are pointing to the same Förderkennziffer (fkz). This can 
happen, if a dataset was updated in the .csv/.xml-file. 
The user-specified action is done, by setting boolean-values for 
`keepPendingState` and `keepCurrentState` in the .yaml-file. These
values have to be set consistent: Only one Dataset can be kept, the
other one should be deleted. Consistent States are:
keepCurrent = true
keepPending = false
or
keepCurrent = false
keepPending = true
Only if a consistent user-input is present, it is executed by
`execute_db_changes`.
The `execute_db_changes`-Script can be executed as a user-defined
Django-Admin Command. First, the Directory needs to be changed to 
where the Django manage.py is located. After that the following 
line needs to be executed:
```
    python3 manage.py execute_db_changes pathToYAML.yaml
```
`pathToYAML.yaml` is a placeholder for the relative/absolute path 
to a .yaml-file with consistent user-specified actions. 
If it is specified to keep the current Database state 
(keepCurrent = true) and delete the CSV-State from the database 
(keepPending = false) only the CSV-Dataset is deleted from the 
database. If the oposite case is present, the current Dataset 
connected to the fkz is deleted (keepCurrent = false) and the 
foreign-key of the CSV-Dataset is set for the fkz 
(keepPending = true).
"""
import yaml
from encodings import utf_8

from django.core.management.base import BaseCommand

from tools_over.models import Tools


class Command(BaseCommand):
    """Defines Django user-defined Command.

    This Class defines a user-defined Django-Admin Command, which can 
    be executed with the Django `manage.py`. On execution, the 
    `manage.py` calls the `handle`-method of this class and passes 
    the as argument specified path to the .yaml-file inside the 
    options-dict into the method.
    Inside the .yaml-file serialiazed python objects of type 
    `DatabaseDifference` are located. The pyyaml-package constructs
    a list of `DatabaseDifference`-objects from the yaml-file.
    On each object, the executeAction-method is called, which executes
    the user-specified action on the database-conflict, if it is 
    consitent.
    """

    def __init__(self):
        """
        
        """
        self.listOfToBeDeletedObjs = []


    def handle(
            self, 
            *args: tuple, 
            **options: dict,
        ) -> None:
        """Called from Django, when executing Class as Django-Command.

        This method gets called by the manage.py, when executing the 
        Django-Admin-Command:
        ```
            python3 manage.py execute_db_changes pathToYAMLFile.yaml
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

        for objToBeDeleted in self.listOfToBeDeletedObjs:
            if "subproject" in dir(objToBeDeleted):
                objToBeDeleted.refresh_from_db()
                try:
                    objToBeDeleted.teilprojekt
                except:
                    objToBeDeleted.delete()
            elif "subproject_set" in dir(objToBeDeleted):
                try:
                    objToBeDeleted.refresh_from_db()
                except:
                    pass
                if len(objToBeDeleted.subproject_set.all()) == 0:
                    objToBeDeleted.delete()
            else:
                pdb.set_trace()


    def add_arguments(
            self, 
            parser,
        ) -> None:
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
        executed, to check if the `Keyword` is used by another
        tuple of type `KeywordRegisterFirstReview`.

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
        if optionCurrent:
            if isinstance(currentStateObj, Tools):
                pendingObj.delete()
            else:

                for currentTable in list(diffDataStructure.keys()):
                    if "Subproject" in currentTable:
                        parent = currentTable.split(".")[1]
                for currentTable in list(diffDataStructure.keys()):
                    if "Subproject" not in currentTable:
                        if parent in currentTable.split(".")[0]:
                            deleteSchlagwort = True
                            if parent == "KeywordRegisterFirstReview":
                                pass

                self.listOfToBeDeletedObjs.append(pendingObj)
        
        else:
            if isinstance(currentStateObj, Tools):
                currentStateObj.name = pendingObj.name
                currentStateObj.shortDescription = pendingObj.shortDescription
                currentStateObj.applicationArea.set(pendingObj.applicationArea.select_related())
                currentStateObj.usage.set(pendingObj.usage.select_related())
                currentStateObj.lifeCyclePhase.set(pendingObj.lifeCyclePhase.select_related())
                currentStateObj.userInterface.set(pendingObj.userInterface.select_related())
                currentStateObj.targetGroup.set(pendingObj.targetGroup.select_related())
                currentStateObj.lastUpdate = pendingObj.lastUpdate
                currentStateObj.license = pendingObj.license
                currentStateObj.licenseNotes = pendingObj.licenseNotes
                currentStateObj.furtherInformation = pendingObj.furtherInformation
                currentStateObj.alternatives = pendingObj.alternatives
                currentStateObj.specificApplication.set(pendingObj.specificApplication.select_related())
                currentStateObj.released = pendingObj.released
                currentStateObj.releasedPlanned = pendingObj.releasedPlanned
                currentStateObj.yearOfRelease = pendingObj.yearOfRelease
                currentStateObj.resources = pendingObj.resources
                currentStateObj.developmentState = pendingObj.developmentState
                currentStateObj.programmingLanguages = pendingObj.programmingLanguages
                currentStateObj.frameworksLibraries = pendingObj.frameworksLibraries
                currentStateObj.databaseSystem = pendingObj.databaseSystem
                currentStateObj.scale.set(pendingObj.scale.select_related())
                currentStateObj.technicalStandardsNorms.set(pendingObj.technicalStandardsNorms.select_related())
                currentStateObj.technicalStandardsProtocols.set(pendingObj.technicalStandardsProtocols.select_related())
                currentStateObj.provider = pendingObj.provider
                currentStateObj.userInterfaceNotes = pendingObj.userInterfaceNotes
                currentStateObj.focus.set(pendingObj.focus.select_related())
                currentStateObj.classification.set(pendingObj.classification.select_related())
                currentStateObj.save()
                pendingObj.delete()
            else:
                currentStateObj.__setattr__(
                    nameOfFieldRelatesToTable.name, 
                    pendingObj,
                )
                currentStateObj.save()

                if currentStateRow is not None:
                    self.listOfToBeDeletedObjs.append(currentStateRow)
                for currentTable in list(diffDataStructure.keys()):
                    if "Subproject" in currentTable:
                        parent = currentTable.split(".")[1]
                for currentTable in list(diffDataStructure.keys()):
                    if parent in currentTable.split(".")[0]:
                        deleteSchlagwort = True
                        if parent == "KeywordRegisterFirstReview":
                            pass


    def parseFile(
            self, 
            filename: str,
        ) -> list:
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











