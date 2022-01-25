from django.db import models
import csv
from django.db import IntegrityError
class Teilprojekt(models.Model):
    fkz = models.CharField(max_length=10, primary_key=True)
    # when  there is a problem try related_name
    enargus_daten = models.ForeignKey('Enargus', null=True,
                                      on_delete=models.DO_NOTHING)
    # foerdersumme move to Enargus table, here for testing
    foerdersumme = models.IntegerField(help_text='Foerdersumme in EUR', null=True)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.fkz  # maybe change to the shortname of the project


class Enargus(models.Model):
    enargus_id = models.AutoField(primary_key=True)
    laufzeitbeginn = models.DateField(blank=True)
    laufzeitende = models.DateField(blank=True)
    thema = models.CharField(max_length=500, blank=True)
    verbundbezeichnung = models.CharField(max_length=200, blank=
                                          True)
    forschung = models.ForeignKey('Forschung', null=True,
                                  on_delete=models.DO_NOTHING)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.verbundbezeichnung  # maybe change to the shortname of the project



class Forschung(models.Model):
    forschung_id = models.AutoField(primary_key=True)
    bundesministerium = models.CharField(max_length=10, blank=True)
    projekttraeger = models.CharField(max_length=50, blank=True)
    forschungsprogramm = models.CharField(max_length=50, blank=True)
    foerderprogramm = models.CharField(max_length=50, blank=True)

