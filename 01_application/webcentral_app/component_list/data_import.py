
from datetime import (
        datetime,
        timedelta,
)
import pandas as pd

from common.data_import import DataImport

from .models import *

class DataImportApp(DataImport):
    
    MAPPING_EXCEL_DB_EN = {
        "Kategorie__en": "category_en",
        "Komponente__en": "component_en",
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
            energyConsumptionUsePhaseTotal = float(row[header.index(
                "Energieverbrauch Nutzungsphase (gesamt; in kWh/Jahr)")])
        except ValueError:
            energyConsumptionUsePhaseTotal = None
        try:
            specificGlobalWarmingPotentialTotal = float(row[header.index(
                "Spezifisches Teibhauspotential Gesamt  (in kg CO2-e/Jahr)")])
        except ValueError:
            specificGlobalWarmingPotentialTotal = None
        try:
            globalWarmingPotentialTotal = float(row[header.index(
                "Treibhauspotenzial (gesamt; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialTotal = None       
        try:
            componentWeight = float(
                row[header.index("Bauteilgewicht (in kg)")])
        except ValueError:
            componentWeight = None
        try:
            lifetime = float(row[header.index("Lebensdauer (in Jahre)")])
        except ValueError:
            lifetime = None
        # lifetime = row[header.index("Lifetime (in years)")]
        try:
            energyConsumptionUsePhaseActive = float(row[header.index(
                "Leistung Nutzungsphase (akitv; in W)")])
        except ValueError:
            energyConsumptionUsePhaseActive = None
        try:
            energyConsumptionUsePhasePassive = float(row[header.index(
                "Leistung Nutzungsphase (passiv/ Stand-by; in W)")])
        except ValueError:
            energyConsumptionUsePhasePassive = None

        try:
            globalWarmingPotentialProduction = float(row[header.index(
                "Treibhauspotenzial (Herstellung; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialProduction = None
        try:
            globalWarmingPotentialUsePhase = float(row[header.index(
                "Treibhauspotenzial (Nutzung; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialUsePhase = None
        try:
            globalWarmingPotentialEndOfLife = float(row[header.index(
                "Treibhauspotenzial (Entsorgung; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialEndOfLife = None
        furtherInformationNotes = row[header.index(
            "Weitere Informationen / Anmerkungen")]
        sources = row[header.index("Quellen")]
        try:
            yearOfUse = int(row[header.index("Betriebsdauer (h/Jahr)")])
        except:
            yearOfUse = None
        obj, created = Component.objects.get_or_create(
            category=category,
            component=component,
            description=description,
            energyConsumptionUsePhaseTotal=energyConsumptionUsePhaseTotal,
            globalWarmingPotentialTotal=globalWarmingPotentialTotal,
            specificGlobalWarmingPotential=specificGlobalWarmingPotentialTotal,
            componentWeight=componentWeight,
            lifetime=lifetime,
            energyConsumptionUsePhaseActive=energyConsumptionUsePhaseActive,
            energyConsumptionUsePhasePassive=energyConsumptionUsePhasePassive,
            globalWarmingPotentialProduction=globalWarmingPotentialProduction,
            globalWarmingPotentialUsePhase=globalWarmingPotentialUsePhase,
            globalWarmingPotentialEndOfLife=globalWarmingPotentialEndOfLife,
            furtherInformationNotes=furtherInformationNotes,
            sources=sources,
            yearOfUsePerYear=yearOfUse,
        )
        
        if _englishHeadersPresent(header):
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
    def _englishHeadersPresent(self, header: list) -> bool:
        """Check if english translation headers are present in the
        list of headers. If yes, then return `True` otherwise `False`

        """
        for headerItem in header:
            if "__en" in headerItem:
                return True
        
        return False
