import ast
# import pdb
import importlib

from project_listing.models import Subproject
from tools_over.models import Tools

import yaml
import numpy as np

class DatabaseDifference(yaml.YAMLObject):
    """Class of one Database Difference

    This class holds the Differences, which appear, when loading a 
    .csv-file and a Förderkennzeichen-Dataset is present in the .csv-
    file and the Database and the two Datasets differ. The differences
    are sorted by Database-table and safed inside of 
    `differencesSortedByTable`. With the `addTable`- and the 
    `addDifference`-methods, the `differencesSortedByTable` can be filled.
    Furthermore the class holds methods for writing the object to a file
    (`writeToYAML`-method) and postprocess the datastructure after read 
    it back in from file (`postprocessAfterReadIn`-method).

    Attributes:
    identifer:  dict
        Key-Value-Pair, which represents the column-name and value of
        the dataset, where the conflict appeared. Typically it will have
        the form {fkz: "GE64775"}.
    verbundbezeichnung: str
        Short describtion, whcih helps to understand, which fkz is ment.
    differencesSortedByTable:   dict
        nested-Dictionary, containing all differences between Database-
        state (currentState) and CSV-state (pendingState).
    keepCurrentState: bool
        Boolean, specifies, if the Database-State (currentState) is kept.
    keepCurrentState: bool
        Boolean, specifies, if the csv-State (pendingState) is kept.
    
    """

    def __init__(
            self, 
            identifer: dict, 
            verbundbezeichnung: str,
        ):
        """Constructor of DatabaseDifference-class

            identifier: dict
                Dictionary, containing Förderkennzeichen and the Thema.
        """
        self.identifer = identifer
        self.verbundbezeichnung = verbundbezeichnung
        self.differencesSortedByTable = {}
        self.keepCurrentState = None
        self.keepPendingState = None

    def addTable(self, tableName) -> None:
        """Creates a new Table-Entry, in which the Differences are stored
        
        tableName:  str
            Name of the Table, in which a difference is detected.
        """
        self.differencesSortedByTable[tableName] = {}
        self.differencesSortedByTable[tableName]["currentState"] = {}
        self.differencesSortedByTable[tableName]["pendingState"] = {}

    def addDifference(
            self, 
            tableName, 
            currentState, 
            pendingState,
        ) -> None:
        """Adds a Difference to a table, which is already present in 
        the data-strucutre.

        tableName:  str
            Name of the table, which is already present in the 
            DifferenceSortedByTable Attribute-Dict.
        
        currentState: dict
            Dictionary containing as key the name of the fieldname and
            as value the value of the field. Of the current State of 
            the Database.tupleOfDjangoDBObjsme and as value the value 
            of the field. Of the pending State of the Database.
        
        """
        self.differencesSortedByTable[tableName]["currentState"].update(
            currentState,
        )
        self.differencesSortedByTable[tableName]["pendingState"].update(
            pendingState,
        )
    
    def checkIfUserInputIsValid(self) -> bool:
        """Checks if the Modification of the .yaml-File of the user is
        present and consistent.
        """
        if self.keepCurrentState is None or self.keepPendingState is None:
             return False
        else:
             if (bool(self.keepCurrentState) == True 
                 and bool(self.keepPendingState) == False):
                  return True
             elif (bool(self.keepCurrentState) == False 
                   and bool(self.keepPendingState) == True):
                  return True
             else:
                  return False
    

    def _findModelNameForKey(self, allModels, curentTableFromKey):
        """
        
        """
        currNameWithUpperLetter = curentTableFromKey[0].upper() + curentTableFromKey[1:]
        for model in dir(allModels):
            if currNameWithUpperLetter in model or curentTableFromKey in model:
                return model
        

    def checkIfConflictIsConsistentWithDatabase(self):
        """Checks if, the conflict is consistent with the current state
        of the database. This should secure from error, which are 
        introduced by execute the same database-conflict file multiple 
        times.

        """
        rootTableName = self.getStartingPoint()
        allModels = importlib.import_module("project_listing.models")
        allModelsTools = importlib.import_module("tools_over.models")
        try:
            classNameOfTable = getattr(allModels.__getattribute__(rootTableName.split(".")[0]), rootTableName.split(".")[1]).field.related_model
        except:
            # breakpoint()
            # classNameOfTable = getattr(allModelsTools.__getattribute__(rootTableName.split(".")[0]), rootTableName.split(".")[1]).field.related_model
            classNameOfTable = allModelsTools.__getattribute__(rootTableName.split(".")[0])
        parentTableName = rootTableName.split(".")[0]
        dictofRootTable = list(
            self.differencesSortedByTable[rootTableName]["currentState"].keys()
        )
        for rootTableFieldName in dictofRootTable:
             
             if "_id" in rootTableFieldName or rootTableFieldName == "id":
                if self.differencesSortedByTable[rootTableName]\
                    ["currentState"][rootTableFieldName] is not None:
                    
                    idOfConflictingCurrentObj = int(self.differencesSortedByTable[rootTableName]["currentState"][rootTableFieldName])
                else:
                    idOfConflictingCurrentObj = None
                idOfConflictingPendingObj = int(
                    self.differencesSortedByTable[rootTableName]\
                        ["pendingState"][rootTableFieldName]
                )
                currentStateInRootTable = globals()[parentTableName].objects.filter(**{list(self.identifer.keys())[0]: self.identifer[list(self.identifer.keys())[0]]})
                querySetForPendingObj = classNameOfTable\
                .objects.filter(
                    **{rootTableFieldName: idOfConflictingPendingObj}
                )
                querySetForCurrentObj = globals()[parentTableName].objects.filter(
                    **self.identifer,
                )

                if (len(querySetForPendingObj) > 0 
                    and (len(querySetForCurrentObj) > 0 or idOfConflictingCurrentObj is None)
                    and len(currentStateInRootTable) > 0):
                    # breakpoint()
                    try:
                        nameOfFieldRelatesToTable = self.findFieldNameRelatingToForeignTable(globals()[parentTableName], classNameOfTable)
                    except:
                        nameOfFieldRelatesToTable = None
                    try:
                        currentStateRowObj = currentStateInRootTable[0].__getattribute__(
                            nameOfFieldRelatesToTable.name,
                        )
                    except:
                        currentStateRowObj = currentStateInRootTable[0]
                    return (
                        self.keepCurrentState, 
                        querySetForCurrentObj[0], 
                        querySetForPendingObj[0], 
                        currentStateRowObj, 
                        nameOfFieldRelatesToTable, 
                        currentStateInRootTable[0],
                    )                
        return None

    def getStartingPoint(self) -> str:
        """Returns a string with the starting point in the Dictionary
        of the Tables. The starting point is the table in which the 
        objects are located, which produces the conflict. E.g. in case
        of enargus-data it is the Enargus-Table. 
        
        Returns:
        rootTableName:  str
            Returns the root-table name, where the database-conflict
            appeared. This is at the moment the "Teilprojekt"-table.
            So it is explictly searched for that string.
        """
        for tableName in list(self.differencesSortedByTable.keys()):
            if "Subproject" in tableName:
                rootTableName = tableName
                break
        try:
            return rootTableName
        except:
            for tableName in list(self.differencesSortedByTable.keys()):
                if "Tools" in tableName:
                    rootTableName = tableName
                    break            
            return rootTableName
            # pdb.set_trace()

    def findFieldNameRelatingToForeignTable(self, parentTable, tableObj):
        """Finds the 
        
        """
        listOfFields = parentTable._meta.get_fields()

        for field in listOfFields:
            if field.is_relation:
                if field.related_model == tableObj:
                    return field                

    def postprocessAfterReadIn(self) -> None:
        """After read-in of the .yaml-file, the lowest-level dict 
        is represented by a string and needs to be parsed to a 
        dict. Furthermore trailing whitespaces need to be deleted 
        from the values.
        
        TODO:  In multiple methods a iteration through the nested dict is done.
        This is not DRY! Only one method should do the iteration.
        """
        for tableNameKey in self.differencesSortedByTable:
            self.differencesSortedByTable[tableNameKey]["currentState"] = ast.literal_eval(
                self.differencesSortedByTable[tableNameKey]["currentState"]
            )
            self.differencesSortedByTable[tableNameKey]["pendingState"] = ast.literal_eval(
                self.differencesSortedByTable[tableNameKey]["pendingState"]
            )

            for diffAttribute in list(
                self.differencesSortedByTable[tableNameKey]["currentState"].keys()
            ):
                if isinstance(
                    self.differencesSortedByTable[tableNameKey]["currentState"][diffAttribute], 
                    str,
                ):
                    self.differencesSortedByTable[tableNameKey]["currentState"]\
                        [diffAttribute] = self.differencesSortedByTable\
                            [tableNameKey]["currentState"][diffAttribute].rstrip()
                self.differencesSortedByTable[tableNameKey]["pendingState"]\
                    [diffAttribute] = self.differencesSortedByTable\
                        [tableNameKey]["pendingState"][diffAttribute].rstrip()

                if self.differencesSortedByTable[tableNameKey]["currentState"]\
                        [diffAttribute] == "None":
                    self.differencesSortedByTable[tableNameKey]["currentState"]\
                        [diffAttribute] = None





    def writeToYAML(self, yamlFileName):
        """Prepares the Attributes to be written out to yaml. 
        It removes all entries of the self.differencesSortedByTable dict, so that only 
        Table Differences are shown.
        
        yamlFileName:   str
            file name of the yaml-file, in which the Database Difference Object is 
            serialized to.
        """
        keysToBeDeleted = []
        for tableNameKey in self.differencesSortedByTable:
            if len(self.differencesSortedByTable[tableNameKey]["currentState"].keys()) == 0:
                 keysToBeDeleted.append(tableNameKey)
            
            for currentDiffAttribute in list(
                self.differencesSortedByTable[tableNameKey]["currentState"].keys()
            ):
                
                valueCurrent = self.differencesSortedByTable[tableNameKey]\
                    ["currentState"][currentDiffAttribute]
                
                valuePending = self.differencesSortedByTable[tableNameKey]\
                    ["pendingState"][currentDiffAttribute]

                if valueCurrent is None:
                    lengthOfCurrent = 4
                    self.differencesSortedByTable[tableNameKey]["currentState"]\
                        [currentDiffAttribute] = "None"
                else:
                    lengthOfCurrent = len(valueCurrent)
                
                lengthOfStr = np.array([lengthOfCurrent, len(valuePending)])
                posOfMaxLengthStr = np.argmin(lengthOfStr)
                numberOfCharacterDifference = np.abs(lengthOfStr[0] - lengthOfStr[1])
                if posOfMaxLengthStr == 0:
                   self.differencesSortedByTable[tableNameKey]["currentState"]\
                    [currentDiffAttribute] += numberOfCharacterDifference * " "
                else:
                    self.differencesSortedByTable[tableNameKey]["pendingState"]\
                        [currentDiffAttribute] += numberOfCharacterDifference * " "                
            self.differencesSortedByTable[tableNameKey]["currentState"] = str(
                self.differencesSortedByTable[tableNameKey]["currentState"]
            )
            self.differencesSortedByTable[tableNameKey]["pendingState"] = str(
                self.differencesSortedByTable[tableNameKey]["pendingState"]
            )
        
        for keyToBeDeleted in keysToBeDeleted:
                 self.differencesSortedByTable.pop(keyToBeDeleted)
        with open(yamlFileName, "a") as stream:
            yaml.dump(
                self, 
                stream, 
                explicit_start=True, 
                explicit_end=True, 
                allow_unicode=True,
                width=float("inf"),
            )

    
