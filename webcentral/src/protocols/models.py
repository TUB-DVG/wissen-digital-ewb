from django.db import models
from django.db.models.functions import Now

from common.models import (
    Accessibility,
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    Scale,
    LifeCyclePhase,
    TargetGroup,
    License,
    AbstractTechnicalFocus, 
)
from project_listing.models import Subproject
from TechnicalStandards.models import Norm


class Protocol(AbstractTechnicalFocus):

    technicalStandardsNorms = models.ManyToManyField(
        Norm,
        blank=True,
        db_comment="Norms - Which norms serve as the basis or orientation for the item?",
    )
    # yearOfRelease = models.CharField(
    #     blank=True,
    #     max_length=100,
    #     help_text="year of software release (planned or conducted)",
    #     db_comment="Year of publication - If the item is published, in which year was it released?",
    #     null=True,
    # )
    usage = models.ManyToManyField(
        Usage,
        db_comment="Use type - What purpose is the item used for? (Simulation, monitoring, optimization, planning, control advanced control)",
    )
    # associatedTools = models.ManyToManyField(Tools, db_comment="Relation to tools")
    communicationMediumCategory = models.CharField(
        max_length=150,
        help_text="Übertragungsmethoden (verkabelt, drahtlos oder verkabelt und drahtlos)",
        blank=True,
        db_comment="Transmission category - How is data transfered between the various components and devices within the system (wired, wireless or wired & wireless)",
    )
    supportedTransmissionMediuems = models.CharField(
        max_length=150,
        help_text="Unterstützte Übertragungsmedien",
        blank=True,
        db_comment="Supported transmission media - how are signals transmitted?",
    )
    associatedStandards = models.CharField(
        max_length=200,
        help_text="Zugehörige Standards (Spezifische Standards, denen jedes Protokoll entspricht)",
        blank=True,
    )

    networkTopology = models.CharField(
        max_length=150,
        help_text="Netzwerktopologie (Physische und logische Anordnung von Geräten in einem Netzwerk)",
        blank=True,
        db_comment="Network topology - what is the physical and logical arrangement of devices and components in a network?",
    )
    security = models.CharField(
        max_length=150,
        help_text="Implementierte Sicherheitmechanismen",
        blank=True,
        db_comment="Implemented security mechanisms - whether and what mechanisms are implemented in the protocol to ensure data security?",
    )
    bandwidth = models.CharField(
        max_length=150,
        help_text="Bandbreite",
        blank=True,
        db_comment="Bandwidth - The capacity of the communication channel to transmit data between the various components of the system.",
    )
    frequency = models.CharField(
        max_length=100, help_text="Frequenz", blank=True
    )
    range = models.CharField(
        max_length=150,
        help_text="Reichweite",
        blank=True,
        db_comment="Range - the maximum distance over which communication can be mainained between the various devices and components of the system without the signal strength becoming to weak.",
    )
    numberOfConnectedDevices = models.CharField(
        max_length=5,
        help_text="Geräte (maximale Anzahl an Geräten, die vernetzt werden können)",
        blank=True,
        db_comment="Maximum devices - maximum number of simultaneous connected devices.",
        null=True,
    )
    dataModelArchitecture = models.CharField(
        max_length=150,
        help_text="Datenmodell Architektur (Datenmodell, in dem die Informationen/Attribute zu einem Objekt hinzugefügt werden)",
        blank=True,
    )
    discovery = models.CharField(
        max_length=10,
        help_text="Discovery (Funktion, um Geräte im Netzwerk automatisch zu identifzieren)",
        blank=True,
    )
    # if BooleanField shall be used: input in the .csv should be True/False
    multiMaster = models.CharField(
        max_length=50,
        help_text="Multi Master (Können mehrere Mastergeräte zeitgleich agieren)",
        blank=True,
    )
    # if BooleanField shall be used: input in the .csv should be True/False
    packetSize = models.CharField(
        max_length=10,
        help_text="Paketgröße (Datenpaketgröße, die nach Maximum Transmission Unit übertragen werden können)",
        blank=True,
        null=True,
    )
    priorities = models.CharField(
        max_length=300,
        help_text="Priorität  (Vorgehen, wie die Änderungen / Aktualisierungen vorgenommen werden)",
        blank=True,
        db_comment="Priority - Procedure for how the changes or updates are made.",
    )
    price = models.CharField(
        max_length=150,
        help_text="Kosten, um Hardwareuntersützung für weitere Protokolle zu ermöglichen (Gering, Durchschnittlich, Hoch)",
        blank=True,
        null=True,
    )
    osiLayers = models.CharField(
        max_length=150,
        help_text="Implementierte OSI-Schichten (Anwendung [Application], Darstellung [Presentation], Sitzung [Session], Transport [Transport], Vermittlung/Paket [Network], Sicherung [Data Link], Bitübertragung [Phyiscal])",
        blank=True,
        db_comment="Implemented OSI-layer - the application of the layers of the OSI reference model for communication between the various components of the system.",
    )
    buildingAutomationLayer = models.CharField(
        max_length=150,
        help_text="Ebenen der Gebäudeautomation (Feldebene, Automationsebene, Managementebene)",
        blank=True,
        db_comment="Levels of building automation - the hierachical structure of building automation system.",
    )
    exampleProject = models.CharField(
        max_length=250,
        help_text="Typische Anwendung (Beispielhafte Anwendung)",
        blank=True,
        null=True,
    )
    # image = models.ImageField(null=True, blank=True)
    # programmingLanguages = models.CharField(
    #     max_length=500,
    #     blank=True,
    #     db_comment="Programming languages - Which programming languages are mainly used to implment the item.",
    #     null=True,
    # )

    def __str__(self):
        return self.name


class History(models.Model):
    """History model for the Dataset model. Implements a rollback feature for `Dataset`-model"""

    identifer = models.CharField(max_length=300)
    stringifiedObj = models.TextField()
    loaded = models.BooleanField(default=False)
    updateDate = models.DateTimeField(db_default=Now())
