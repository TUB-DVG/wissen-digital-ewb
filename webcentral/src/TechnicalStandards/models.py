from django.db import models
from django.contrib.auth.models import User

from common.models import (
    ApplicationArea,
    Focus,
    LifeCyclePhase,
    Scale,
    TargetGroup,
    Accessibility,
    Classification,
    License,
    Usage,
)
from project_listing.models import Subproject


class Norm(models.Model):
    # isNorm = models.BooleanField(default=True)
    name = models.CharField(
        max_length=150,
        help_text="name of the norm",
        blank=True,
        db_comment="Name of the item",
    )
    resources = models.CharField(
        max_length=1000,
        help_text="link",
        blank=True,
        db_comment="Sources of information - sources for further information about the item e.g. git repo, project website, ...",
    )

    title = models.CharField(
        max_length=250,
        help_text="title of the norm",
        blank=True,
        db_comment="full title  of the norm",
    )
    description = models.TextField(
        max_length=1000,
        help_text="short description",
        default=None,
        blank=True,
        null=True,
        db_comment="Description of the item.",
    )
    source = models.CharField(max_length=100, help_text="source", blank=True)

    applicationArea = models.ManyToManyField(
        ApplicationArea,
        db_comment="Typical application area in which the item is used.",
    )
    classification = models.ManyToManyField(
        Classification,
        db_comment="General type of item - Which type or of to which typ belongs the item. E.g. framework, programming language, ...",
    )
    focus = models.ManyToManyField(
        Focus,
        max_length=200,
        db_comment="Focus identifier - Selected focus (Definied by Wissensplattform)",
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
        db_comment="Alternatives - items with equal or likewise use case.",
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
        db_comment="under which license was the dataset published and are there any costs associated with using the dataset?",
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
    usage = models.ManyToManyField(
        Usage,
        db_comment="Use type - What purpose is the item used for? (Simulation, monitoring, optimization, planning, control advanced control)",
    )

    def __str__(self):
        return self.name
