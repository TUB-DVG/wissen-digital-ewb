from django.db import models

class Component(models.Model):
    category = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    description = models.TextField()
    energyConsumptionUsePhaseTotal = models.FloatField()
    globalWarmingPotentialTotal = models.FloatField()
    componentWeight = models.FloatField()
    lifetime = models.IntegerField()
    energyConsumptionUsePhaseActive = models.FloatField()
    energyConsumptionUsePhasePassive = models.FloatField()
    globalWarmingPotentialProduction = models.FloatField()
    globalWarmingPotentialUsePhase = models.FloatField()
    globalWarmingPotentialEndOfLife = models.FloatField()
    furtherInformationNotes = models.TextField(blank=True)
    sources = models.TextField()

    def __str__(self):
        return self.component