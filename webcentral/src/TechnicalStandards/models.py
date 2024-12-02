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
    AbstractHistory,
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


class History(AbstractHistory):
    """model class to store updates of the Tools model"""
