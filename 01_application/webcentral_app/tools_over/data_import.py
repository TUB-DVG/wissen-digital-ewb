
from datetime import (
        datetime,
        timedelta,
)
import pandas as pd

from common.data_import import DataImport
from .models import (
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    TargetGroup,
    LifeCyclePhase,
    UserInterface,
    Accessibility,
    Scale,
    Tools,
)
from TechnicalStandards.models import (
        Norm,
        Protocol,
)
from project_listing.models import Subproject

class DataImportApp(DataImport):
    
    MAPPING_EXCEL_DB_EN = {
        "name_en": "name_en",
        "shortDescription_en": "shortDescription_en",
        # "resources_en": "resources_en",
        # "applicationArea_en": "applicationArea_en",
        # "provider_en": "provider_en",
        # "usage_en": "usage_en",
        # "lifeCyclePhase_en": "lifeCyclePhase_en",
        # "targetGroup_en": "targetGroup_en",
        # "userInterface_en": "userInterface_en",
        # "userInterfaceNotes_en": "userInterfaceNotes_en",
        # "programmingLanguages_en": "programmingLanguages_en",
        # "frameworksLibraries_en": "frameworksLibraries_en",
        # "databaseSystem_en": "databaseSystem_en",
        # "classification_en": "classification_en",
        # "focus_en": "focus_en",
        # "scale_en": "scale_en",
        # "lastUpdate_en": "lastUpdate_en",
        # "accessibility_en": "accessibility_en",
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
            obj, created = self.getOrCreate(row, header)

    def getOrCreate(
        self,
        row: list,
        header: list,
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
        shortDescription = row[header.index("shortDescription")]

        processedApplicationAreaList = self._correctReadInValue(
            row[header.index("applicationArea")])
        applicationAreaList = self._iterateThroughListOfStrings(
            processedApplicationAreaList, ApplicationArea)

        processedUsageList = self._correctReadInValue(
            row[header.index("usage")])
        usageList = self._iterateThroughListOfStrings(processedUsageList,
                                                      Usage)

        processedTargetGroup = self._correctReadInValue(
            row[header.index("targetGroup")])
        targetGroupList = self._iterateThroughListOfStrings(
            processedTargetGroup, TargetGroup)

        processedAccessibilityList = self._correctReadInValue(
            row[header.index("accessibility")])
        accessibilityList = self._iterateThroughListOfStrings(
            processedAccessibilityList, Accessibility)

        processedlifeCyclePhase = self._correctReadInValue(
            row[header.index("lifeCyclePhase")])
        lifeCyclePhaseList = self._iterateThroughListOfStrings(
            processedlifeCyclePhase, LifeCyclePhase)

        processedUserInterface = self._correctReadInValue(
            row[header.index("userInterface")])
        userInterfaceList = self._iterateThroughListOfStrings(
            processedUserInterface, UserInterface)

        lastUpdate = row[header.index("lastUpdate")]

        correctLastUpdateValues = ["unbekannt", "laufend"]
        if lastUpdate == "":
            lastUpdate = "unbekannt"
        if lastUpdate not in correctLastUpdateValues:
            if isinstance(lastUpdate, pd.Timestamp) or isinstance(
                    lastUpdate, datetime):
                date = lastUpdate.date()
            else:
                try:
                    # Try to parse the string as a date with time
                    date = datetime.strptime(lastUpdate, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        # If that fails, try to parse it as a date without time
                        date = datetime.strptime(lastUpdate, "%Y-%m-%d")
                    except ValueError:
                        # If that also fails, return None
                        raise ValueError(
                            f"The tool {name} could not be imported, because the lastUpdate-Value is {lastUpdate}. Only 'unbekannt', 'laufend' or a date in the format 'YYYY-MM-DD' is allowed."
                        )

            # Return the date part of the datetime object as a string
            lastUpdate = date.strftime("%Y-%m-%d")

        license = row[header.index("license")]
        licenseNotes = row[header.index("licenseNotes")]
        furtherInfos = row[header.index("furtherInformation")]
        alternatives = row[header.index("alternatives")]
        processedSpecificApplicationList = self._correctReadInValue(
            row[header.index("specificApplication")])
        specificApplicationList = self._iterateThroughListOfStrings(
            processedSpecificApplicationList, Subproject)

        provider = row[header.index("provider")]
        imageName = row[header.index("image")]
        processedScaleList = self._correctReadInValue(
            row[header.index("scale")])

        scaleList = self._iterateThroughListOfStrings(processedScaleList,
                                                      Scale)
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

        processedTechnicalStandardsNorms = self._correctReadInValue(
            row[header.index("technicalStandardsNorms")])
        technicalStandardsNormsList = self._iterateThroughListOfStrings(
            processedTechnicalStandardsNorms, Norm)

        technicalStandardsProtocolsList = row[header.index(
            "technicalStandardsProtocols")].split(",")
        processedFocusList = self._correctReadInValue(
            row[header.index("focus")])
        focusList = self._iterateThroughListOfStrings(processedFocusList,
                                                      Focus)

        processedClassificationList = self._correctReadInValue(
            row[header.index("classification")])
        classificationList = self._iterateThroughListOfStrings(
            processedClassificationList, Classification)
        userInterfaceNotes = row[header.index("userInterfaceNotes")]
        programmingLanguages = row[header.index("programmingLanguages")]
        frameworksLibraries = row[header.index("frameworksLibraries")]
        databaseSystem = row[header.index("databaseSystem")]
        resources = row[header.index("resources")]
        # breakpoint()
        focusElements = Focus.objects.filter(focus__in=focusList)
        classificationElements = Classification.objects.filter(
            classification__in=classificationList)
        applicationAreaElements = ApplicationArea.objects.filter(
            applicationArea__in=applicationAreaList)
        usageElements = Usage.objects.filter(usage__in=usageList)
        lifeCyclePhaseElements = LifeCyclePhase.objects.filter(
            lifeCyclePhase__in=lifeCyclePhaseList)
        userInterfaceElements = UserInterface.objects.filter(
            userInterface__in=userInterfaceList)
        targetGroupElements = TargetGroup.objects.filter(
            targetGroup__in=targetGroupList)
        scaleElements = Scale.objects.filter(scale__in=scaleList)
        accessibilityElements = Accessibility.objects.filter(
            accessibility__in=accessibilityList)
        specificApplicationElements = Subproject.objects.filter(
            referenceNumber_id__in=specificApplicationList)
        technicalStandardsNormsElements = Norm.objects.filter(
            name__in=technicalStandardsNormsList)
        technicalStandardsProtocolsElements = Protocol.objects.filter(
            name__in=technicalStandardsProtocolsList)
        obj, created = Tools.objects.get_or_create(
            name=name,
            shortDescription=shortDescription,
            applicationArea__in=applicationAreaElements,
            usage__in=usageElements,
            lifeCyclePhase__in=lifeCyclePhaseElements,
            userInterface__in=userInterfaceElements,
            userInterfaceNotes=userInterfaceNotes,
            programmingLanguages=programmingLanguages,
            frameworksLibraries=frameworksLibraries,
            databaseSystem=databaseSystem,
            scale__in=scaleElements,
            accessibility__in=accessibilityElements,
            targetGroup__in=targetGroupElements,
            lastUpdate=lastUpdate,
            license=license,
            licenseNotes=licenseNotes,
            furtherInformation=furtherInfos,
            alternatives=alternatives,
            specificApplication__in=specificApplicationElements,
            focus__in=focusElements,
            classification__in=classificationElements,
            provider=provider,
            image=imageName,
            released=released,
            releasedPlanned=releasedPlanned,
            resources=resources,
            yearOfRelease=yearOfRelease,
            developmentState=developmentState,
            technicalStandardsNorms__in=technicalStandardsNormsElements,
            technicalStandardsProtocols__in=technicalStandardsProtocolsElements,
        )
        if created:
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
                *technicalStandardsProtocolsElements)
            for column_identifer in list(self.MAPPING_EXCEL_DB_EN.keys()):
                setattr(obj, self.MAPPING_EXCEL_DB_EN[column_identifer], row[header.index(column_identifer)])
            obj.save()

        return obj, created

   
