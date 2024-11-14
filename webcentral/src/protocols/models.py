from django.db import models

from tools_over.models import (
    Tools,
    Classification,
    Focus,
    ApplicationArea,
    LifeCyclePhase,
    Scale,
    TargetGroup,
    Accessibility,
)
from common.models import License
from project_listing.models import Subproject
from TechnicalStandards.models import Norm


class Protocol(models.Model):
    name = models.CharField(
        max_length=150, help_text="name of the norm", blank=True
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
        db_comment="General type of protocol - Which type or of to which typ belongs the dataset. E.g. framework, programming language, ...",
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
    released = models.BooleanField(
        blank=True,
        null=True,
        db_comment="Released - Is the publication done?",
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
        db_comment="Sources of information - sources for further information about the item e.g. git repo, project website, ...",
    )
    license = models.ManyToManyField(
        License,
        db_comment="under which license was the protocol published and are there any costs associated with using the protocol?",
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
    description = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        db_comment="Description of the item",
    )
    specificApplication = models.ManyToManyField(
        Subproject,
        blank=True,
        null=True,
        db_comment="Specific use cases - Identification of concrete examples of the use of the item in the construction sector/energy transition (equals project number)",
    )
    technicalStandardsNorms = models.ManyToManyField(
        Norm,
        blank=True,
        null=True,
        db_comment="Norms - Which norms serve as the basis or orientation for the item?",
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
    tools = models.ManyToManyField(Tools, db_comment="Relation to tools")
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
    )
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
