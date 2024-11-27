from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now

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
    AbstractTechnicalFocus,
)
from project_listing.models import Subproject


class Norm(
    AbstractTechnicalFocus,
):
    title = models.CharField(
        max_length=250,
        help_text="title of the norm",
        blank=True,
        db_comment="full title  of the norm",
    )
    applicationArea = models.ManyToManyField(
        ApplicationArea,
        db_comment="Typical application area in which the item is used.",
    )

    usage = models.ManyToManyField(
        Usage,
        db_comment="Use type - What purpose is the item used for? (Simulation, monitoring, optimization, planning, control advanced control)",
    )

    def __str__(self):
        return self.name


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
