from django.db import models
from django.template import (
    Template,
    Context,
)

from common.models import Literature


class DataSufficiency(models.Model):
    strategyCategory = models.CharField(max_length=255)
    categoryShortDescription = models.TextField()
    categoryLongDescription = models.TextField()
    example1 = models.TextField(blank=True, null=True)
    example1Heading = models.CharField(max_length=200, blank=True, null=True)
    example2 = models.TextField(blank=True, null=True)
    example2Heading = models.CharField(max_length=200, blank=True, null=True)
    literature = models.ManyToManyField(Literature, blank=True, null=True)

    @property
    def categoryLongDescriptionRendered(self):
        """Getter method for the long-description.
        HTML is rendered by the django-Template engine.
        """
        templateObj = Template(self.categoryLongDescription.replace("<br>", "<br><br>"))
        contextObj = Context({})
        return templateObj.render(contextObj)

    @property
    def literatureList(self):
        """The pname property."""

        combinedText = "<ul>"
        for literature in self.literature.all():
            if literature.literature.startswith("<sup"):
                combinedText += "<li id='footnote1'>" + literature.literature + "</li>"
            else:
                linkName = literature.linkName.replace("\n", "")
                combinedText += (
                    f"<li id='{linkName}'>" + literature.literature + "</li>"
                )

        combinedText += "</ul>"
        templateObj = Template(combinedText)
        contextObj = Context({})
        return templateObj.render(contextObj)

    def __str__(self):
        return self.strategyCategory
