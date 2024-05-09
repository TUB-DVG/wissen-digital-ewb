from django.db import models


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
