from django.db import models

from project_listing.models import Subproject


class ComponentClass(models.Model):
    componentClass = models.CharField(max_length=255)

    def __str__(self):
        return self.componentClass


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Component(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    component = models.ForeignKey("ComponentClass", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    energyConsumptionUsePhaseTotal = models.FloatField(blank=True, null=True)
    globalWarmingPotentialTotal = models.FloatField(blank=True, null=True)
    componentWeight = models.FloatField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    energyConsumptionUsePhaseActive = models.FloatField(blank=True, null=True)
    energyConsumptionUsePhasePassive = models.FloatField(blank=True, null=True)
    globalWarmingPotentialProduction = models.FloatField(blank=True, null=True)
    globalWarmingPotentialUsePhase = models.FloatField(blank=True, null=True)
    globalWarmingPotentialEndOfLife = models.FloatField(blank=True, null=True)
    furtherInformationNotes = models.TextField(blank=True)
    sources = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.component.componentClass


class EnvironmentalImpact(models.Model):
    category = models.CharField(max_length=255)
    description = models.TextField()
    name_digital_application = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    funding_label = models.ForeignKey(Subproject, on_delete=models.CASCADE)
    # duration = models.DurationField()
    partner = models.CharField(max_length=255)
    project_website = models.URLField()
    consortium = models.TextField()
    further = models.TextField(blank=True, null=True)
    digitalApplications = models.TextField()
    goals = models.TextField()
    strategies = models.TextField()
    relevance = models.TextField()
    image = models.CharField(max_length=300)
    problem_statement_and_problem_goals = models.TextField()
    implementation_in_the_project = models.TextField()
    evaluation = models.TextField()

    def __str__(self):
        return self.category


class DataSufficiency(models.Model):
    strategyCategory = models.CharField(max_length=255)
    categoryShortDescription = models.TextField()
    example1 = models.TextField()
    example2 = models.TextField()

    def __str__(self):
        return self.strategyCategory
