from django.db import models


class BusinessModell(models.Model):
    shortDescription = models.CharField(max_length=255)
    property1 = models.CharField(max_length=255)
    property1Text = models.TextField()
    property2 = models.CharField(max_length=255)
    property2Text = models.TextField()
    property3 = models.CharField(max_length=255)
    property3Text = models.TextField()
    property4 = models.CharField(max_length=255)
    property4Text = models.TextField()
    property5 = models.CharField(max_length=255)
    property5Text = models.TextField()

    def __str__(self):
        return self.shortDescription
