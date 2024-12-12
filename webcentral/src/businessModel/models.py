from django.db import models

from common.models import AbstractHistory, AbstractModelMethods


class History(AbstractHistory):
    """ """


class BusinessModelManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(
            name=name,
        )


class BusinessModel(AbstractModelMethods):
    challenge = models.CharField(max_length=255, blank=True, null=True)
    shortDescription = models.TextField(blank=True, null=True)
    property1 = models.CharField(max_length=255, blank=True, null=True)
    property1Text = models.TextField(blank=True, null=True)
    property2 = models.CharField(max_length=255, blank=True, null=True)
    property2Text = models.TextField(blank=True, null=True)
    property3 = models.CharField(max_length=255, blank=True, null=True)
    property3Text = models.TextField(blank=True, null=True)
    property4 = models.CharField(max_length=255, blank=True, null=True)
    property4Text = models.TextField(blank=True, null=True)
    property5 = models.CharField(max_length=255, blank=True, null=True)
    property5Text = models.TextField(blank=True, null=True)
    imageIcon = models.CharField(max_length=255, blank=True, null=True)
    imageIconSelected = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.challenge

    objects = BusinessModelManager()
