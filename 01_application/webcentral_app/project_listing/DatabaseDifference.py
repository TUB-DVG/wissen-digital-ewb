import pdb

from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from schlagwoerter.models import *
import yaml

class DatabaseDifference:
    """This class holds data for one database-Difference
    
    """

    def __init__(self, identifer: dict, thema: str):
        """Constructor of DatabaseDifference-class

            identifier: dict
                Dictionary, containing Förderkennzeichen and the Thema.
        """
        self.identifer = identifer
        self.thema = thema
        self.differencesSortedByTable = {}
        self.keepCurrentState = None
        self.keepPendingState = None
    
    # def __repr__(self) -> str:
    #     return f"Conflict found for: {self.identifer} \n{self.differencesSortedByTable}"
    
    def addTable(self, tableName) -> None:
        """Creates a new Table-Entry, in which the Differences are stored
        
        tableName:  str
            Name of the Table, in which a difference is detected.
        """
        self.differencesSortedByTable[tableName] = {}
        self.differencesSortedByTable[tableName]["currentState"] = {}
        self.differencesSortedByTable[tableName]["pendingState"] = {}

    def addDifference(self, tableName, currentState, pendingState) -> None:
        """Adds a Difference to a table, which is already present in the data-strucutre.

        tableName:  str
            Name of the table, which is already present in the DifferenceSortedByTable Attribute-Dict.
        
        currentState: dict
            Dictionary containing as key the name of the fieldname and as value the value of the field. 
            Of the current State of the Database.tupleOfDjangoDBObjsme and as value the value of the field. 
            Of the pending State of the Database.
        
        """
        self.differencesSortedByTable[tableName]["currentState"].update(currentState)
        self.differencesSortedByTable[tableName]["pendingState"].update(pendingState)
    
    def checkIfUserInputIsValid(self) -> bool:
        """Checks if the Modification of the .yaml-File of the user is present and consistent.
        """
        if self.keepCurrentState is None or self.keepPendingState is None:
             return False
        else:
             if bool(self.keepCurrentState) == True and bool(self.keepPendingState) == False:
                  return True
             elif bool(self.keepCurrentState) == False and bool(self.keepPendingState) == True:
                  return True
             else:
                  return False
    
    def checkIfConflictIsConsistentWithDatabase(self):
        """Checks if, the conflict is consistent with the current state of the database. 
        This should secure from error, which are introduced by execute the same database-conflict file 
        multiple times.

        """
        # find the root-table:

        rootTableName = self.getStartingPoint()
        
        tableWhereConflictingObjsAreLocated = rootTableName.split(".")[1]
        parentTableName = rootTableName.split(".")[0]
        dictofRootTable = list(self.differencesSortedByTable[rootTableName]["currentState"].keys())
        for rootTableFieldName in dictofRootTable:
             if "_id" in rootTableFieldName:
                idOfConflictingCurrentObj = int(self.differencesSortedByTable[rootTableName]["currentState"][rootTableFieldName])
                idOfConflictingPendingObj = int(self.differencesSortedByTable[rootTableName]["pendingState"][rootTableFieldName])
                #pdb.set_trace()
                currentStateInRootTable = globals()[parentTableName].objects.filter(**{list(self.identifer.keys())[0]: self.identifer[list(self.identifer.keys())[0]]})
                querySetForPendingObj = globals()[tableWhereConflictingObjsAreLocated].objects.filter(**{rootTableFieldName: idOfConflictingPendingObj})
                querySetForCurrentObj = globals()[tableWhereConflictingObjsAreLocated].objects.filter(**{rootTableFieldName: idOfConflictingCurrentObj})
                if len(querySetForPendingObj) > 0 and len(querySetForCurrentObj) > 0 and len(currentStateInRootTable) > 0:
                    #pdb.set_trace()
                    nameOfFieldRelatesToTable = self.findFieldNameRelatingToForeignTable(globals()[parentTableName], globals()[tableWhereConflictingObjsAreLocated])
                    
                    currentStateRowObj = currentStateInRootTable[0].__getattribute__(nameOfFieldRelatesToTable.name)
                    return (self.keepCurrentState, querySetForCurrentObj[0], querySetForPendingObj[0], currentStateRowObj, nameOfFieldRelatesToTable, currentStateInRootTable[0])
                #querySetForCurrentObj = Teilprojekt.objects.filter(**{rootTableFieldName: idOfConflictingCurrentObj, "fkz": self.identifer["fkz"]})
                
        return None
    

    def getStartingPoint(self) -> str:
        """Returns a string with the starting point in the Dictionary of the Tables. The starting point is the table in which the objects are located,
        which produces the conflict. E.g. in case of enargus-data it is the Enargus-Table. 
        
        """
        for tableName in list(self.differencesSortedByTable.keys()):
            if "Teilprojekt" in tableName:
                rootTableName = tableName
                break
        
        return rootTableName

    def findFieldNameRelatingToForeignTable(self, parentTable, tableObj):
        """
        
        """
        listOfFields = parentTable._meta.get_fields()

        for field in listOfFields:
            if field.is_relation:
                if field.related_model == tableObj:
                    return field                

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
        
        for keyToBeDeleted in keysToBeDeleted:
                 self.differencesSortedByTable.pop(keyToBeDeleted)
        with open(yamlFileName, "a") as stream:
            yaml.dump(self, stream, explicit_start=True, explicit_end=True)
    
