from django.db import models

class Teilprojekt(models.Model):
    fkz = models.CharField(max_length=10, primary_key=True)
    # when  there is a problem try related_name
    enargus_daten = models.ForeignKey('Enargus', null=True, on_delete=models.DO_NOTHING)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.fkz  # maybe change to the shortname of the project


class Enargus(models.Model):
    enargus_id = models.AutoField(primary_key=True)
    laufzeitbeginn = models.DateTimeField(blank=True)
    laufzeitende = models.DateTimeField(blank=True)
    thema = models.CharField(max_length=500, blank=True)
    verbundbezeichnung = models.CharField(max_length=200, blank=
                                          True)
    # forschung = models.ForeignKey('Forschung', null=True, on_delete=models.DO_NOTHING)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.verbundbezeichnung  # maybe change to the shortname of the project



# class Forschung(models.Model):
#     forschung_id = models.AutoField(primary_key=True)
#     bundesministerium = models.CharField(max_length=10, blank=True)
