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
    License,
    AbstractTechnicalFocus,
    AbstractHistory,
)


class ToolManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(
            name=name,
        )


class Tools(AbstractTechnicalFocus):
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        db_comment="What do the developers describe as the area of application of their digital tool",
    )
    usage = models.ManyToManyField(Usage)

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
    lastUpdate = models.CharField(
        max_length=100,
        help_text="time (year/month/date) of the last update",
        blank=True,
    )

    licenseNotes = models.CharField(
        max_length=500, help_text="license notes", blank=True
    )

    releasedPlanned = models.BooleanField(
        blank=True,
        null=True,
        help_text="whether publication is planned",
    )

    frameworksLibraries = models.CharField(
        max_length=500,
        blank=True,
    )
    databaseSystem = models.CharField(
        max_length=500,
        blank=True,
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
    programmingLanguages = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        db_comment="Programming languages - Which programming languages are mainly used to implment the item.",
    ) 
    @property
    def imageOrDefault(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        else:
            return "{% static 'assets/default.jpg' %}"

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

    objects = ToolManager()

    class Meta:
        app_label = "tools_over"


class History(AbstractHistory):
    """model class to store updates of the Tools model"""
