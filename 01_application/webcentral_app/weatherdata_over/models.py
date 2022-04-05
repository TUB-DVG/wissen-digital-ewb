from django.db import models

# Create your models here.

class Weatherdata(models.Model):
    data_service = models.CharField(max_length = 150,
                                   help_text="Name der Anwendung",
                                   blank = True)
    short_description = models.CharField(max_length = 1000,
                                   help_text = "Kurzbeschreibung des DatenService",
                                   blank = True)
    provider = models.CharField(max_length = 150,
                                         help_text = "Provider des DatenService",
                                         blank=True)
    further_information = models.CharField(max_length = 500,
                                        help_text = "weitere Informationen zum DatenService",
                                        blank = True)
    data_url = models.CharField(max_length = 300,
                                         help_text = "Url zu Datensatz",
                                         blank = True)
    logo_url = models.CharField(max_length = 300,
                                           help_text = "Logo url",
                                           blank = True)
    applications = models.CharField(max_length = 500,
                                     help_text = "Anwendung in EWB Projekten",
                                     blank = True)
    last_update = models.CharField(max_length = 100,
                                      help_text = "letztes Update des DatenServices",
                                      blank = True)
    license = models.CharField(max_length = 200,
                              help_text = "Lizenz des DatenServices",
                              blank = True)
    category = models.CharField(max_length = 150,
                                help_text = "Kategorie des DatenServices (Datensatz, Anwendung, ...)",
                                blank = True)
    long_description = models.CharField(max_length = 10000,
                                   help_text = "Beschreibung des DatenService",
                                   blank = True)