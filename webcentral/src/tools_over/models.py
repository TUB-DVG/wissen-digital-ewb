import json

from django.db import models
from django.db.models.functions import Now

from project_listing.models import Subproject
from TechnicalStandards.models import (
    Norm,
    Protocol,
)


class ClassificationManager(models.Manager):
    def get_by_natural_key(self, classification_de, classification_en):
        return self.get(
            classification_de=classification_de,
            classification_en=classification_en,
        )


class Classification(models.Model):
    """Model for"""

    classification = models.CharField(
        max_length=100,
        help_text="Classification Category",
    )

    objects = ClassificationManager()

    def __str__(self):
        return self.classification

    def natural_key(self):
        return (self.classification_de, self.classification_en)

    class Meta:

        app_label = "tools_over"


class FocusManager(models.Manager):
    def get_by_natural_key(self, focus_de, focus_en):
        return self.get(focus_de=focus_de, focus_en=focus_en)


class Focus(models.Model):
    """Focus of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    focus = models.CharField(
        max_length=100,
        help_text="Focus of the Tool",
    )

    objects = FocusManager()

    def __str__(self):
        return self.focus

    def natural_key(self):
        return (self.focus_de, self.focus_en)

    class Meta:

        app_label = "tools_over"


class ApplicationAreaManager(models.Manager):
    def get_by_natural_key(self, applicationArea_de, applicationArea_en):
        return self.get(
            applicationArea_de=applicationArea_de,
            applicationArea_en=applicationArea_en,
        )


class ApplicationArea(models.Model):
    """ApplicationArea of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    applicationArea = models.CharField(
        max_length=1000,
        help_text="application area",
        blank=True,
    )
    objects = ApplicationAreaManager()

    def natural_key(self):
        return (self.applicationArea_de, self.applicationArea_en)

    def __str__(self):
        return self.applicationArea

    class Meta:
        app_label = "tools_over"


class UsageManager(models.Manager):
    def get_by_natural_key(self, usage_de, usage_en):
        return self.get(usage_de=usage_de, usage_en=usage_en)


class Usage(models.Model):
    """Usage of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    usage = models.CharField(
        max_length=100,
        help_text="usage",
        blank=True,
    )

    objects = UsageManager()

    def natural_key(self):
        return (self.usage_de, self.usage_en)

    def __str__(self):
        return self.usage

    class Meta:

        app_label = "tools_over"


class TargetGroupManager(models.Manager):
    def get_by_natural_key(self, targetGroup_de, targetGroup_en):
        return self.get(
            targetGroup_de=targetGroup_de, targetGroup_en=targetGroup_en
        )


class TargetGroup(models.Model):
    """TargetGroup of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    targetGroup = models.CharField(
        max_length=300,
        help_text="Which group of people is the tool targeted at?",
        blank=True,
    )

    objects = TargetGroupManager()

    def natural_key(self):
        return (self.targetGroup_de, self.targetGroup_en)

    def __str__(self):
        return self.targetGroup

    class Meta:
        app_label = "tools_over"


class LifeCyclePhaseManager(models.Manager):
    def get_by_natural_key(self, lifeCyclePhase_de, lifeCyclePhase_en):
        return self.get(
            lifeCyclePhase_de=lifeCyclePhase_de,
            lifeCyclePhase_en=lifeCyclePhase_en,
        )


class LifeCyclePhase(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    lifeCyclePhase = models.CharField(
        max_length=100,
        help_text="Life cycle phase of buildings where the application is used",
        blank=True,
    )

    objects = LifeCyclePhaseManager()

    def natural_key(self):
        return (self.lifeCyclePhase_de, self.lifeCyclePhase_en)

    def __str__(self):
        return self.lifeCyclePhase

    class Meta:

        app_label = "tools_over"


class UserInterfaceManager(models.Manager):
    def get_by_natural_key(self, userInterface_de, userInterface_en):
        return self.get(
            userInterface_de=userInterface_de, userInterface_en=userInterface_en
        )


class UserInterface(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    userInterface = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )

    objects = UserInterfaceManager()

    def natural_key(self):
        return (self.userInterface_de, self.userInterface_en)

    def __str__(self):
        return self.userInterface

    class Meta:
        app_label = "tools_over"


class AccessibilityManager(models.Manager):
    def get_by_natural_key(self, accessibility_de, accessibility_en):
        return self.get(
            accessibility_de=accessibility_de, accessibility_en=accessibility_en
        )


class Accessibility(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    accessibility = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )

    objects = AccessibilityManager()

    def __str__(self):
        return self.accessibility

    def natural_key(self):
        return (self.accessibility_de, self.accessibility_en)

    class Meta:

        app_label = "tools_over"


class ScaleManager(models.Manager):
    def get_by_natural_key(self, scale_de, scale_en):
        return self.get(scale_de=scale_de, scale_en=scale_en)


class Scale(models.Model):
    """Scale of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    scale = models.CharField(
        max_length=100,
        help_text="spatial scope of consideration",
        blank=True,
    )

    objects = ScaleManager()

    def natural_key(self):
        return (self.scale_de, self.scale_en)

    def __str__(self):
        return self.scale

    class Meta:

        app_label = "tools_over"


class Tools(models.Model):
    name = models.CharField(max_length=150, help_text="name", blank=True)
    shortDescription = models.CharField(
        max_length=1000, help_text="short description", blank=True
    )
    applicationArea = models.ManyToManyField(ApplicationArea)
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

    def getManyToManyAttrAsStr(self, manyToManyAttr, languageSuffix, separator=","):
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
        return returnStr[:-len(separator)]

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
        """Set all fields of the new ORM object into the old object.

        """
        stringifiedObj = json.loads(historyObj.stringifiedObj)

        for field in self._meta.get_fields():
            if field.name != "id":
                if isinstance(field, models.ManyToManyField):
                    listOfM2Mobjs = []
                    for naturalKeyTuple in stringifiedObj[0]["fields"][field.name]:
                        listOfM2Mobjs.append(getattr(self, field.name).model.objects.get_by_natural_key(naturalKeyTuple[0], naturalKeyTuple[1]))
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
