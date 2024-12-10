import pandas as pd
from django.db import models

from businessModel.models import BusinessModel


class DataExport:
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "challenge": "challenge",
        "shortDescription": "shortDescription",
        "property1": "property1",
        "property1Text": "property1Text",
        "property2": "property2",
        "property2Text": "property2Text",
        "property3": "property3",
        "property3Text": "property3Text",
        "property4": "property4",
        "property4Text": "property4Text",
        "property5": "property5",
        "property5Text": "property5Text",
        "imageIcon": "imageIcon",
        "imageIconSelected": "imageIconSelected",
    }

    DATA_APP_DIR = "10_business_models"
    EXPORT_MODEL_OBJ = BusinessModel

    def __init__(self, filename):
        """ """
        self.filename = filename

    def exportToXlsx(self):
        """ """

        allBusinessModels = self.EXPORT_MODEL_OBJ.objects.all()

        germanData, englishData = self._sortObjectsIntoGermanAndEnglishDs(
            allBusinessModels
        )

        self._writeDictsToXlsx(germanData, englishData)

    def _sortObjectsIntoGermanAndEnglishDs(self, ormObjs) -> tuple:
        """Sort the the german and english attributes of the ORM-objects into to different dictionaries.

        Arguments:
        ormObjs: Queryset
            Iterable of orm-objs to be sorted into german and english buckets

        Returns:
            tuple of germanData and englishData

        """
        germanData = {}
        englishData = {}

        for ormObj in ormObjs:

            for mappingNameORM in self.MAPPING_ORM_TO_XLSX.keys():
                if hasattr(ormObj, mappingNameORM + "_en"):
                    englishData = self._checkIfKeyExistsAndAppendData(
                        englishData, mappingNameORM
                    )
                    englishData = self._apppendToDs(
                        englishData, mappingNameORM, ormObj, "_en"
                    )

                    germanData = self._checkIfKeyExistsAndAppendData(
                        germanData, mappingNameORM
                    )
                    germanData = self._apppendToDs(
                        germanData, mappingNameORM, ormObj, "_de"
                    )

                else:
                    englishData = self._checkIfKeyExistsAndAppendData(
                        englishData, mappingNameORM
                    )
                    englishData = self._apppendToDs(
                        englishData, mappingNameORM, ormObj, "_en"
                    )

                    germanData = self._checkIfKeyExistsAndAppendData(
                        germanData, mappingNameORM
                    )
                    germanData = self._apppendToDs(
                        germanData, mappingNameORM, ormObj, "_de"
                    )

        return (germanData, englishData)

    def _checkIfKeyExistsAndAppendData(self, dataDict, keyName) -> dict:
        """Check if the key in the data-dict exists otherwise create it.

        Arguments:
        dataDict: dict
            datastructure to store a table. keys are the column name.
        keyName: str
            name of the key to be checked if a key in the dict.

        Returns:
            dict
        """
        if keyName in dataDict.keys():
            return dataDict

        dataDict[keyName] = []
        return dataDict

    def _apppendToDs(self, dataDict, mappingNameORM, ormObj, languageSuffix):
        """ """
        if isinstance(
            ormObj._meta.get_field(mappingNameORM), models.ManyToManyField
        ):
            concatenatedMTMStr = ormObj.getManyToManyAttrAsStr(
                mappingNameORM, languageSuffix, separator=";;"
            )
            dataDict[mappingNameORM].append(concatenatedMTMStr)
        elif isinstance(
            ormObj._meta.get_field(mappingNameORM), models.BooleanField
        ):
            valueOfBooleanField = getattr(ormObj, mappingNameORM)
            if valueOfBooleanField == "" or valueOfBooleanField is None:
                dataDict[mappingNameORM].append("")
            else:
                dataDict[mappingNameORM].append(
                    int(getattr(ormObj, mappingNameORM))
                )
        else:
            try:
                dataDict[mappingNameORM].append(
                    getattr(ormObj, mappingNameORM + languageSuffix)
                )
            except AttributeError:
                dataDict[mappingNameORM].append(getattr(ormObj, mappingNameORM))

        return dataDict

    def _writeDictsToXlsx(self, germanData, englishData):
        """ """
        dfGerman = pd.DataFrame(germanData)
        dfEnglish = pd.DataFrame(englishData)

        with pd.ExcelWriter(self.filename, engine="openpyxl") as writer:
            dfGerman.to_excel(writer, sheet_name="German", index=False)
            dfEnglish.to_excel(writer, sheet_name="English", index=False)
