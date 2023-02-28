from django.db import models

# Create your models here.

class collectedDatasets(models.Model):
    useCaseCategory=models.CharField(max_length=200,null=True)
    categoryDataset=models.CharField(max_length=200,null=True)
    reference=models.CharField(max_length=200,null=True)
    referenceLink=models.CharField(max_length=200,null=True)
    availability=models.CharField(max_length=200,null=True)
    coverage=models.CharField(max_length=200,null=True)
    resolution=models.CharField(max_length=200,null=True)
    comment=models.CharField(max_length=200,null=True)
    dataSources=models.CharField(max_length=200,null=True)
    shortDesciption=models.CharField(max_length=200,null=True)
    includesNonResidential=models.CharField(max_length=200,null=True)
