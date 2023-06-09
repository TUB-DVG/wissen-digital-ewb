from django.db import models

# Create your models here.

class collectedDatasets(models.Model):

    nameDataset=models.CharField(max_length=200)
    useCaseCategory=models.CharField(max_length=200,null=True)
    categoryDataset=models.CharField(max_length=200,null=True)
    reference=models.CharField(max_length=200,null=True,blank=True)
    referenceLink=models.CharField(max_length=200,null=True,blank=True)
    availability=models.CharField(max_length=200,null=True)
    coverage=models.CharField(max_length=200,null=True,blank=True)
    resolution=models.CharField(max_length=500,null=True,blank=True)
    comment=models.CharField(max_length=200,null=True,blank=True)
    dataSources=models.CharField(max_length=500,null=True,blank=True)
    # shortDescriptionEn
    # shortDescritopnDe -> vereinheitlichen 
    shortDescriptionDe=models.CharField(max_length=300,null=True,blank=True)
    includesNonResidential=models.CharField(max_length=200,null=True,blank=True)
