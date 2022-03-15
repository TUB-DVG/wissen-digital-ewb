from pyexpat import model
from typing import ValuesView
from django.db import models
from django.db import IntegrityError
from django.forms import CharField

from sqlalchemy import null, true
class Teilprojekt(models.Model):
    fkz = models.CharField(
        max_length=10,
        primary_key=True,
        help_text= 'Förderkennzeichen')
    # when  there is a problem try related_name
    enargus_daten = models.OneToOneField('Enargus',
                                         null=True,
                                         on_delete=models.CASCADE)
    #projektlandkarte

    zuordnung=models.ForeignKey("Modulen_zuordnung_ptj",null=true,on_delete=models.SET_NULL,blank=True)

    schlagwoerter_erstsichtung=models.ForeignKey("Schlagwortregister_erstsichtung",null=true,on_delete=models.SET_NULL,blank=True)
    fragebogen_21=models.ForeignKey("Fragebogen_21",null=true,on_delete=models.SET_NULL,blank=True)


    # foerdersumme move to Enargus table, here for testing
    #foerdersumme = models.IntegerField(help_text='Foerdersumme in EUR', null=True)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.fkz  # maybe change to the shortname of the project

class Fragebogen_21(models.Model):
        Fragebogen_21=models.AutoField(primary_key=True ,help_text="auto generiert ID")



class Schlagwortregister_erstsichtung(models.Model):
    schlagwortregister_erstsichtung_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    schlagwort_1=models.ForeignKey("Schlagwort",related_name='schlagwort_1',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_2=models.ForeignKey("Schlagwort",related_name='schlagwort_2',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_3=models.ForeignKey("Schlagwort",related_name='schlagwort_3',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_4=models.ForeignKey("Schlagwort",related_name='schlagwort_4',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_5=models.ForeignKey("Schlagwort",related_name='schlagwort_5',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_6=models.ForeignKey("Schlagwort",related_name='schlagwort_6',null=True,on_delete=models.SET_NULL,blank=True)
    schlagwort_7=models.ForeignKey("Schlagwort",related_name='schlagwort_7',null=True,on_delete=models.SET_NULL,blank=True)





class Schlagwort (models.Model):
    schlagwort_id= models.CharField(max_length=200,help_text="Name des Schlagwortes")
    schlagwort_definition=models.CharField(max_length=1500,help_text="Definition des Schlagwortes")
    literatur=models.CharField(max_length=1500,help_text="Literaturquellen zum Schlagwort")




class Modulen_zuordnung_ptj(models.Model):
    mod_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    priority_1=models.CharField(max_length=2,help_text="Projektzuordnung mit der Prioritat 1, ag: ausgelaufen")
    priority_2=models.CharField(max_length=2,help_text="Projektzuordnung mit der Prioritat 2, ag: ausgelaufen")
    priority_3=models.CharField(max_length=2,help_text="Projektzuordnung mit der Prioritat 3, ag: ausgelaufen")
    priority_4=models.CharField(max_length=2,
                 help_text="Projektzuordnung mit der Prioritat 4, ag: ausgelaufen",
                 null=True, blank=True
                                )





class Enargus(models.Model):
    enargus_id = models.AutoField(primary_key=True)
    laufzeitbeginn = models.DateField(blank=True)
    laufzeitende = models.DateField(blank=True)
    thema = models.CharField(max_length=500, blank=True)
    verbundbezeichnung = models.CharField(max_length=200, blank=
                                          True)
    forschung = models.ForeignKey('Forschung', null=True,
                                  on_delete=models.SET_NULL,blank=True)
    projektleiter =models.ForeignKey('Person', null = True,
                                     on_delete=models.SET_NULL,blank=True)
    datenbank= models.CharField(max_length=15,
                                help_text="Datenbank Information/Enargus Intern",
                                default=null)
    kurzbeschreibung_de=models.TextField(help_text="Deutsche Kurzbeschreibung",
                                         default=null)
    kurzbeschreibung_en=models.TextField(help_text="Englische Kurzbeschreibung",
                                         default=null)
    leistungsplan_systematik=models.ForeignKey("Leistung_sys",
                                                null=True,
                                                on_delete=models.SET_NULL,
                                                blank=True)
    zuwendsempfanger = models.ForeignKey("Zuwendungsempfaenger", null =true,
                                       on_delete=models.SET_NULL,blank=True)
    ausfuehrende_stelle = models.ForeignKey("Ausfuehrende_stelle",
                                            null =true,
                                            on_delete=models.SET_NULL,
                                            blank=True
                                            )

    foerdersumme = models.DecimalField(help_text='Foerdersumme in EUR',
                                       null=True,blank=True, max_digits=10,
                                       decimal_places=2)

    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.verbundbezeichnung  # maybe change to the shortname of the project



class Forschung(models.Model):
    forschung_id = models.AutoField(primary_key=True,help_text="Auto.generiert ID")
    bundesministerium = models.CharField(max_length=10, blank=True,help_text="Akronym des Bundesministeriums")
    projekttraeger = models.CharField(max_length=50, blank=True,help_text="Name des Projektraegers")
    forschungsprogramm = models.CharField(max_length=50, blank=True,help_text="Name des Forschungsprogramms")
    foerderprogramm = models.CharField(max_length=50, blank=True,help_text="Name des Forderprogramms")




class Leistung_sys(models.Model):
    leistungsplansystematik_nr=models.CharField(
        primary_key=True,
        max_length= 6,
        help_text="Leistungsplansystematiknummer")
    leistungsplansystematik_text=models.CharField(max_length=150)


class Ausfuehrende_stelle(models.Model):
    ausfuehrende_stelle_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    name=models.CharField(max_length=250)
    anschrift=models.ForeignKey("Anschrift",null= true,on_delete=models.SET_NULL,blank=True)


class Zuwendungsempfaenger(models.Model):
    zuwendungsempfaenger_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    name=models.CharField(max_length=250)
    anschrift=models.ForeignKey("Anschrift",null= true,on_delete=models.SET_NULL,blank=True)



class Person(models.Model):
    person_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    name=models.CharField(max_length=100,help_text="Name der Person")
    vorname=models.CharField(max_length=50,help_text="Vorname der Person")
    titel=models.CharField(max_length=50, help_text="Titel der Person")
    email=models.EmailField(help_text="Email_Adresse der Person")

class Anschrift(models.Model):
    anschrift_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    plz=models.CharField(max_length=5)
    ort=models.CharField(max_length=50)
    land=models.CharField(max_length=50)
    adresse=models.CharField(max_length=150)


