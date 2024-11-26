"""Models, which can be used in all other apps of the projects.

"""

from django.db import models
from project_listing.models import Subproject
from django.db.models.functions import Now
from django.utils.translation import gettext as _


class DbDiff(models.Model):
    """ORM-model definition of the `DBDiff`, which is instanciated if
    data conflicts appear in the data_import-process.

    """

    identifier = models.CharField(max_length=100)
    diffStr = models.TextField()
    executed = models.BooleanField(default=False)


class Literature(models.Model):
    """Definition of the Literature-ORM class, which is used in the apps
    `user_integration`, `positive_environemntal_impact` and `data_sufficiency`
    """

    literature = models.TextField()
    linkName = models.CharField(max_length=255, blank=True, null=True)

    # authors = models.CharField(max_length=500)
    # publication_year = models.IntegerField(blank=True, null=True)
    # publication_title = models.CharField(max_length=500)
    # publisher = models.CharField(max_length=500, blank=True, null=True)
    # publication_location = models.CharField(max_length=500,
    #                                         blank=True,
    #                                         null=True)
    def __str__(self):
        return str(self.literature)


class License(models.Model):
    """ORM-class containing license information of tools, datasets, norms and protocols"""

    license = models.CharField(max_length=300, null=True, blank=True)
    openSourceStatus = models.CharField(
        max_length=50,
        help_text="Open-Source-Status (Ob Spezifikationen öffentlich und frei verfügbar sind oder nicht)",
        blank=True,
        null=True,
    )
    licensingFeeRequirement = models.CharField(
        max_length=150,
        help_text="Lizenzgebühr (Gebühr zur Abdeckung der Kosten für Tests und Zertifizierung)",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.license)


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


class History(models.Model):
    """Abstract model class for the history models in each app."""

    identifer = models.CharField(max_length=300)
    stringifiedObj = models.TextField()
    loaded = models.BooleanField(default=False)
    updateDate = models.DateTimeField(db_default=Now())

    class Meta:
        abstract = True


class AbstractTechnicalFocus(models.Model):
    """Abstract model, which holds the attributes, which are all present in the
    models Tools, Protocol, Dataset and Norm

    """

    name = models.CharField(max_length=200, db_comment="Name of the item")
    focus = models.ManyToManyField(
        Focus,
        max_length=200,
        db_comment="Focus identifier - Selected focus (Definied by Wissensplattform)",
    )
    classification = models.ManyToManyField(
        Classification,
        db_comment="General type of dataset - Which type or of to which typ belongs the dataset. E.g. framework, programming language, ...",
    )
    lifeCyclePhase = models.ManyToManyField(
        LifeCyclePhase,
        db_comment="Life cycle phase - In which phase of the product life cycle is the tool used?",
    )
    scale = models.ManyToManyField(
        Scale,
        db_comment="Spatial scale of the use cases - On what scale is the dataset used?",
    )
    targetGroup = models.ManyToManyField(
        TargetGroup,
        db_comment="Target group - Who do you say the digital item is aimed at?",
    )
    alternatives = models.CharField(
        max_length=300,
        help_text="Alternatives - Items with equal or likewise use case.",
        blank=True,
        null=True,
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
        db_comment="Level of development - What is the curent development status",
    )
    furtherInformation = models.CharField(
        max_length=1200,
        null=True,
        blank=True,
        db_comment="Further information - Information of miscellaneous subjects",
    )

    image = models.ImageField(
        null=True,
        blank=True,
        db_comment="File name of image file. Located in media-folder.",
    )
    released = models.BooleanField(
        blank=True,
        null=True,
        db_comment="Released - Is the publication done?",
    )
    license = models.ManyToManyField(
        License,
        db_comment="under which license was the item published and are there any costs associated with using the dataset?",
    )
    accessibility = models.ManyToManyField(
        Accessibility,
        db_comment="Accessibility - How accessible is the dataset?",
    )
    programmingLanguages = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        db_comment="Programming languages - Which programming languages are mainly used to implment the item.",
    )
    provider = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_comment="Developers/maintainers/provider - Person or organisation responsible for the development of the item.",
    )
    resources = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        db_comment="Sources of information - sources for further information about the item e.g. git repo, project website, ...",
    )
    description = models.CharField(
        max_length=1100,
        null=True,
        blank=True,
        db_comment="Description of the item",
    )
    specificApplication = models.ManyToManyField(
        Subproject,
        blank=True,
        db_comment="Specific use cases - Identification of concrete examples of the use of the item in the construction sector/energy transition (equals project number)",
    )
    yearOfRelease = models.CharField(
        blank=True,
        max_length=100,
        help_text="year of software release (planned or conducted)",
        db_comment="Year of publication - If the item is published, in which year was it released?",
        null=True,
    )

    @property
    def devStateStr(self):
        """Return the string, which is meant by the number in the database

        1 : pre-Alpha
        2 : Alpha
        3 : Beta
        4 : Release Canditate
        5 : Release
        """
        mappingDict = {
            1: "pre-Alpha",
            2: "Alpha",
            3: "Beta",
            4: _("Veröffentlichungskandidat"),
            5: _("Veröffentlicht"),
        }

        if self.developmentState is None:
            return "n/a"
        return mappingDict[self.developmentState]

    class Meta:
        abstract = True
