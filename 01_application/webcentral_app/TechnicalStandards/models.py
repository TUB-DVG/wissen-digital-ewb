from django.db import models
from django.contrib.auth.models import User

class TechnicalStandard(models.Model):
    isNorm = models.BooleanField(default=True)
    name = models.CharField(max_length = 150,
                                   help_text="name of the norm",
                                   blank = True)
    link = models.CharField(max_length = 150,
                                         help_text = "link",
                                         blank = True)
    class Meta:
        abstract = True # tells Django not to create a database table
    def __str__(self):
        return self.name
    
class Norm(TechnicalStandard):
    title = models.CharField(max_length = 250,
                                         help_text = "title of the norm",
                                         blank=True)
    shortDescription = models.TextField(max_length = 600,
                                   help_text = "short description")
    source = models.CharField(max_length = 100,
                                 help_text = "source",
                                 blank = True)
    def __str__(self):
        return self.name
    
class Protocol(TechnicalStandard):
    communicationMediumCategory = models.CharField(max_length = 150,
                                   help_text="Übertragungsmethoden (verkabelt, drahtlos oder verkabelt und drahtlos)",
                                   blank = True)
    supportedTransmissionMediuems = models.CharField(max_length = 150,
                                         help_text = "Unterstützte Übertragungsmedien",
                                         blank = True)
    associatedStandards = models.CharField(max_length = 200,
                                         help_text = "Zugehörige Standards (Spezifische Standards, denen jedes Protokoll entspricht)",
                                         blank = True)
    openSourceStatus = models.CharField(max_length = 50,
                                         help_text = "Open-Source-Status (Ob Spezifikationen öffentlich und frei verfügbar sind oder nicht)",
                                         blank = True)
    licensingFeeRequirement = models.CharField(max_length = 150,
                                        help_text = "Lizenzgebühr (Gebühr zur Abdeckung der Kosten für Tests und Zertifizierung)",
                                        blank = True)
    networkTopology = models.CharField(max_length = 150,
                                         help_text = "Netzwerktopologie (Physische und logische Anordnung von Geräten in einem Netzwerk)",
                                         blank = True)
    security = models.CharField(max_length = 150,
                                         help_text = "Implementierte Sicherheitmechanismen",
                                         blank = True)
    bandwidth = models.CharField(max_length = 150,
                                        help_text = "Bandbreite",
                                        blank = True)
    frequency = models.CharField(max_length = 100,
                                         help_text = "Frequenz",
                                         blank = True)
    range = models.CharField(max_length = 150,
                                         help_text = "Reichweite",
                                         blank = True)
    numberOfConnectedDevices = models.CharField(max_length = 5,
                                         help_text = "Geräte (maximale Anzahl an Geräten, die vernetzt werden können)",
                                         blank = True)
    dataModelArchitecture = models.CharField(max_length = 150,
                                        help_text = "Datenmodell Architektur (Datenmodell, in dem die Informationen/Attribute zu einem Objekt hinzugefügt werden)",
                                        blank = True)
    discovery = models.CharField(max_length = 10,
                                 help_text = "Discovery (Funktion, um Geräte im Netzwerk automatisch zu identifzieren)",
                                         blank = True) 
    # if BooleanField shall be used: input in the .csv should be True/False
    multiMaster = models.CharField(max_length = 10,
                                   help_text = "Multi Master (Können mehrere Mastergeräte zeitgleich agieren)",
                                         blank = True)
    # if BooleanField shall be used: input in the .csv should be True/False
    packetSize = models.CharField(max_length = 10,
                                        help_text = "Paketgröße (Datenpaketgröße, die nach Maximum Transmission Unit übertragen werden können)",
                                        blank = True)
    priorities = models.CharField(max_length = 100,
                                         help_text = "Prorität (Vorgehen, wie die Änderungen / Aktualisierungen vorgenommen werden)",
                                         blank = True)
    price = models.CharField(max_length = 150,
                                         help_text = "Kosten, um Hardwareuntersützung für weitere Protokolle zu ermöglichen (Gering, Durchschnittlich, Hoch)",
                                         blank = True)
    osiLayers = models.CharField(max_length = 150,
                                        help_text = "Implementierte OSI-Schichten (Anwendung [Application], Darstellung [Presentation], Sitzung [Session], Transport [Transport], Vermittlung/Paket [Network], Sicherung [Data Link], Bitübertragung [Phyiscal])",
                                        blank = True)
    buildingAutomationLayer = models.CharField(max_length = 150,
                                        help_text = "Ebenen der Gebäudeautomation (Feldebene, Automationsebene, Managementebene)",
                                        blank = True)	
    image=models.ImageField(null=True, blank = True)  

    def __str__(self):
        return self.name



