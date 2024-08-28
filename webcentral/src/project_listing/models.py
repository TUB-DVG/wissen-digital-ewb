"""This module creates the Django ORM-models for the `Subproject` and 
subsequent models.

"""

from django.db import models
from sqlalchemy import null, true


class Subproject(models.Model):
    """ORM-Model Defintion for the Subproject model

    """
    referenceNumber_id = models.CharField(
        max_length=10,
        primary_key=True,
        help_text="""Funding code (numerical sequence of 9 to 10 characters),
            fkz - Förderkennzeichen""",
    )
    # when  there is a problem try related_name
    enargusData = models.OneToOneField(
        "Enargus", null=True, on_delete=models.CASCADE
    )  # Set to cascade since this is a one to one relation.
    # projektlandkarte

    moduleAssignment = models.ForeignKey(
        "ModuleAssignment", null=true, on_delete=models.SET_NULL, blank=True
    )  # One to many behaviour
    keywordsFirstReview = models.ForeignKey(
        "keywords.KeywordRegisterFirstReview",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
    )  # One to many behaviour

    def __str__(self):
        return (
            str(self.referenceNumber_id)
        )  # maybe change to the shortname of the project

    # def en_id(self):
    #   return self.enargus_daten.enargus_id




class ModuleAssignment(models.Model):
    """ORM-Model Defintion for the moduleAssignment model


    """
    moduleAssignment_id = models.AutoField(
        primary_key=True, help_text="auto generiert ID"
    )
    priority1 = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text="""Project allocation with priority 1 (main contact partner)
            e.g. M2, M1, ag: ausgelaufen""",
    )
    priority2 = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text="""Project allocation with priority 2 (main contact partner)
            e.g. M2, M1, ag: ausgelaufen""",
    )
    priority3 = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text="""Project allocation with priority 3 (main contact partner)
            e.g. M2, M1, ag: ausgelaufen""",
    )
    priority4 = models.CharField(
        max_length=2,
        help_text="""Project allocation with priority 4 (main contact partner)
            e.g. M2, M1, ag: ausgelaufen""",
        null=True,
        blank=True,
    )


class Enargus(models.Model):
    """ORM-Model Defintion for the Enargus model


    """
    enargus_id = models.AutoField(primary_key=True)
    startDate = models.DateField(blank=True, null=True)
    endDate = models.DateField(blank=True, null=True)
    topics = models.CharField(
        max_length=500,
        help_text="title of the subproject, incl. acronym",
        blank=True,
        null=True,
    )
    collaborativeProject = models.CharField(
        max_length=200,
        help_text="title of the joint project, including acronym",
        blank=True,
        null=True,
    )
    furtherFundingInformation = models.ForeignKey(
        "FurtherFundingInformation",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    projectLead = models.ForeignKey(
        "Person", null=True, on_delete=models.SET_NULL, blank=True
    )
    database = models.CharField(
        max_length=15,
        help_text="database information from EnArgus internal usage",
        default=null,
        null=True,
        blank=True,
    )
    shortDescriptionDe = models.TextField(
        help_text="short description in German",
        default=null,
        null=True,
        blank=True,
    )
    shortDescriptionEn = models.TextField(
        help_text="short description in English",
        default=null,
        null=True,
        blank=True,
    )
    rAndDPlanningCategory = models.ForeignKey(
        "RAndDPlanningCategory",
        help_text="""number of the systematic performance plan ('leistungsplan
            systematik')""",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    grantRecipient = models.ForeignKey(
        "GrantRecipient",
        help_text="recipient organization, to which the funding is granted",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    executingEntity = models.ForeignKey(
        "ExecutingEntity",
        help_text="name of the organization which executes the project",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    appropriatedBudget = models.DecimalField(
        help_text="amount of funding in Euros",
        blank=True,
        max_digits=12,
        decimal_places=2,
        null=True,
    )

    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return (
            str(self.collaborativeProject)
        )  # maybe change to the shortname of the project


class FurtherFundingInformation(models.Model):
    """ORM-Model Defintion for the FurtherFundingInformation model


    """
    furtherFundingInformation_id = models.AutoField(
        primary_key=True, help_text="Auto.generiert ID"
    )
    fundedBy = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Akronym des Bundesministeriums",
    )
    projectManagementAgency = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Name des Projektraegers",
    )
    researchProgram = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Name des Forschungsprogramms",
    )
    fundingProgram = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Name des Forderprogramms",
    )


class RAndDPlanningCategory(models.Model):
    """ORM-Model Defintion for the RAndDplanningCategory model

    """
    rAndDPlanningCategoryNumber = models.CharField(
        primary_key=True,
        max_length=6,
        help_text="""identifier number of the performance plan systematic -
            'Leistungsplansystematiknummer'""",
    )
    rAndDPlanningCategoryText = models.CharField(max_length=150)
    # def __str__(self):
    #    return self.rAndDPlanningCategoryNumber


class ExecutingEntity(models.Model):
    """ORM-Model Defintion for the Executing-Entity model

    """
    executingEntity_id = models.AutoField(
        primary_key=True, help_text="auto generiert ID"
    )
    name = models.CharField(max_length=250)
    address = models.ForeignKey(
        "Address", null=true, on_delete=models.SET_NULL, blank=True
    )  # If address is deleted no need to delete this entry, just set to NULL


class GrantRecipient(models.Model):
    """ORM-Model Defintion for the Grant-Recipient model

    """
    grantRecipient_id = models.AutoField(
        primary_key=True, help_text="auto generiert ID"
    )
    name = models.CharField(max_length=250)
    address = models.ForeignKey(
        "Address", null=True, on_delete=models.SET_NULL, blank=True
    )  # If address is deleted no need to delete this entry, just set to NULL


class Person(models.Model):
    """ORM-Model Defintion for the Person model

    """
    person_id = models.AutoField(
        primary_key=True, help_text="auto generiert ID"
    )
    surname = models.CharField(
        max_length=100, help_text="family name", null=True
    )
    firstName = models.CharField(max_length=50, help_text="name", null=True)
    title = models.CharField(
        max_length=50, help_text="title of the person", null=True
    )
    email = models.EmailField(help_text="Email Address", null=True)


class Address(models.Model):
    """ORM-Model Defintion for the Address model

    """
    address_id = models.AutoField(
        primary_key=True, help_text="auto generiert ID"
    )
    plz = models.CharField(max_length=5, null=True)
    location = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=150, null=True)
