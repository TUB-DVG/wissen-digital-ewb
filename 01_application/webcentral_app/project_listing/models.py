from pyexpat import model
from typing import ValuesView
from django.db import models
from django.db import IntegrityError
from django.forms import CharField
from keywords.models import *

from sqlalchemy import null, true
class Subproject(models.Model):
    referenceNumber_id=models.CharField(
        max_length=10,
        primary_key=True,
        help_text="Funding code (numerical sequence of 9 to 10 characters), fkz - Förderkennzeichen")
    # when  there is a problem try related_name
    enargusData=models.OneToOneField('Enargus',
                                         null=True,
                                         on_delete=models.CASCADE) # Set to cascade since this is a one to one relation.
    #projektlandkarte

    moduleAssignment=models.ForeignKey('ModuleAssignment',null=true,on_delete=models.SET_NULL,blank=True) # One to many behaviour
    keywordsFirstReview=models.ForeignKey("keywords.KeywordRegisterFirstReview", null=true, on_delete=models.SET_NULL,blank=True) # One to many behaviour
    questionnaire2021=models.ForeignKey("Questionnaire2021",null=true,on_delete=models.SET_NULL,blank=True) # One to many behaviour

    # foerdersumme move to Enargus table, here for testing
    #foerdersumme = models.IntegerField(help_text='Foerdersumme in EUR', null=True)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.referenceNumber_id  # maybe change to the shortname of the project
    #def en_id(self):
     #   return self.enargus_daten.enargus_id

class Questionnaire2021(models.Model):
        Questionnaire2021=models.AutoField(primary_key=True ,help_text="auto generiert ID")

class ModuleAssignment(models.Model):
    moduleAssignment_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    priority1=models.CharField(max_length=2,null=True, blank=True,help_text="Project allocation with priority 1 (main contact partner) e.g. M2, M1, ag: ausgelaufen")
    priority2=models.CharField(max_length=2,null=True, blank=True,help_text="Project allocation with priority 2 (main contact partner) e.g. M2, M1, ag: ausgelaufen")
    priority3=models.CharField(max_length=2,null=True, blank=True,help_text="Project allocation with priority 3 (main contact partner) e.g. M2, M1, ag: ausgelaufen")
    priority4=models.CharField(max_length=2,
                 help_text="Project allocation with priority 4 (main contact partner) e.g. M2, M1, ag: ausgelaufen",
                 null=True, blank=True)

class Enargus(models.Model):
    enargus_id=models.AutoField(primary_key=True)
    startDate=models.DateField(blank=True,null=True)
    endDate=models.DateField(blank=True,null=True)
    topics=models.CharField(max_length=500, 
                              help_text="title of the subproject, incl. acronym",blank=True,null=True)
    collaborativeProject=models.CharField(max_length=200, help_text="title of the joint project, including acronym",
                                            blank=True,null=True)
    furtherFundingInformation=models.ForeignKey("FurtherFundingInformation", null=True,
                                  on_delete=models.SET_NULL,blank=True)
    projectLead=models.ForeignKey("Person", null = True,
                                     on_delete=models.SET_NULL,blank=True)
    database=models.CharField(max_length=15,
                                help_text="database information from EnArgus internal usage",
                                default=null,null=True,blank=True)
    shortDescriptionDe=models.TextField(help_text="short description in German",
                                         default=null,null=True,blank=True)
    shortDescriptionEn=models.TextField(help_text="short description in English",
                                         default=null,null=True,blank=True)
    rAndDPlanningCategory=models.ForeignKey("RAndDPlanningCategory",
                                            help_text="number of the systematic performance plan ('leistungsplan systematik')",
                                            null=True,
                                            on_delete=models.SET_NULL,
                                            blank=True)
    grantRecipient=models.ForeignKey("GrantRecipient", help_text="recipient organization, to which the funding is granted",
                                       null =True,
                                       on_delete=models.SET_NULL,blank=True)
    executingEntity=models.ForeignKey("ExecutingEntity",help_text="name of the organization which executes the project",
                                            null =True,
                                            on_delete=models.SET_NULL,
                                            blank=True)
    appropriatedBudget=models.DecimalField(help_text="amount of funding in Euros",blank=True,max_digits=12,
                                       decimal_places=2,null=True)

    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.collaborativeProject  # maybe change to the shortname of the project



class FurtherFundingInformation(models.Model):
    furtherFundingInformation_id=models.AutoField(primary_key=True,help_text="Auto.generiert ID")
    fundedBy=models.CharField(max_length=10, null= True,blank=True,help_text="Akronym des Bundesministeriums")
    projectManagementAgency=models.CharField(max_length=50, null= True,blank=True,help_text="Name des Projektraegers")
    researchProgram=models.CharField(max_length=50,null= True, blank=True,help_text="Name des Forschungsprogramms")
    fundingProgram=models.CharField(max_length=50, null= True,blank=True,help_text="Name des Forderprogramms")

class RAndDPlanningCategory(models.Model):
    rAndDPlanningCategoryNumber=models.CharField(
                                                primary_key=True,
                                                max_length= 6,
                                                help_text="identifier number of the performance plan systematic - 'Leistungsplansystematiknummer'")
    rAndDPlanningCategoryText=models.CharField(max_length=150)
    #def __str__(self):
    #    return self.rAndDPlanningCategoryNumber 

class ExecutingEntity(models.Model):
    executingEntity_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    name=models.CharField(max_length=250)
    address=models.ForeignKey("Address",null= true,on_delete=models.SET_NULL,blank=True) #If address is deleted no need to delete this entry, just set to NULL

class GrantRecipient(models.Model):
    grantRecipient_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    name=models.CharField(max_length=250)
    address=models.ForeignKey("Address",null= True,on_delete=models.SET_NULL,blank=True)# If address is deleted no need to delete this entry, just set to NULL

class Person(models.Model):
    person_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    surname=models.CharField(max_length=100,help_text="family name",null= True)
    firstName=models.CharField(max_length=50,help_text="name",null= True)
    title=models.CharField(max_length=50, help_text="title of the person",null= True)
    email=models.EmailField(help_text="Email Address",null= True)

class Address(models.Model):
    address_id=models.AutoField(primary_key=True,help_text="auto generiert ID")
    plz=models.CharField(max_length=5,null= True)
    location=models.CharField(max_length=50,null= True)
    state=models.CharField(max_length=50,null= True)
    address=models.CharField(max_length=150,null= True)
