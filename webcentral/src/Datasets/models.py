from django.db import models
from django.db.models.functions import Now

from common.models import (
    ApplicationArea,
    Focus,
    LifeCyclePhase,
    Scale,
    TargetGroup,
    Accessibility,
    Classification,
    AbstractTechnicalFocus,
    License,
    History,
)

class Dataset(AbstractTechnicalFocus):

    
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        db_comment="Typical application area in which the dataset is used.",
    )
    
    availability = models.CharField(
        max_length=200,
        null=True,
        db_comment="How accessible is the dataset?",
        blank=True,
    )
    coverage = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_comment="Geographical coverage - regions covered by the dataset",
    )
    
    resolution = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_comment="Spatial resolution - spatial detail level of the data",
    )
    
    licenseNotes = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_comment="Further information regarding the used license.",
    )
    
    lastUpdate = models.CharField(
        max_length=100,
        db_comment="Last update - When was the last update done?",
        blank=True,
        null=True,
    )
    
    releasedPlanned = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether publication is planned",
        db_comment="Publication planned - If the item is not yet published, are there plans to publish it?",
    )
    

    def __str__(self):
        return self.name

    def isEqual(self, other):
        """Check equality of two instances of `Tools`"""

        for field in self._meta.get_fields():
            if isinstance(field, models.ManyToManyField):
                firstObjAttr = self.getManyToManyWithTranslation(field.name)
                secondObjAttr = other.getManyToManyWithTranslation(field.name)
                if firstObjAttr != secondObjAttr:
                    return False
            else:
                if not field.name == "id":
                    firstObjAttr = getattr(self, field.name)
                    secondObjAttr = getattr(other, field.name)
                    if (firstObjAttr is None and secondObjAttr == "") or (
                        secondObjAttr is None and firstObjAttr == ""
                    ):
                        continue
                    if firstObjAttr != secondObjAttr:
                        return False

        return True

    def get_fields(self):
        """Returns a list of field names and values for use in templates."""
        return [field.name for field in self._meta.get_fields()]

    def getManyToManyWithTranslation(self, manyToManyAttr) -> str:
        """Wrapper around `getManyToManyAttrAsStr()` to return german and english version in one call.
        If german ang english translation are present in the conacnted ManyToMany-model
        both versions are returned. Otherwise only the german version is fetched.

        Arguments:
        manyToManyAttr: str
            attribute name of the ManyToMany attribute

        Returns:
            str: concatenated string of many to many attributes from connected model.
        """
        fields = self._meta.get_fields()
        for field in fields:
            if "_en" in field.name or "_de" in field.name:
                germanAttrs = self.getManyToManyAttrAsStr(manyToManyAttr, "_de")
                englishAttrs = self.getManyToManyAttrAsStr(
                    manyToManyAttr, "_en"
                )
                return germanAttrs + ", " + englishAttrs

        return self.getManyToManyAttrAsStr(manyToManyAttr, "_de")

    def getManyToManyAttrAsStr(
        self, manyToManyAttr, languageSuffix, separator=","
    ):
        """ """
        if manyToManyAttr == "specificApplication":
            querysetOfManyToManyElements = (
                getattr(self, manyToManyAttr)
                .all()
                .order_by("referenceNumber_id")
            )
        elif (
            manyToManyAttr == "technicalStandardsNorms"
            or manyToManyAttr == "technicalStandardsProtocols"
        ):
            querysetOfManyToManyElements = (
                getattr(self, manyToManyAttr).all().order_by("name")
            )
        else:
            querysetOfManyToManyElements = (
                getattr(self, manyToManyAttr).all().order_by(manyToManyAttr)
            )
        if len(querysetOfManyToManyElements) > 0:
            fieldsOfManyToManyModel = querysetOfManyToManyElements[
                0
            ]._meta.get_fields()
            fieldNames = [field.name for field in fieldsOfManyToManyModel]
            suffixInFieldNames = False
            for field in fieldNames:
                if languageSuffix in field:
                    suffixInFieldNames = True
                    break

        returnStr = ""
        for element in querysetOfManyToManyElements:
            if suffixInFieldNames:
                if getattr(element, field) is not None:
                    returnStr += getattr(element, field) + separator
            else:
                returnStr += element.__str__() + separator
        return returnStr[: -len(separator)]


class History(History):
    """History model for the Dataset model. Implements a rollback feature for `Dataset`-model"""


