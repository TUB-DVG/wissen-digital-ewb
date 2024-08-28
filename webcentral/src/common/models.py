from django.db import models


class DbDiff(models.Model):
    """ """

    identifier = models.CharField(max_length=100)
    diffStr = models.TextField()
    executed = models.BooleanField(default=False)


class Literature(models.Model):
    """ """

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
        return self.literature
