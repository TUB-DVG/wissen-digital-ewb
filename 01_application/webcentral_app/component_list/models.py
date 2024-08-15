from django.db import models
from django.template import Template, Context

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
    componentClass = models.ForeignKey("ComponentClass", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    energyConsumptionUsePhaseTotal = models.FloatField(blank=True, null=True)
    globalWarmingPotentialTotal = models.FloatField(blank=True, null=True)
    componentWeight = models.FloatField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    specificGlobalWarmingPotential = models.FloatField(blank=True, null=True)
    energyConsumptionUsePhaseActive = models.FloatField(blank=True, null=True)
    powerUseCasePhaseActiveSuperscript = models.CharField(max_length=100, blank=True, null=True)
    energyConsumptionUsePhasePassive = models.FloatField(blank=True, null=True)
    globalWarmingPotentialProduction = models.FloatField(blank=True, null=True)
    globalWarmingPotentialProdSup = models.CharField(max_length=100, blank=True, null=True)

    globalWarmingPotentialUsePhase = models.FloatField(blank=True, null=True)
    globalWarmingPotentialUsePhaseSup = models.CharField(max_length=100, blank=True, null=True)

    globalWarmingPotentialEndOfLife = models.FloatField(blank=True, null=True)
    furtherInformationNotes = models.TextField(blank=True)
    sources = models.TextField(blank=True, null=True)
    operationTime = models.IntegerField(blank=True, null=True)
    operationTimeSupscript = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.componentClass.componentClass

    @property
    def energyConsumptionUsePhaseTotalRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.energyConsumptionUsePhaseTotal)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.energyConsumptionUsePhaseTotal is not None:
            return round(self.energyConsumptionUsePhaseTotal, decimalPosToRound)

    @property
    def globalWarmingPotentialTotalRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.globalWarmingPotentialTotal)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.globalWarmingPotentialTotal is not None:
            return round(self.globalWarmingPotentialTotal, decimalPosToRound)

    @property
    def componentWeightRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.componentWeight)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.componentWeight is not None:
            return round(self.componentWeight, decimalPosToRound)

    @property
    def specificGlobalWarmingPotentialRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.specificGlobalWarmingPotential)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.specificGlobalWarmingPotential is not None:
            return round(self.specificGlobalWarmingPotential, decimalPosToRound)
    
    @property
    def energyConsumptionUsePhaseActiveRoundedSup(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.energyConsumptionUsePhaseActive)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.energyConsumptionUsePhaseActive is not None:
            roundedNumber = round(self.energyConsumptionUsePhaseActive, decimalPosToRound)
            if self.powerUseCasePhaseActiveSuperscript is not None:
                return Template(str(roundedNumber) + f"<sup class='supForNumValues'>{self.powerUseCasePhaseActiveSuperscript}</sup>").render(Context({}))
            else:
                return roundedNumber

    @property
    def energyConsumptionUsePhasePassiveRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.energyConsumptionUsePhasePassive)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.energyConsumptionUsePhasePassive is not None:
            return round(self.energyConsumptionUsePhasePassive, decimalPosToRound)

    @property
    def globalWarmingPotentialProductionRoundedSub(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.globalWarmingPotentialProduction)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.globalWarmingPotentialProduction is not None:
            roundedNumber = round(self.globalWarmingPotentialProduction, decimalPosToRound)
            if self.globalWarmingPotentialProdSup is not None:
                return Template(str(roundedNumber) + f"<sup class='supForNumValues'>{self.globalWarmingPotentialProdSup}</sup>").render(Context({}))
    
    @property
    def globalWarmingPotentialUsePhaseRoundedSub(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.globalWarmingPotentialUsePhase)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.globalWarmingPotentialUsePhase is not None:
            roundedNumber = round(self.globalWarmingPotentialUsePhase, decimalPosToRound)
            if self.globalWarmingPotentialUsePhaseSup is not None:
                return Template(str(roundedNumber) + f"<sup class='supForNumValues'>{self.globalWarmingPotentialUsePhaseSup}</sup>").render(Context({}))
  
    @property
    def globalWarmingPotentialEndOfLifeRounded(self):
        """Processes the FloatField and rounds 

        """
        stringOfFloat = str(self.globalWarmingPotentialEndOfLife)
        decimalPosToRound = self._findLastDecimalPlaces(stringOfFloat)
        if self.globalWarmingPotentialEndOfLife is not None:
            return round(self.globalWarmingPotentialEndOfLife, decimalPosToRound)

    @property
    def furtherInformationNotesRendered(self):
        return Template(self.furtherInformationNotes.replace("\n", "")).render(Context({}))

    @property
    def operationTimeRendered(self):
        
        if self.operationTimeSupscript is not None or self.operationTimeSupscript != "":
            return Template(str(self.operationTime) + f"<sup class='supForNumValues'>{self.operationTimeSupscript}</sup>").render(Context({}))



    def _findLastDecimalPlaces(self, elementStr):
        """Find the 2 last decimal places to the furthet right. Return the decimal position
        of the most right deimal position.
        E.g. 
        1,00020 -> 4 
        1,00021 -> 5
        0,21 -> 2
 

        """
        if "." in elementStr:
            splitted = elementStr.split(".")
        elif "," in elementStr:
            splitted = elementStr.split(",")
        else:
            return 0
        
        decimalPlaces = splitted[1]
        countedNonZeros = 0
        for position, place in enumerate(decimalPlaces):
            if place in "123456789":
                return position+2
            
