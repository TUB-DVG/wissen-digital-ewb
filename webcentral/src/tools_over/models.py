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
