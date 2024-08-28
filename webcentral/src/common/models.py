"""Models, which can be used in all other apps of the projects.

"""
from django.db import models


class DbDiff(models.Model):
    """ORM-model definition of the `DBDiff`, which is instanciated if 
    data conflicts appear in the data_import-process.
    
    """

    identifier = models.CharField(max_length=100)
    diffStr = models.TextField()
    executed = models.BooleanField(default=False)


class Literature(models.Model):
    """Definition of the Literature-ORM class, which is used in the apps
    `user_integration`, `positive_environemntal_impact` and `data_sufficiency`
    """

    literature = models.TextField()
    linkName = models.CharField(max_length=255, blank=True, null=True)

    # authors = models.CharField(max_length=500)
    # publication_year = models.IntegerField(blank=True, null=True)
    # publication_title = models.CharField(max_length=500)
    # publisher = models.CharField(max_length=500, blank=True, null=True)
    # publication_location = models.CharField(max_length=500,
    #                                         blank=True,
    #                                         null=True)
    def __str__(self):
        return str(self.literature)
