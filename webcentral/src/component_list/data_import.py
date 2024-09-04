from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport

from .models import *


class DataImportApp(DataImport):
    DJANGO_APP = "component_list"
    DJANGO_MODEL = "Component"
    MAPPING_EXCEL_DB_EN = {
        "Kategorie__en": "category_en",
        "Komponente__en": "componentClass_en",
        "Beschreibung__en": "description_en",
        "Weitere Informationen / Anmerkungen__en": "furtherInformationNotes_en",
    }

    def __init__(self, path_to_data_file):
        """Constructor of the app-specific data_import

        Calls the constructor of the parent class `DataImport`.
        The parent-class then handles the read in process of the
        file, whose file-path was given as `path_to_data_file`.

        path_to_data_file:  str
            Represents the file-path to the Data-File (xlsx or csv).
        """
        super().__init__(path_to_data_file)

    def getOrCreate(self, row: list, header: list, data: list) -> tuple:
        """Gets or Creates an object of type UserIntegration from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        UserIntegration according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    UserIntegration
            UserIntegration-object, represent the created or in database
            present UserIntegration-Dataset with the data from row.
        created:    bool
            Indicates, if the UserIntegration-object was created or not.
        """
        categoryName = row[header.index("Kategorie")]
        # category = self._correctReadInValue(categoryName)
        categoryStr = self._selectNearestMatch(categoryName, Category)
        category = Category.objects.get(category=categoryStr)
        # Add foreign key relation to category
        componentName = row[header.index("Komponente")]
        componentStr = self._selectNearestMatch(componentName, ComponentClass)
        component = ComponentClass.objects.get(componentClass=componentStr)
        description = row[header.index("Beschreibung")]
        try:
            energyConsumptionUsePhaseTotal = float(
                row[
                    header.index("Energieverbrauch Nutzungsphase (gesamt; in kWh/Jahr)")
                ]
            )
        except ValueError:
            energyConsumptionUsePhaseTotal = None
        try:
            specificGlobalWarmingPotentialTotal = float(
                row[
                    header.index(
                        "Spezifisches Teibhauspotential Gesamt  (in kg CO2-e/Jahr)"
                    )
                ]
            )
        except ValueError:
            specificGlobalWarmingPotentialTotal = None
        try:
            globalWarmingPotentialTotal = float(
                row[header.index("Treibhauspotenzial (gesamt; in kg CO2-e)")]
            )
        except ValueError:
            globalWarmingPotentialTotal = None
        try:
            componentWeight = float(row[header.index("Bauteilgewicht (in kg)")])
        except ValueError:
            componentWeight = None
        try:
            lifetime = float(row[header.index("Lebensdauer (in Jahre)")])
        except ValueError:
            lifetime = None
        # lifetime = row[header.index("Lifetime (in years)")]
        powerConsumptionUsePhaseActiveStr = row[
            header.index("Leistung Nutzungsphase (akitv; in W)")
        ]
        energyConsumptionUsePhaseActive, powerUseActiveSuper = (
            self._processFloatWithCharacter(str(powerConsumptionUsePhaseActiveStr))
        )

        try:
            energyConsumptionUsePhasePassive = float(
                row[header.index("Leistung Nutzungsphase (passiv/ Stand-by; in W)")]
            )
        except ValueError:
            energyConsumptionUsePhasePassive = None

        globalWarmingPotentialProductionStr = row[
            header.index("Treibhauspotenzial (Herstellung; in kg CO2-e)")
        ]
        globalWarmingPotentialProduction, potentialProductionSup = (
            self._processFloatWithCharacter(str(globalWarmingPotentialProductionStr))
        )

        globalWarmingPotentialUsePhase = row[
            header.index("Treibhauspotenzial (Nutzung; in kg CO2-e)")
        ]
        globalWarmingPotentialUsePhase, potentialUseSup = (
            self._processFloatWithCharacter(str(globalWarmingPotentialUsePhase))
        )

        try:
            globalWarmingPotentialEndOfLife = float(
                row[header.index("Treibhauspotenzial (Entsorgung; in kg CO2-e)")]
            )
        except ValueError:
            globalWarmingPotentialEndOfLife = None
        furtherInformationNotes = row[
            header.index("Weitere Informationen / Anmerkungen")
        ]
        sources = row[header.index("Quellen")]

        operationTimeStr = row[header.index("Betriebsdauer (h/Jahr)")]
        yearOfUse, operationSup = self._processFloatWithCharacter(str(operationTimeStr))

        obj, created = Component.objects.get_or_create(
            category=category,
            componentClass=component,
            description=description,
            energyConsumptionUsePhaseTotal=energyConsumptionUsePhaseTotal,
            globalWarmingPotentialTotal=globalWarmingPotentialTotal,
            specificGlobalWarmingPotential=specificGlobalWarmingPotentialTotal,
            powerUseCasePhaseActiveSuperscript=powerUseActiveSuper,
            componentWeight=componentWeight,
            lifetime=lifetime,
            energyConsumptionUsePhaseActive=energyConsumptionUsePhaseActive,
            energyConsumptionUsePhasePassive=energyConsumptionUsePhasePassive,
            globalWarmingPotentialProduction=globalWarmingPotentialProduction,
            globalWarmingPotentialProdSup=potentialProductionSup,
            globalWarmingPotentialUsePhase=globalWarmingPotentialUsePhase,
            globalWarmingPotentialUsePhaseSup=potentialUseSup,
            globalWarmingPotentialEndOfLife=globalWarmingPotentialEndOfLife,
            furtherInformationNotes=furtherInformationNotes,
            sources=sources,
            operationTime=yearOfUse,
            operationTimeSupscript=operationSup,
        )
        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(obj, header, row, self.MAPPING_EXCEL_DB_EN)
        return obj, created

    # def _getOrCreateEnglishTranslation(self, row: list, header: list, data: list, environmentalimpactObj):
    #     """
    #
    #     """
    #     for mappingKey in self.MAPPING_EXCEL_DB_EN.keys():
    #         # attributeNameWithoutEn = self.MAPPING_EXCEL_DB_EN[mappingKey].remove("__en")
    #         # if hasattr(obj, attributeNameWithoutEn)
    #         try:
    #             setattr(environmentalimpactObj, self.MAPPING_EXCEL_DB_EN[mappingKey], row[header.index(mappingKey)])
    #         except:
    #             breakpoint()
    #     environmentalimpactObj.save()
    #
    #

    def _processFloatWithCharacter(self, strElement):
        """ """
        superscript = None
        if strElement[-1] in "abcd":
            superscript = strElement[-1]
            numElement = strElement[:-1]
        else:
            numElement = strElement

        numElement = numElement.replace(",", ".")
        try:
            floatNumElement = float(numElement)
        except:
            floatNumElement = None

        return floatNumElement, superscript
