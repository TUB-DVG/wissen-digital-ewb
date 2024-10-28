from django.db import models
from django.db.models.functions import Now

from project_listing.models import Subproject
from TechnicalStandards.models import (
    Norm,
    Protocol,
)


class Classification(models.Model):
    """Model for"""

    classification = models.CharField(
        max_length=100,
        help_text="Classification Category",
    )

    def __str__(self):
        return self.classification

    class Meta:

        app_label = "tools_over"


class Focus(models.Model):
    """Focus of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    focus = models.CharField(
        max_length=100,
        help_text="Focus of the Tool",
    )

    def __str__(self):
        return self.focus

    class Meta:

        app_label = "tools_over"


class ApplicationArea(models.Model):
    """ApplicationArea of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    applicationArea = models.CharField(
        max_length=1000,
        help_text="application area",
        blank=True,
    )

    def __str__(self):
        return self.applicationArea

    class Meta:
        app_label = "tools_over"


class Usage(models.Model):
    """Usage of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    usage = models.CharField(
        max_length=100,
        help_text="usage",
        blank=True,
    )

    def __str__(self):
        return self.usage

    class Meta:

        app_label = "tools_over"


class TargetGroup(models.Model):
    """TargetGroup of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    targetGroup = models.CharField(
        max_length=300,
        help_text="Which group of people is the tool targeted at?",
        blank=True,
    )

    def __str__(self):
        return self.targetGroup

    class Meta:

        app_label = "tools_over"


class LifeCyclePhase(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    lifeCyclePhase = models.CharField(
        max_length=100,
        help_text="Life cycle phase of buildings where the application is used",
        blank=True,
    )

    def __str__(self):
        return self.lifeCyclePhase

    class Meta:

        app_label = "tools_over"


class UserInterface(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    userInterface = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )

    def __str__(self):
        return self.userInterface

    class Meta:
        app_label = "tools_over"


class Accessibility(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    accessibility = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )

    def __str__(self):
        return self.accessibility

    class Meta:

        app_label = "tools_over"


class Scale(models.Model):
    """Scale of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """

    scale = models.CharField(
        max_length=100,
        help_text="spatial scope of consideration",
        blank=True,
    )

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

    def get_fields(self):
        """Returns a list of field names and values for use in templates."""
        return [field.name for field in self._meta.get_fields()]

    def getManyToManyAttrAsStr(self, manyToManyAttr, languageSuffix):
        """ """
        querysetOfManyToManyElements = getattr(self, manyToManyAttr).all()
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
                    returnStr += getattr(element, field) + ", "
            else:
                returnStr += element.__str__() + ", "
        return returnStr[:-2]

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
