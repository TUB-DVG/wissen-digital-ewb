from django.db import models


class DataSufficiency(models.Model):
    strategyCategory = models.CharField(max_length=255)
    categoryShortDescription = models.TextField()
    example1 = models.TextField()
    example2 = models.TextField()

    def __str__(self):
        return self.strategyCategory
