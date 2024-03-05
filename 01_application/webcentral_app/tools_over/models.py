from django.db import models

from project_listing.models import Subproject
from TechnicalStandards.models import (
    Norm,
    Protocol,
)

class Classification(models.Model):
    """Model for 
    
    """
    classification = models.CharField(
        max_length=100,
        help_text="Classification Category",    
    )

    def __str__(self):
        return self.classification

    class Meta:

        app_label = 'tools_over'


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

        app_label = 'tools_over'

class ApplicationArea(models.Model):
    """ApplicationArea of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    applicationArea = models.CharField(
        max_length=1000,
        help_text="application area",
        blank=True,
    )
    class Meta:
        app_label = 'tools_over'

class Usage(models.Model):
    """Usage of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    usage = models.CharField(
        max_length=100,
        help_text="usage",
        blank=True,
    )
    class Meta:

        app_label = 'tools_over'

class TargetGroup(models.Model):
    """TargetGroup of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    targetGroup = models.CharField(
        max_length=300,
        help_text="Which group of people is the tool targeted at?",
        blank=True,
    )
    class Meta:

        app_label = 'tools_over'

class LifeCyclePhase(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    lifeCyclePhase = models.CharField(
        max_length=100,
        help_text="Life cycle phase of buildings where the application is used",
        blank=True,
    )
    class Meta:

        app_label = 'tools_over'

class UserInterface(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    userInterface = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )
    class Meta:
        app_label = 'tools_over'


class Accessibility(models.Model):
    """LifeCyclePhase of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    accessibility = models.CharField(
        max_length=300,
        help_text="userInterface",
        blank=True,
    )
    class Meta:

        app_label = 'tools_over'

class Scale(models.Model):
    """Scale of the Tool-Items

    This Model has a ManyToMany-Relationship to Tools
    """
    scale = models.CharField(
        max_length=100,
        help_text="spatial scope of consideration",
        blank=True,
    )
    class Meta:

        app_label = 'tools_over'

class Tools(models.Model):
    name = models.CharField(max_length = 150,
                                   help_text="name",
                                   blank = True)
    shortDescription = models.CharField(max_length = 1000,
                                   help_text = "short description",
                                   blank = True)
    applicationArea = models.ManyToManyField(ApplicationArea)
    usage = models.ManyToManyField(Usage)
    targetGroup = models.ManyToManyField(TargetGroup)
    lifeCyclePhase  = models.ManyToManyField(LifeCyclePhase)
    userInterface = models.ManyToManyField(UserInterface)
    userInterfaceNotes = models.CharField(
        max_length=300,
        help_text="additional notes for userInterface",
        blank=True,
    )
    accessibility = models.ManyToManyField(Accessibility)
    lastUpdate = models.CharField(max_length = 100,
                                  help_text = "time (year/month/date) of the last update",
                                  blank = True)
    license = models.CharField(max_length = 500,
                              help_text = "license",
                              blank = True)
    licenseNotes = models.CharField(max_length = 500,
                              help_text = "license notes",
                              blank = True)                              
    furtherInformation = models.CharField(max_length = 500,
                                          help_text = "further information",
                                          blank = True)
    alternatives = models.CharField(max_length = 300,
                                    help_text = "similar tool(s) that can serve as alternatives",
                                    blank = True)
    specificApplication = models.ManyToManyField(
        Subproject,
        help_text = "specific application of the tool in EWB projects (project name + fkz)",
    )
    
    # models.CharField(max_length = 500,
                                        #   help_text = "specific application of the tool in EWB projects (project name + fkz)",
                                        #   blank = True)
    provider = models.CharField(
        max_length=300,
        blank=True,
    )
    released = models.BooleanField(
        blank=True,
        null=True,
        help_text = "whether the tool is released or not",
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
    scale = models.ManyToManyField(Scale)

    technicalStandardsNorms = models.ManyToManyField(Norm)
    technicalStandardsProtocols = models.ManyToManyField(Protocol)
    #image=models.ImageField(default="webcentral_app/tools_over/Media/Default.webp", null=True,blank = True)  #You need to install pillow
    image = models.ImageField(
        null=True,
        blank = True,
    )  #You need to install pillow

    classification = models.ManyToManyField(Classification) 
    focus = models.ManyToManyField(Focus)
    
    class Meta:
        app_label = 'tools_over'



