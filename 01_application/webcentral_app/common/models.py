from django.db import models

class DbDiff(models.Model):
    """

    """
    identifier = models.CharField(max_length=100)
    diffStr = models.TextField()
    executed = models.BooleanField(default=False)
