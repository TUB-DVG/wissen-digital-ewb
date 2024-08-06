import difflib

import pandas as pd
from django.db.models import Model

class DataImport:
    def __init__(self, path_to_data_file):
        """Constructor of the Base-DataImport-class.

        """
        self.path_to_file = path_to_data_file

    def importList(self, header, data) -> None:
        """Iterate over the list of databases-tuples and call 
        `getOrCreate()` on each of them.

        header: list
            list of heaser strings from imported file.
        data:   list
            list of database tuples.

        returns:
            None
        """

        for row in data:
            self.getOrCreate(row, header, data)

    def load(self):
        """load csv/excel-file

        """
        
        # if its a excel file, check if 2 sheets are present:


        if self.path_to_file.endswith(".csv"):
            header, data = self.readCSV(pathFile)
        elif self.path_to_file.endswith(".xlsx"):
            header, data = self.readExcel()
            return header, data
        else:
            raise CommandError(
                "Invalid file format. Please provide a .csv or .xlsx file.")

    def readExcel(
            self,
        ) -> tuple:
        """This method reads the excel-file, and loads the content into
        the two variables header and data.

        Parameters:
        path:   str

        Returns:
        header: list
            List of headers from the excel-file.
        data:   list
            list, containing the rows from the excel-file.
        """
        try:
            dfGermanEnglish = pd.read_excel(self.path_to_file, sheet_name=["German", "English"])
            germanEnglish = True
        except:
            df = pd.read_excel(self.path_to_file)
            germanEnglish = False
        
        if germanEnglish:
            if len(dfGermanEnglish["English"] == len(dfGermanEnglish["German"])):
                for index, german_column in enumerate(dfGermanEnglish["German"].columns):
                    if german_column == dfGermanEnglish["English"].columns[index]:
                        dfGermanEnglish["English"] = dfGermanEnglish["English"].rename(columns={dfGermanEnglish["English"].columns[index]: dfGermanEnglish["English"].columns[index] + "__en"})
                df_concatenated = pd.concat([dfGermanEnglish["English"], dfGermanEnglish["German"]], axis=1, ignore_index=True)
                df_concatenated.columns = list(dfGermanEnglish["English"].columns) + list(dfGermanEnglish["German"].columns)
            else:
                print("German and english sheets dont have the same number of rows. Only using the german elements and skipping the translation.")
                df_concatenated = dfGermanEnglish["German"]

        else:
            df_concatenated = df

        df = df_concatenated.fillna("")
        header = list(df.columns)
        data = df.values.tolist()
        # breakpoint()
        return header, data

    def _correctReadInValue(self, readInString):
        """Correct the read in value from the csv-file.

        This method corrects the read in value from the csv-file,
        by removing whitespaces at the beginning and end of the
        string.

        readInString:   str
            String, which represents the read in value from the csv-file.
        """

        if isinstance(readInString, float) and math.isnan(readInString):
            return ""
        if readInString == "":
            return ""
        splitStringToSeeIfList = readInString.split(",")
        splitStringToSeeIfList = [
            item for item in splitStringToSeeIfList if item
        ]
        if len(splitStringToSeeIfList) > 0:
            for index, listElement in enumerate(splitStringToSeeIfList):
                if listElement[0] == " ":
                    listElement = listElement[1:]
                if listElement[-1] == " ":
                    listElement = listElement[:-1]
                splitStringToSeeIfList[index] = listElement
            return splitStringToSeeIfList
        else:
            if readInString[0] == " ":
                readInString = readInString[1:]
            if readInString[-1] == " ":
                readInString = readInString[:-1]
            return readInString

    def _selectNearestMatch(self, categoryString: str,
                            djangoModel: Model) -> str:
        """Return closest match for categoryString in djangoModel

        This method returns the closest match for `categoryString` in `djangoModel`
        by using the difflib.get_close_matches-function. Thereby the cutoff is set
        to 80 %. That means if the closest match is below 80 %, an error message
        is printed and an empty string is returned.

        categoryStr:    str
            String, which represents the category, which should be matched.
        djangoModel:    Model
            Django-Model, which represents the table, in which the closest match is searched.

        Returns:
        str
            String, which represents the closest match for `categoryString` in `djangoModel`.

        """

        # get names of all djangoModel-objects
        if djangoModel.__name__ == "Subproject":
            attributeNameInModel = "referenceNumber_id"
        elif djangoModel.__name__ == "Norm":
            attributeNameInModel = "title"
        else:
            attributeNameInModel = (djangoModel.__name__[0].lower() +
                                    djangoModel.__name__[1:])
        allNames = [
            x.__getattribute__(attributeNameInModel)
            for x in djangoModel.objects.all()
        ]

        # get the closest match
        listOfClosestMatches = difflib.get_close_matches(categoryString,
                                                         allNames,
                                                         n=1,
                                                         cutoff=0.8)
        if len(listOfClosestMatches) > 0:
            return listOfClosestMatches[0]
        else:
            if (djangoModel.__name__ != "Subproject"
                    and djangoModel.__name__ != "Norm"):
                try:
                    newlyCreatedRow = djangoModel.objects.create(
                        **{attributeNameInModel: categoryString})
                except:
                    breakpoint()
                print(
                    f"No nearest match for {categoryString} in {djangoModel} was found. {categoryString} is created inside of {djangoModel}",
                )
                return newlyCreatedRow.__getattribute__(attributeNameInModel)

    def _iterateThroughListOfStrings(self, listOfStrings: list,
                                     djangoModel: Model):
        """ """
        listOfModifiedStrings = []
        for curretnCategoryString in listOfStrings:
            modifiedStr = self._selectNearestMatch(curretnCategoryString,
                                                   djangoModel)
            listOfModifiedStrings.append(modifiedStr)
        return listOfModifiedStrings

    def _processListInput(self, inputStr, separator=";"):
        """Process a cell, which includes a list of elements"""
        returnList = []
        for element in inputStr.split(separator):
            if not self._checkIfOnlyContainsSpaces(element):
                returnList.append(element)

        return returnList

    def _checkIfOnlyContainsSpaces(self, inputStr):
        """Check if the inputStr only contains whitespaces.

        This method checks if the inputStr only contains whitespaces.
        If this is the case, the method returns True, otherwise False.

        Parameters:
        inputStr:   str
            String, which should be checked, if it only contains whitespaces.

        Returns:
        bool
            True, if the inputStr only contains whitespaces, otherwise False.
        """
        return all(x.isspace() for x in inputStr)
