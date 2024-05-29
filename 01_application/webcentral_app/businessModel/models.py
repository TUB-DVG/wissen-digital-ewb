from django.db import models


class BusinessModel(models.Model):
    challenge = models.CharField(max_length=255, blank=True, null=True)
    shortDescription = models.TextField(blank=True, null=True)
    property1 = models.CharField(max_length=255, blank=True, null=True)
    property1Text = models.TextField(blank=True, null=True)
    property2 = models.CharField(max_length=255, blank=True, null=True)
    property2Text = models.TextField(blank=True, null=True)
    property3 = models.CharField(max_length=255, blank=True, null=True)
    property3Text = models.TextField(blank=True, null=True)
    property4 = models.CharField(max_length=255, blank=True, null=True)
    property4Text = models.TextField(blank=True, null=True)
    property5 = models.CharField(max_length=255, blank=True, null=True)
    property5Text = models.TextField(blank=True, null=True)
    imageIcon = models.CharField(max_length=255, blank=True, null=True)
    imageIconSelected = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.challenge


class UserEngagement(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True)
    categoryShortDescription = models.TextField(blank=True, null=True)
    subCategory = models.CharField(max_length=255, blank=True, null=True)
    subCategoryShortDescription = models.TextField(blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    timeRequired = models.CharField(max_length=255, blank=True, null=True)
    groupSize = models.CharField(max_length=255, blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    advantages = models.TextField(blank=True, null=True)
    disadvantages = models.TextField(blank=True, null=True)
    conductedBy = models.CharField(max_length=255, blank=True, null=True)
    successFactors = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    procedure = models.TextField(blank=True, null=True)
    specificGoals = models.TextField(blank=True, null=True)
    specificProcedure = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category
