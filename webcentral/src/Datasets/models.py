from django.db import models
from django.db.models.functions import Now

from tools_over.models import (
    ApplicationArea,
    Focus,
    LifeCyclePhase,
    Scale,
    TargetGroup,
    Accessibility,
    Classification,
)
from common.models import License
from project_listing.models import Subproject


class Dataset(models.Model):

    name = models.CharField(max_length=200, db_comment="Name of the dataset")
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        max_length=200,
        null=True,
        db_comment="Typical application area in which the dataset is used.",
    )
    focus = models.ManyToManyField(
        Focus,
        max_length=200,
        null=True,
        db_comment="Focus identifier - Selected focus (Definied by Wissensplattform)",
    )
    classification = models.ManyToManyField(
        Classification,
        null=True,
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
        TargetGroup, db_comment="Target group - Who do you say the digital item is aimed at?"
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
        db_comment="Sources of information - sources for further information about the dataset e.g. git repo, project website, ...",
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
    accessibility = models.ManyToManyField(
        Accessibility, db_comment="Accessibility - How accessible is the dataset?"
    )
    resolution = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_comment="Spatial resolution - spatial detail level of the data",
    )
    description = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_comment="Description of the dataset",
    )
    furtherInformation = models.CharField(
        max_length=1200,
        null=True,
        blank=True,
        db_comment="Further information - Information of miscellaneous subjects",
    )
    license = models.ManyToManyField(
        License,
        db_comment="under which license was the dataset published and are there any costs associated with using the dataset?",
    )
    licenseNotes = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_comment="Further information regarding the used license.",
    )
    image = models.ImageField(
        null=True,
        blank=True,
        db_comment="File name of image file. Located in media-folder.",
    )
    lastUpdate = models.CharField(
        max_length=100,
        db_comment="Last update - When was the last update done?",
        blank=True,
        null=True,
    )
    released = models.BooleanField(
        blank=True,
        null=True,
        db_comment="Released - Is the publication done?",
    )
    releasedPlanned = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether publication is planned",
        db_comment="Publication planned - If the item is not yet published, are there plans to publish it?",
    )
    yearOfRelease = models.CharField(
        blank=True,
        max_length=100,
        help_text="year of software release (planned or conducted)",
        db_comment="Year of publication - If the item is published, in which year was it released?",
        null=True,
    )
    
    programmingLanguages = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        db_comment="Programming languages - Which programming languages are mainly used to implment the item.",
    )
    specificApplication = models.ManyToManyField(
        Subproject,
        blank=True,
        null=True,
        db_comment="Specific use cases - Identification of concrete examples of the use of the item in the construction sector/energy transition (equals project number)"
    )


    def __str__(self):
        return self.name

class HistoryDataset(models.Model):
    """History model for the Dataset model. Implements a rollback feature for `Dataset`-model

    """
    identifer = models.CharField(max_length=300)
    stringifiedObj = models.TextField()
    loaded = models.BooleanField(default=False)
    updateDate = models.DateTimeField(db_default=Now())
