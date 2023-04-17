"""

"""

import os
import pdb
import importlib
import datetime

from django.test import TransactionTestCase
from django.core import management
import yaml

from project_listing.models import Teilprojekt, Enargus
from project_listing.management.commands.data_import import Command, MultipleFKZDatasets

class checkDifferencesInDatabase(TransactionTestCase):
    """
    
    """

    def testLoadingTwoTimesTheSameDataset(self):
        """This method tests what happens, if 2 times the same dataset 
        is loaded into the DB. It loads the .csv file at 
        "testData/enargus_testDatabaseFile.csv" two times in a row,
        and checks each time if only one dataset is present in the 
        datasbe and that its the one, represented by the first dataset
        inside the .csv-file.
        
        """

        fileNameContainingTestData = "testData/enargus_testDatabaseFile.csv"

        dataImportCommand = Command()
        header, data = dataImportCommand.readCSV(fileNameContainingTestData)

        management.call_command('data_import', fileNameContainingTestData)

        # only one Teilprojekt should be present in the test-database:
        self.assertTrue(len(Teilprojekt.objects.all()) == 1)
        
        # check if the dataset was corretly loaded into the DB:
        testDatasetFromDB = Teilprojekt.objects.filter(fkz=data[0][0])[0]

        testDatasetEnargus = testDatasetFromDB.enargus_daten

        self.assertTrue(str(testDatasetEnargus.laufzeitbeginn) == data[0][1])
        self.assertTrue(str(testDatasetEnargus.laufzeitende) == data[0][2])
        self.assertTrue(str(testDatasetEnargus.datenbank) == data[0][3])
        self.assertTrue(str(testDatasetEnargus.thema) == data[0][4])

        # check what happens, if two times the same dataset is loaded:
        management.call_command('data_import', fileNameContainingTestData)

        # still only one dataset should be present in the database:
        self.assertTrue(len(Teilprojekt.objects.all()) == 1)

        # check if the dataset was corretly loaded into the DB:
        testDatasetFromDB = Teilprojekt.objects.filter(fkz=data[0][0])[0]  
        
        testDatasetEnargus = testDatasetFromDB.enargus_daten

        self.assertTrue(str(testDatasetEnargus.laufzeitbeginn) == data[0][1])
        self.assertTrue(str(testDatasetEnargus.laufzeitende) == data[0][2])
        self.assertTrue(str(testDatasetEnargus.datenbank) == data[0][3])
        self.assertTrue(str(testDatasetEnargus.thema) == data[0][4])

    def testSameFKZTwoTimesInCSV(self):
        """This method tests the behaviour of the `data_import` if the same
        FKZ is present multiple times in the .csv-file and every 
        dataset is different.
        """

        csvFileToBeLoaded = "testData/enargus_testMultipleTimesSameDataset.csv"

        self.assertRaises(
            MultipleFKZDatasets, 
            management.call_command('data_import', csvFileToBeLoaded)
        )
    
    def testIfYAMLRepresentsDBState(self) -> None:
        """This method tests if the Database State-Differences, which are 
        specified in the .yaml file, are acutally present in the Database.
        Therefore it loads two .csv files, which include different 
        datasets for the same Förderkennziffer (fkz). This should produce
        a .yaml-file, which shows the differences. Th

        Returns: 
        None
        """

        fileNameContainingTestData = "testData/enargus_testDatabaseFile.csv"
        management.call_command('data_import', fileNameContainingTestData)

        fileNameModifiedTestData = "testData/enargus_testDatabaseFileModified.csv"
        management.call_command('data_import', fileNameModifiedTestData)
        
        fileContents = os.listdir()
        newest = 0
        newestFileName = ""
        for currentFilename in fileContents:
            if ".yaml" in currentFilename:
                fileWithoutExtension = currentFilename[0:-5].replace("-", "")
                if int(fileWithoutExtension) > int(newest):
                    newest = fileWithoutExtension
                    newestFileName = currentFilename
        
        # check, if the timestamp of the newly created file, lies in the last
        # 5 minutes:
        currentTimeStamp = datetime.datetime.now()
        currentTimeInt = str(currentTimeStamp).replace("-", "").replace(":", "").replace(" ", "").split(".")[0]
        
        self.assertTrue(
            int(newest) + 2*60 > int(currentTimeInt), 
            "Newest .YAML-File has an too old Timestamp!",
        )

        listOfDBDifferenceObjs = []

        with open(newestFileName, "r") as file:
            for databaseDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()
                listOfDBDifferenceObjs.append(databaseDifferenceObj)
            
        for databaseDiffObj in listOfDBDifferenceObjs:
            nestedDictContainingDiffs = databaseDiffObj.differencesSortedByTable
            dictMappingToTable = self._getTablesFromDiffDataStructure(
                nestedDictContainingDiffs
            ) 
            self._checkIfDifferencesFromYAMLAreInDB(
                nestedDictContainingDiffs, 
                dictMappingToTable
            )


    def _checkIfDifferencesFromYAMLAreInDB(
            self, 
            nestedDictContainingDiffs: dict, 
            dictMappingToTable: list,
    ) -> None:
        """This method tests, if the two Database-states descried in the
        .yaml file are acutally present in the Database.

        nestedDictContainingDiffs:  dict
            Nested Dictionary containing the current DB-state and the 
            CSV-state.
        dictMappingToTable: dict
            Dictionary, which does a mapping between the entries of  
            nestedDictContainingDiffs and the actual Modelnames.
        
        Returns:
        None
        """
        allModels = importlib.import_module("project_listing.models")

        for tableDictKey in list(nestedDictContainingDiffs.keys()):
            
            tableName = dictMappingToTable[tableDictKey]
            dictOfDifferences = nestedDictContainingDiffs[tableDictKey]
            currentDBStateInTable = dictOfDifferences["currentState"]
            CSVState = dictOfDifferences["pendingState"]

            # check if both states are present in the DB, 
            # like they are shown in the .yaml-file:
            currentTableModel = allModels.__getattribute__(tableName) 
            self.assertTrue(
                len(currentTableModel.objects.filter(**currentDBStateInTable)) == 1
            )
            self.assertTrue(
                len(currentTableModel.objects.filter(**CSVState)) == 1
            )


    def _getTablesFromDiffDataStructure(
            self, 
            nestedDictContainingDiffs: dict,
    ) -> dict:
        """This method is a helper-function to get the Tablenames from the 
        Database-Difference-Object, in which differences between the current 
        state and the .csv-state are present.
        
        nestedDictContainingDiffs:  dict
            Nested Dictionary containing as keys the tables, in which 
            Differences are present, and as values another Dictionary, 
            which contains as keys the field-names and as values the 
            values, which are present in the DB-state respectivly in 
            the .csv-state.
        
        Returns:
        returnDict:   dict
            List of tables of type string, in which the differences are 
            present.    
        """
        
        returnDict = {}
        for currentTableKey in list(nestedDictContainingDiffs.keys()):
            tableName = currentTableKey.split(".")[1]
            tableName = tableName[0].upper() + tableName[1:]

            returnDict[currentTableKey] = tableName


        return returnDict