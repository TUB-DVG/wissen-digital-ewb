from django.db import models
from django.template import (
    Template,
    Context,
)

from user_integration.models import Literature

class DataSufficiency(models.Model):
    strategyCategory = models.CharField(max_length=255)
    categoryShortDescription = models.TextField()
    categoryLongDescription = models.TextField()
    example1 = models.TextField()
    example2 = models.TextField()
    literature = models.ManyToManyField(Literature, blank=True, null=True)
    

    @property
    def categoryLongDescriptionRendered(self):
        """Getter method for the long-description.
        HTML is rendered by the django-Template engine.
        """
        templateObj = Template(self.categoryLongDescription.replace("<br>", "<br><br>"))
        contextObj = Context({})
        return templateObj.render(contextObj)

    def __str__(self):
        return self.strategyCategory
