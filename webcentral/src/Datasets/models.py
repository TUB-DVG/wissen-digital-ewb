from django.db import models

# Create your models here.


class collectedDatasets(models.Model):

    name = models.CharField(max_length=200, db_comment="Name of the dataset")
    applicationArea = models.CharField(max_length=200, null=True, db_comment="Typical application area in which the dataset is used. An application area describes all possible methods and datasets, that can be used to achieve a specific purpose.")
    classification = models.CharField(max_length=200, null=True, db_comment="General type of dataset - Which category does the data set belong to?")
    reference = models.CharField(max_length=200, null=True, blank=True)
    referenceLink = models.CharField(max_length=200, null=True, blank=True)
    availability = models.CharField(max_length=200, null=True)
    coverage = models.CharField(max_length=200, null=True, blank=True)
    resolution = models.CharField(max_length=500, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    dataSources = models.CharField(max_length=500, null=True, blank=True)
    shortDescriptionDe = models.CharField(max_length=300, null=True, blank=True)
    includesNonResidential = models.CharField(
        max_length=200, null=True, blank=True
    )

    def __str__(self):
        return self.name
