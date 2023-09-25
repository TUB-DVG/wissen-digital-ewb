from django.db import models

# Create your models here.

class UseCase(models.Model):
    item_code = models.CharField(max_length=25, unique=True)
    useCase = models.CharField(max_length=50)
    sriLevel = models.CharField(max_length=255,
                                verbose_name="SRI-Zuordnung")
    levelOfAction = models.CharField(max_length=100)
    degreeOfDetail = models.CharField(max_length=100)
    perspective = models.CharField(max_length=255)
    idPerspectiveforDetail = models.PositiveIntegerField()
    effectEvaluation = models.CharField(max_length=1, 
                                     choices=[('+', 'Positive'), ('-', 'Negative'), ('o', 'Neutrale')])
    effectName = models.CharField(max_length=255)
    effectDescription = models.TextField()
    furtherInformation = models.TextField(blank=True, 
                                    null=True)
    icon = models.ImageField(upload_to='icons/', 
                             blank=True, 
                             null=True)

    def __str__(self):
        return self.item_code+'/'+self.useCase