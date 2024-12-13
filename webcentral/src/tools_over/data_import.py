from datetime import (
    datetime,
    timedelta,
)
import json
import re

import pandas as pd
from django.db import models

from common.data_import import DataImport
from .models import (
    Tools,
    History,
)
from common.models import (
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    TargetGroup,
    LifeCyclePhase,
    UserInterface,
    Accessibility,
    Scale,
    License,
)
from TechnicalStandards.models import (
    Norm,
)
from protocols.models import Protocol
from project_listing.models import Subproject


class DataImportApp(DataImport):

    DJANGO_MODEL = "Tools"
    DJANGO_MODEL_OBJ = Tools
    DJANGO_APP = "tools_over"
    APP_HISTORY_MODEL_OBJ = History
    MAPPING_EXCEL_DB_EN = {
        # "name_en": "name_en",
        "description__en": "description_en",
        "userInterfaceNotes__en": "userInterfaceNotes_en",
        "licenseNotes__en": "licenseNotes_en",
        "furtherInformation__en": "furtherInformation_en",
        "provider__en": "provider_en",
        "yearOfRelease__en": "yearOfRelease_en",
        "lastUpdate__en": "lastUpdate_en",
        "classification__en": "classification_en",
        "resources__en": "resources_en",
        "applicationArea__en": "applicationArea_en",
        "provider__en": "provider_en",
        "usage__en": "usage_en",
        "lifeCyclePhase__en": "lifeCyclePhase_en",
        "targetGroup__en": "targetGroup_en",
        "userInterface__en": "userInterface_en",
        "focus__en": "focus_en",
        # "userInterfaceNotes_en": "userInterfaceNotes_en",
        # "databaseSystem_en": "databaseSystem_en",
        # "classification_en": "classification_en",
        # "focus_en": "focus_en",
        "scale__en": "scale_en",
        # "lastUpdate_en": "lastUpdate_en",
        "accessibility__en": "accessibility_en",
        # "license_en": "license_en",
        # "licenseNotes_en": "licenseNotes_en",
        # "furtherInformation_en": "furtherInformation_en",
        # "alternatives_en": "alternatives_en",
        # "specificApplication_en": "specificApplication_en",
        # "released_en": "released_en",
        # "releasedPlanned_en": "releasedPlanned_en",
        # "yearOfRelease_en": "yearOfRelease_en",
        # "developmentState_en": "developmentState_en",
        # "technicalStandardsNorms_en": "technicalStandardsNorms_en",
        # "technicalStandardsProtocols_en": "technicalStandardsProtocols_en",
        # "image_en": "image_en",
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
        self.dictIdentifier = None
        self.personalDataFlag = False

    def getOrCreate(
        self,
        row: list,
        header: list,
        data: list,
    ) -> tuple:
        """Gets or Creates an object of type Tools from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Tools according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    ToolsSubproject the Tools-object was created or not.
        """

        name = row[header.index("name")]
        shortDescription = row[header.index("description")]

        # processedApplicationAreaList = self._correctReadInValue(
        #     row[header.index("applicationArea")]
        # )
        processedApplicationAreaList = self._processListInput(
            row[header.index("applicationArea")], separator=";;"
        )

        applicationAreaList = self._iterateThroughListOfStrings(
            processedApplicationAreaList, ApplicationArea
        )
        processedUsageList = self._processListInput(
            row[header.index("usage")], separator=";;"
        )
        usageList = self._iterateThroughListOfStrings(processedUsageList, Usage)

        processedTargetGroup = self._processListInput(
            row[header.index("targetGroup")], separator=";;"
        )
        targetGroupList = self._iterateThroughListOfStrings(
            processedTargetGroup, TargetGroup
        )

        processedAccessibilityList = self._processListInput(
            row[header.index("accessibility")], separator=";;"
        )
        accessibilityList = self._iterateThroughListOfStrings(
            processedAccessibilityList, Accessibility
        )

        processedlifeCyclePhase = self._processListInput(
            row[header.index("lifeCyclePhase")], separator=";;"
        )
        lifeCyclePhaseList = self._iterateThroughListOfStrings(
            processedlifeCyclePhase, LifeCyclePhase
        )

        processedUserInterface = self._processListInput(
            row[header.index("userInterface")], separator=";;"
        )
        userInterfaceList = self._iterateThroughListOfStrings(
            processedUserInterface, UserInterface
        )

        lastUpdate = self._processDate(row[header.index("lastUpdate")])

        processedLicenseList = self._processListInput(
            row[header.index("license")], separator=";;"
        )
        licenseList = self._iterateThroughListOfStrings(
            processedLicenseList, License
        )
        licenseNotes = row[header.index("licenseNotes")]
        furtherInfos = row[header.index("furtherInformation")]
        alternatives = row[header.index("alternatives")]
        processedSpecificApplicationList = self._processListInput(
            row[header.index("specificApplication")], separator=";;"
        )
        specificApplicationList = self._iterateThroughListOfStrings(
            processedSpecificApplicationList, Subproject
        )

        provider = row[header.index("provider")]
        imageName = row[header.index("image")]
        processedScaleList = self._processListInput(
            row[header.index("scale")], separator=";;"
        )

        scaleList = self._iterateThroughListOfStrings(processedScaleList, Scale)
        released = row[header.index("released")]
        if released == "":
            released = None
        elif released == "unbekannt":
            released = None
        else:
            released = bool(int(released))

        releasedPlanned = row[header.index("releasedPlanned")]
        if releasedPlanned == "":
            releasedPlanned = None
        else:
            releasedPlanned = bool(int(releasedPlanned))

        yearOfRelease = row[header.index("yearOfRelease")]

        developmentState = row[header.index("developmentState")]
        if developmentState == "":
            developmentState = None
        else:
            developmentState = int(developmentState)

        processedTechnicalStandardsNorms = self._processListInput(
            row[header.index("technicalStandardsNorms")], separator=";;"
        )
        technicalStandardsNormsList = self._iterateThroughListOfStrings(
            processedTechnicalStandardsNorms, Norm
        )

        technicalStandardsProtocolsList = row[
            header.index("technicalStandardsProtocols")
        ].split(",")
        processedFocusList = self._processListInput(
            row[header.index("focus")], separator=";;"
        )
        focusList = self._iterateThroughListOfStrings(processedFocusList, Focus)

        processedClassificationList = self._processListInput(
            row[header.index("classification")], separator=";;"
        )
        classificationList = self._iterateThroughListOfStrings(
            processedClassificationList, Classification
        )
        userInterfaceNotes = row[header.index("userInterfaceNotes")]
        programmingLanguages = row[header.index("programmingLanguages")]
        frameworksLibraries = row[header.index("frameworksLibraries")]
        databaseSystem = row[header.index("databaseSystem")]
        resources = row[header.index("resources")]
        focusElements = Focus.objects.filter(focus__in=focusList)
        classificationElements = Classification.objects.filter(
            classification__in=classificationList
        )
        applicationAreaElements = ApplicationArea.objects.filter(
            applicationArea__in=applicationAreaList
        )
        usageElements = Usage.objects.filter(usage__in=usageList)
        lifeCyclePhaseElements = LifeCyclePhase.objects.filter(
            lifeCyclePhase__in=lifeCyclePhaseList
        )
        userInterfaceElements = UserInterface.objects.filter(
            userInterface__in=userInterfaceList
        )
        targetGroupElements = TargetGroup.objects.filter(
            targetGroup__in=targetGroupList
        )
        scaleElements = Scale.objects.filter(scale__in=scaleList)
        accessibilityElements = Accessibility.objects.filter(
            accessibility__in=accessibilityList
        )
        specificApplicationElements = Subproject.objects.filter(
            referenceNumber_id__in=specificApplicationList
        )
        technicalStandardsNormsElements = Norm.objects.filter(
            name__in=technicalStandardsNormsList
        )
        technicalStandardsProtocolsElements = Protocol.objects.filter(
            name__in=technicalStandardsProtocolsList
        )
        licenseElements = License.objects.filter(license__in=licenseList)

        obj = Tools(
            name=name,
            description=shortDescription,
            # applicationArea__in=applicationAreaElements,
            # usage__in=usageElements,
            # lifeCyclePhase__in=lifeCyclePhaseElements,
            # userInterface__in=userInterfaceElements,
            userInterfaceNotes=userInterfaceNotes,
            programmingLanguages=programmingLanguages,
            frameworksLibraries=frameworksLibraries,
            databaseSystem=databaseSystem,
            # scale__in=scaleElements,
            # accessibility__in=accessibilityElements,
            # targetGroup__in=targetGroupElements,
            lastUpdate=lastUpdate,
            # license=license,
            licenseNotes=licenseNotes,
            furtherInformation=furtherInfos,
            alternatives=alternatives,
            # specificApplication__in=specificApplicationElements,
            # focus__in=focusElements,
            # classification__in=classificationElements,
            provider=provider,
            image=imageName,
            released=released,
            releasedPlanned=releasedPlanned,
            resources=resources,
            yearOfRelease=yearOfRelease,
            developmentState=developmentState,
            # technicalStandardsNorms__in=technicalStandardsNormsElements,
            # technicalStandardsProtocols__in=technicalStandardsProtocolsElements,
        )

        tupleOrNone = self._checkIfItemExistsInDB(
            row[header.index("name")], "name"
        )

        obj.save()
        # obj.id = toolInDb.id
        obj.license.add(*licenseElements)
        obj.focus.add(*focusElements)
        obj.classification.add(*classificationElements)
        obj.applicationArea.add(*applicationAreaElements)
        obj.usage.add(*usageElements)
        obj.lifeCyclePhase.add(*lifeCyclePhaseElements)
        obj.userInterface.add(*userInterfaceElements)
        obj.scale.add(*scaleElements)
        obj.accessibility.add(*accessibilityElements)
        obj.targetGroup.add(*targetGroupElements)
        obj.specificApplication.add(*specificApplicationElements)
        obj.technicalStandardsNorms.add(*technicalStandardsNormsElements)
        obj.technicalStandardsProtocols.add(
            *technicalStandardsProtocolsElements
        )
        obj.save()
        obj = self._importEnglishTranslation(
            obj, header, row, self.MAPPING_EXCEL_DB_EN
        )
        obj.save()
        if tupleOrNone is None:
            return obj, True
        idOfAlreadyPresentTool = tupleOrNone[0]
        return self._checkIfEqualAndUpdate(obj, tupleOrNone[1])

    def _processDate(self, lastUpdate: str):
        """Process a string value into a datetime object."""
        reForDotDate = re.compile("[0-9]{4,4}\.[0-9]{2,2}\.[0-9]{2,2}")
        reMinusDate = re.compile("[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}")
        correctLastUpdateValues = ["unbekannt", "laufend"]
        if lastUpdate == "":
            lastUpdate = "unbekannt"
        if lastUpdate not in correctLastUpdateValues:
            if isinstance(lastUpdate, pd.Timestamp) or isinstance(
                lastUpdate, datetime
            ):
                date = lastUpdate.date()
            else:
                try:
                    lastUpdate = lastUpdate.replace(" ", "")
                except:
                    breakpoint()
                if reForDotDate.search(lastUpdate) is not None:
                    spanOfMatch = reForDotDate.search(lastUpdate).span()
                    date = datetime.strptime(
                        lastUpdate[spanOfMatch[0] : spanOfMatch[1]], "%Y.%m.%d"
                    )
                    lastUpdate = date.strftime("%Y-%m-%d")

                elif reMinusDate.search(lastUpdate) is not None:
                    spanOfMatch = reMinusDate.search(lastUpdate).span()
                    date = datetime.strptime(
                        lastUpdate[spanOfMatch[0] : spanOfMatch[1]], "%Y-%m-%d"
                    )
                    lastUpdate = date.strftime("%Y-%m-%d")
                else:

                    lastUpdate = "unbekannt"

        return lastUpdate

    def _update(self, oldObj, newObj):
        """Set all fields of the new ORM object into the old object."""

        for field in newObj._meta.get_fields():
            if field.name != "id":
                if isinstance(field, models.ManyToManyField):
                    getattr(oldObj, field.name).set(
                        getattr(newObj, field.name).all()
                    )
                else:
                    setattr(oldObj, field.name, getattr(newObj, field.name))

        oldObj.save()
        newObj.delete()
