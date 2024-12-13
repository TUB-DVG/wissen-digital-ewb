"""Gneral Dataimport Classholding methods,which are used by the app specific
data_import classes.

"""

import difflib
import csv
import math

import pandas as pd
from django.core.management.base import CommandError
from django.db.models import Model
from django.db import models
from django.apps import apps
from django.db.models import (
    ForeignKey,
    OneToOneField,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
)
from django.db.models.query import QuerySet
from django.core.serializers import serialize

from common.models import DbDiff, Literature
from protocols.models import Protocol
from publications.models import Type, Publication
from tools_over.models import Tools
from TechnicalStandards.models import Norm
from Datasets.models import Dataset

# from .serializers import BackReferenceSerializer


class DataImport:
    """Definition of the general DataImport class"""

    def __init__(self, path_to_data_file):
        """Constructor of the Base-DataImport-class."""
        self.path_to_file = path_to_data_file
        self.diffStr = ""
        self.diffStrDict = {}
        # register_serializer("custom_json", BackReferenceSerializer)

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
        """load csv/excel-file"""
        # if its a excel file, check if 2 sheets are present:
        if self.path_to_file.endswith(".csv"):
            header, data = self.readCSV()
            return header, data
        if self.path_to_file.endswith(".xlsx"):
            header, data = self.readExcel()
            return header, data
        raise CommandError(
            "Invalid file format. Please provide a .csv or .xlsx file."
        )

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
        df = None
        try:
            dfGermanEnglish = pd.read_excel(
                self.path_to_file, sheet_name=["German", "English"]
            )
            germanEnglish = True
        except ValueError:
            df = pd.read_excel(self.path_to_file)
            germanEnglish = False
        if germanEnglish:
            if len(
                dfGermanEnglish["English"] == len(dfGermanEnglish["German"])
            ):
                for index, german_column in enumerate(
                    dfGermanEnglish["German"].columns
                ):
                    if (
                        german_column
                        == dfGermanEnglish["English"].columns[index]
                    ):
                        dfGermanEnglish["English"] = dfGermanEnglish[
                            "English"
                        ].rename(
                            columns={
                                dfGermanEnglish["English"]
                                .columns[index]: dfGermanEnglish["English"]
                                .columns[index]
                                + "__en"
                            }
                        )
                df_concatenated = pd.concat(
                    [dfGermanEnglish["English"], dfGermanEnglish["German"]],
                    axis=1,
                    ignore_index=True,
                )
                df_concatenated.columns = list(
                    dfGermanEnglish["English"].columns
                ) + list(dfGermanEnglish["German"].columns)
            else:
                print(
                    """German and english sheets dont have the same number of
                    rows. Only using the german elements and skipping the
                    translation."""
                )
                df_concatenated = dfGermanEnglish["German"]

        else:
            df_concatenated = df

        df = df_concatenated.fillna("")
        header = list(df.columns)
        data = df.values.tolist()
        return header, data

    def readCSV(self):
        """Read the provided csv-file and return the header and the data as
        2 lists.
        """
        with open(self.path_to_file, "r") as fh:
            csvReader = csv.reader(fh, delimiter=";")
            header = next(csvReader)
            # data = [row for row in csvReader]
            data = list(csvReader)

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
        if readInString[0] == " ":
            readInString = readInString[1:]
        if readInString[-1] == " ":
            readInString = readInString[:-1]
        return readInString

    def _selectNearestMatch(
        self, categoryString: str, djangoModel: Model
    ) -> str:
        """Return closest match for categoryString in djangoModel

        This method returns the closest match for `categoryString` in
        `djangoModel` by using the difflib.get_close_matcheGs-function.
        Thereby the cutoff is set to 80 %. That means if the closest match
        is below 80 %, an error message is printed and an empty string is
        returned.

        categoryStr:    str
            String, which represents the category, which should be matched.
        djangoModel:    Model
            Django-Model, which represents the table, in which the closest
            match is searched.

        Returns:
        str
            String, which represents the closest match for `categoryString`
            in `djangoModel`.

        """

        # get names of all djangoModel-objects
        if djangoModel.__name__ == "Subproject":
            attributeNameInModel = "referenceNumber_id"
            return djangoModel.objects.get_or_create(
                referenceNumber_id=categoryString
            )[0]

        elif djangoModel.__name__ == "Norm":
            attributeNameInModel = "title"
        elif djangoModel.__name__ == "Protocol":
            attributeNameInModel = "name"
        else:
            attributeNameInModel = (
                djangoModel.__name__[0].lower() + djangoModel.__name__[1:]
            )
        allNames = [
            getattr(x, attributeNameInModel) for x in djangoModel.objects.all()
        ]
        allNames = [element for element in allNames if element is not None]
        listOfClosestMatches = difflib.get_close_matches(
            categoryString, allNames, n=1, cutoff=0.8
        )
        if len(listOfClosestMatches) > 0:
            return listOfClosestMatches[0]

        if djangoModel == Protocol:
            newlyCreatedRow = djangoModel.objects.create(
                **{"name": categoryString}
            )
            return getattr(newlyCreatedRow, "name")
        else:
            newlyCreatedRow = djangoModel.objects.create(
                **{attributeNameInModel: categoryString}
            )
        print(
            f"""No nearest match for {categoryString} in {djangoModel}
            was found. {categoryString} is created inside of
            {djangoModel}""",
        )
        return getattr(newlyCreatedRow, attributeNameInModel)

    def _iterateThroughListOfStrings(
        self, listOfStrings: list, djangoModel: Model
    ):
        """ """
        listOfModifiedStrings = []
        for curretnCategoryString in listOfStrings:
            modifiedStr = self._selectNearestMatch(
                curretnCategoryString, djangoModel
            )
            listOfModifiedStrings.append(modifiedStr)
        return listOfModifiedStrings

    def getM2MelementsQueryset(
        self, listOfStrings: list, djangoModel: Model
    ) -> list:
        """Get queryset of m2m-elements, which corresponds to the string elements of `listOfStrings`

        Arguments:
        djangoModel: models.Model
            Django model ORM class of a ManyToManyField
        listOfStrings: list
            List of strings, whereby each string represents a ManyToMany-object of `djangoModel`

        Returns:
            queryset containing the `djangoModel`-objects
        """
        if djangoModel._meta.model_name == "subproject":
            attrWithDe = "referenceNumber_id"
        elif djangoModel._meta.model_name == "license":
            listOfM2Mobjs = []
            for objString in listOfStrings:
                if isinstance(objString, tuple):
                    listOfM2Mobjs.append(
                        djangoModel.objects.get_or_create(
                            license=objString[0],
                            openSourceStatus=objString[1],
                            licensingFeeRequirement=objString[2],
                            openSourceStatus_en=objString[3],
                            licensingFeeRequirement_en=objString[4],
                        )[0]
                    )
                else:
                    listOfM2Mobjs.append(
                        djangoModel.objects.get_or_create(
                            license=objString,
                        )[0]
                    )
            return listOfM2Mobjs
        elif djangoModel._meta.model_name == "type":
            return djangoModel.objects.get_or_create(
                type=listOfStrings[0],
            )[0]
        else:
            attrNamesOfModel = [
                attr.name for attr in djangoModel._meta.get_fields()
            ]
            attrWithDe = next(
                (attr for attr in attrNamesOfModel if "_de" in attr), None
            )
        listOfM2Mobjs = []
        for objString in listOfStrings:
            listOfM2Mobjs.append(
                djangoModel.objects.get_or_create(**{attrWithDe: objString})[0]
            )
        return listOfM2Mobjs

    def _processListInput(self, inputStr, separator=";"):
        """Process a cell, which includes a list of elements and separate the string by the `separator` and return a list"""
        returnList = []
        for element in inputStr.split(separator):
            if not self._checkIfOnlyContainsSpaces(element):
                returnList.append(element)

        return returnList

    def _buildLiteratureIdentifier(self, literatureElement: str) -> str:
        """build a identifer of the litrature element, which can be used
        in the HTML to point from the literature reference to the literature
        list on the end of the page.

        """

        # find the first 3 names and seperate them with a underscore:
        splitBySpaces = literatureElement.split(" ")
        identifer = ""
        for number in range(3):
            identifer += splitBySpaces[number] + "_"

        # find the year, which is written in brackets:
        year = literatureElement.split("(")[1].split(")")[0]

        return identifer + year

    def _importLiterature(self, literatureElements: str):
        """Import literature elements from csv/excel into `Literature`-
        model.

        """
        literatureList = self._processListInput(literatureElements, ";;")
        literatureObjsList = []
        for literature in literatureList:
            if literature.startswith("<sup"):
                litIdentifier = ""
            else:
                litIdentifier = self._buildLiteratureIdentifier(literature)
            objCreated, _ = Literature.objects.get_or_create(
                literature=literature,
                linkName=litIdentifier,
            )
            literatureObjsList.append(objCreated)

        return literatureObjsList

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

    def _importEnglishTranslation(self, obj, header, row, mapping: dict):
        """ """
        modelObj = apps.get_model(self.DJANGO_APP, self.DJANGO_MODEL)
        for mappingKey in mapping.keys():
            englishModelAttr = mapping[mappingKey]
            attrName = englishModelAttr.replace("_en", "")
            modelAttr = modelObj._meta.get_field(attrName)
            headerAttrName = mappingKey.replace("__en", "")

            if isinstance(modelAttr, models.ManyToManyField):
                obj = self._importEnglishManyToManyRel(
                    obj, header, row, headerAttrName, attrName
                )
            elif isinstance(modelAttr, models.ForeignKey):
                obj = self._importEnglishForeignKeyRel(
                    obj, header, row, headerAttrName, attrName
                )
            else:
                obj = self._importEnglishAttr(
                    obj, header, row, headerAttrName, attrName
                )

        obj.save()
        return obj

    def _importEnglishForeignKeyRel(
        self, ormObj, header, row, headerExcel, dbAttr
    ):
        """Import a english translation for a attribute, which is a ForeignKey-
        Relation"""
        foreignElement = getattr(ormObj, dbAttr)
        englishTranslation = row[header.index(headerExcel + "__en")]
        if getattr(foreignElement, dbAttr + "_en") is None:
            setattr(foreignElement, dbAttr + "_en", englishTranslation)
            foreignElement.save()
        return ormObj

    def _importEnglishManyToManyRel(
        self, ormObj, header, row, headerExcel, dbAttr
    ):
        """ """
        germanManyToManyList = self._processListInput(
            row[header.index(headerExcel)], ";;"
        )

        englishManyToManyList = self._processListInput(
            row[header.index(f"{headerExcel}__en")], ";;"
        )
        elementsForAttr = getattr(ormObj, dbAttr).all()

        for ormRelObj in elementsForAttr:
            for indexInGerList, germanManyToManyElement in enumerate(
                germanManyToManyList
            ):
                if germanManyToManyElement in str(ormRelObj):
                    if getattr(ormRelObj, f"{dbAttr}_en") is None:
                        if englishManyToManyList[indexInGerList] is None:
                            englishManyToManyList[indexInGerList] = ""
                        setattr(
                            ormRelObj,
                            f"{dbAttr}_en",
                            englishManyToManyList[indexInGerList],
                        )
                        ormRelObj.save()
        return ormObj

    def _importEnglishAttr(self, ormObj, header, row, headerExcel, dbAttr):
        """ """
        englishTranslation = row[header.index(f"{headerExcel}__en")]
        if englishTranslation is None:
            englishTranslation = ""
        setattr(ormObj, f"{dbAttr}_en", englishTranslation)

        return ormObj

    def _englishHeadersPresent(self, header: list) -> bool:
        """Check if english translation headers are present in the
        list of headers. If yes, then return `True` otherwise `False`

        """
        for headerItem in header:
            if "__en" in headerItem:
                return True

        return False

    def _checkIfItemExistsInDB(self, itemName: str, attrName: str) -> tuple:
        """Check if `djangoModel` holds a item with the name `itemName`"""
        itemsWithName = self.DJANGO_MODEL_OBJ.objects.filter(
            **{attrName: itemName}
        )
        if len(itemsWithName) > 0:
            return itemsWithName[0].id, itemsWithName[0]

    def _compareDjangoOrmObj(self, modelType, oldObj, newObj):
        """Compares 2 django orm objects of same model-type and creates a diff
        str."""

        diffStrModelName = str(modelType) + ":\n"
        diffStr = ""
        fields = modelType._meta.get_fields()

        for field in fields:

            if not isinstance(
                field,
                (
                    ForeignKey,
                    OneToOneField,
                    ManyToManyField,
                    ManyToOneRel,
                    ManyToManyRel,
                ),
            ):
                oldValue = getattr(oldObj, field.name)
                newValue = getattr(newObj, field.name)
                if oldValue != newValue:
                    if isinstance(oldValue, str):

                        oldValueWithoutNewLine = oldValue.replace("\n", "<br>")
                        if isinstance(newValue, str):
                            newValueWithoutNewLine = newValue.replace(
                                "\n", "<br>"
                            )
                    else:
                        oldValueWithoutNewLine = oldValue
                        newValueWithoutNewLine = newValue
                    diffStr += f"""   {field.name}: {oldValueWithoutNewLine} ->
                    {newValueWithoutNewLine}\n"""

            elif isinstance(field, ForeignKey):
                oldValueReference = getattr(oldObj, field.name)
                oldValue = getattr(
                    oldValueReference, field.foreign_related_fields[0].name
                )

                newValueReference = getattr(newObj, field.name)
                newValue = getattr(
                    newValueReference, field.foreign_related_fields[0].name
                )
                if oldValue != newValue:
                    if isinstance(oldValue, str):
                        oldValueWithoutNewLine = oldValue.replace("\n", "<br>")
                        newValueWithoutNewLine = newValue.replace("\n", "<br>")
                    else:
                        oldValueWithoutNewLine = oldValue
                        newValueWithoutNewLine = newValue
                    diffStr += f"""   {field.name}: {oldValueWithoutNewLine} ->
                    {newValueWithoutNewLine}\n"""

            elif isinstance(field, ManyToManyField):
                fieldName = field.name
                oldValueDe = oldObj.getManyToManyAttrAsStr(fieldName, "_de")
                oldValueEn = oldObj.getManyToManyAttrAsStr(fieldName, "_en")

                newValueDe = newObj.getManyToManyAttrAsStr(fieldName, "_de")
                newValueEn = newObj.getManyToManyAttrAsStr(fieldName, "_en")

                oldStr = f"German: {oldValueDe}, English: {oldValueEn}"
                newStr = f"German: {newValueDe}, English: {newValueEn}"

                if oldStr != newStr:
                    diffStr += f"""   {field.name}: {oldStr} -> {newStr}\n"""

        if diffStr != "":
            diffStr = diffStrModelName + diffStr + ";;"
        self.diffStrDict[self.dictIdentifier] += diffStr

    def _checkIfEqualAndUpdate(self, newObj, oldObj):
        """ """
        objsEqual = oldObj.isEqual(newObj)
        if not objsEqual:
            newHistoryObj = self.APP_HISTORY_MODEL_OBJ(
                identifer=oldObj.__str__(),
                stringifiedObj=serialize(
                    "custom_json", [oldObj], use_natural_foreign_keys=True
                ),
            )
            # parsedJson = json.loads(newHistoryObj.stringifiedObj)
            # parsedJson[0]["pk"] = obj.pk
            # newHistoryObj.stringifiedObj = json.dumps(parsedJson)
            newHistoryObj.save()

            self._update(oldObj, newObj)
            return newObj, True
        else:
            newObj.delete()
            return oldObj, False

    def _update(self, oldObj, newObj):
        """Set all fields of the new ORM object into the old object."""

        for field in newObj._meta.get_fields():
            if field.name != "id":
                if isinstance(field, models.ManyToManyField):
                    getattr(oldObj, field.name).set(
                        getattr(newObj, field.name).all()
                    )
                elif isinstance(field, models.ManyToManyRel):
                    getattr(oldObj, f"{field.name}_set").set(
                        getattr(newObj, f"{field.name}_set").all()
                    )
                else:
                    if hasattr(newObj, field.name):
                        setattr(oldObj, field.name, getattr(newObj, field.name))

        oldObj.save()
        newObj.delete()

    def _writeDiffStrToDB(self):
        """ """

        DbDiff.objects.create(
            identifier=self.dictIdentifier,
            diffStr=self.diffStrDict[self.dictIdentifier],
        )
