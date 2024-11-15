"""Models, which can be used in all other apps of the projects.

"""

from django.db import models


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


