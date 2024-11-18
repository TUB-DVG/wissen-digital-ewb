import json

from django.db import models
from django.db.models.functions import Now

from project_listing.models import Subproject
from TechnicalStandards.models import (
    Norm,
)
from protocols.models import Protocol
from common.models import (
    Accessibility,
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    Scale,
    LifeCyclePhase,
    TargetGroup,
    UserInterface,
)


class Tools(models.Model):
    name = models.CharField(max_length=150, help_text="name", blank=True)
    shortDescription = models.CharField(
        max_length=1000, help_text="short description", blank=True
    )
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        db_comment="What do the developers describe as the area of application of their digital tool",
    )
    usage = models.ManyToManyField(Usage)
    targetGroup = models.ManyToManyField(
        TargetGroup,
        blank=True,
        null=True,
    )
    lifeCyclePhase = models.ManyToManyField(LifeCyclePhase)
    userInterface = models.ManyToManyField(
        UserInterface,
        blank=True,
        null=True,
    )
    userInterfaceNotes = models.CharField(
        max_length=300,
        help_text="additional notes for userInterface",
        blank=True,
    )
    accessibility = models.ManyToManyField(Accessibility)
    lastUpdate = models.CharField(
        max_length=100,
        help_text="time (year/month/date) of the last update",
        blank=True,
    )
    license = models.CharField(max_length=500, help_text="license", blank=True)
    licenseNotes = models.CharField(
        max_length=500, help_text="license notes", blank=True
    )
    furtherInformation = models.CharField(
        max_length=500, help_text="further information", blank=True
    )
    alternatives = models.CharField(
        max_length=300,
        help_text="similar tool(s) that can serve as alternatives",
        blank=True,
    )
    specificApplication = models.ManyToManyField(
        Subproject,
        help_text="specific application of the tool in EWB projects (project name + fkz)",
        blank=True,
        null=True,
    )

    provider = models.CharField(
        max_length=300,
        blank=True,
    )
    released = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether the tool is released or not",
    )
    releasedPlanned = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether publication is planned",
    )
    yearOfRelease = models.CharField(
        blank=True,
        max_length=100,
        help_text="year of software release (planned or conducted)",
    )
    resources = models.CharField(
        max_length=1000,
        blank=True,
        help_text="documentation, literature, git-Repos, etc.",
    )
    choices = [
        (1, "pre-alpha"),
        (2, "alpha"),
        (3, "beta"),
        (4, "release candidate"),
        (5, "release"),
    ]
    developmentState = models.IntegerField(
        choices=choices,
        null=True,
        blank=True,
    )

    programmingLanguages = models.CharField(
        max_length=500,
        blank=True,
        db_comment="Programming languages - Which programming languages are mainly used to implment the item.",
    )
    frameworksLibraries = models.CharField(
        max_length=500,
        blank=True,
    )
    databaseSystem = models.CharField(
        max_length=500,
        blank=True,
    )
    scale = models.ManyToManyField(
        Scale,
        blank=True,
        null=True,
    )

    technicalStandardsNorms = models.ManyToManyField(
        Norm,
        blank=True,
        null=True,
    )
    technicalStandardsProtocols = models.ManyToManyField(
        Protocol,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        null=True,
        blank=True,
    )

    classification = models.ManyToManyField(Classification)
    focus = models.ManyToManyField(Focus)

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

    @property
    def imageOrDefault(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return "{% static 'assets/default.jpg' %}"

    def __str__(self):
        return self.name

    class Meta:
        app_label = "tools_over"

    def _update(self, newState, historyObj):
        """Set all fields of the new ORM object into the old object."""
        stringifiedObj = json.loads(historyObj.stringifiedObj)

        for field in self._meta.get_fields():
            if field.name != "id":
                if isinstance(field, models.ManyToManyField):
                    listOfM2Mobjs = []
                    for naturalKeyTuple in stringifiedObj[0]["fields"][
                        field.name
                    ]:
                        if field.name != "specificApplication":
                            listOfM2Mobjs.append(
                                getattr(
                                    self, field.name
                                ).model.objects.get_by_natural_key(
                                    naturalKeyTuple[0], naturalKeyTuple[1]
                                )
                            )
                        else:
                            specificApplicationElements = stringifiedObj[0][
                                "fields"
                            ][field.name]
                            listOfM2Mobjs = []
                            for (
                                enargusprojectNumber
                            ) in specificApplicationElements:
                                listOfM2Mobjs.append(
                                    Subproject.objects.get(
                                        referenceNumber_id=enargusprojectNumber
                                    )
                                )
                    getattr(self, field.name).set(listOfM2Mobjs)

                else:
                    setattr(self, field.name, getattr(newState, field.name))

        self.save()


class History(models.Model):
    """model class to store updates of the Tools model"""

    identifer = models.CharField(max_length=300)
    stringifiedObj = models.TextField()
    loaded = models.BooleanField(default=False)
    updateDate = models.DateTimeField(db_default=Now())

    def get_fields(self):
        """Returns a list of field names and values for use in templates."""
        return [
            (field.name, getattr(self, field.name))
            for field in self._meta.get_field
        ]

    def __str__(self):
        """ """
        showedName = str(self.identifer) + " " + str(self.updateDate)
        return showedName
