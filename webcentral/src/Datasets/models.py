from django.db import models

from tools_over.models import (
    ApplicationArea,
    Focus,
    LifeCyclePhase,
    Scale,
    TargetGroup,
)
from common.models import License
from project_listing.models import Subproject


class collectedDatasets(models.Model):

    name = models.CharField(max_length=200, db_comment="Name of the dataset")
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        max_length=200,
        null=True,
        db_comment="Typical application area in which the dataset is used. An application area describes all possible methods and datasets, that can be used to achieve a specific purpose.",
    )
    focus = models.ManyToManyField(
        Focus,
        max_length=200,
        null=True,
        db_comment="Typical application area in which the dataset is used. An application area describes all possible methods and datasets, that can be used to achieve a specific purpose.",
    )
    classification = models.CharField(
        max_length=200,
        null=True,
        db_comment="General type of dataset - Which category does the data set belong to?",
    )
    lifeCyclePhase = models.ManyToManyField(
        LifeCyclePhase,
        db_comment="In which phase of the product life cycle is the tool used?",
    )
    scale = models.ManyToManyField(
        Scale,
        db_comment="Spatial scale of the use cases - On what scale is the dataset used?",
    )
    targetGroup = models.ManyToManyField(
        TargetGroup, db_comment="Which user group the dataset is aimed for."
    )
    alternatives = models.CharField(
        max_length=300,
        db_comment="Identification of concrete examples of the use of datasets in the construction sector/energy transition construction (e.g. funding indicators)",
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

    provider = models.CharField(max_length=300, null=True, blank=True)
    resources = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        db_comment="Sources of information - sources for further information about the dataset e.g. git repo, project website, ...",
    )
    availability = models.CharField(
        max_length=200, null=True, db_comment="How accessible is the dataset?"
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
    # comment = models.CharField(max_length=200, null=True, blank=True)
    # dataSources = models.CharField(max_length=500, null=True, blank=True)
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
        db_comment="information of miscellaneous subjects",
    )

    # includesNonResidential = models.CharField(
    #     max_length=200, null=True, blank=True
    # )

    license = models.ManyToManyField(
        License,
        db_comment="under which license was the dataset published and are there any costs associated with using the dataset?",
    )
    licenseNotes = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_comment="",
    )

    image = models.ImageField(
        null=True,
        blank=True,
    )
    lastUpdate = models.CharField(
        max_length=100,
        help_text="time (year/month/date) of the last update",
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

    specificApplication = models.ManyToManyField(
        Subproject,
        help_text="specific application of the dataset in EWB projects (fkz)",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
