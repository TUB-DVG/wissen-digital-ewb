from django.db import models
from django import template
from django.template import Template, Context

register = template.Library()


# Create your models here.
class CriteriaCatalog(models.Model):
    """Represent a CriteriaCatalog, which holds Tree-Structures of Topics."""

    name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000, blank=True)
    imageIcon = models.CharField(max_length=200, blank=True)
    imageIconSelected = models.CharField(max_length=200, blank=True)

    def __str__(self):
        """Define a String-Representation of a object of type UseCase

        This defines, which String is shown in the admin-panel. It should
        show the `name`-attribute of an `useCase`-Object.
        """
        return self.name


class Topic(models.Model):
    """Represent the Elements inside the hierarchical-structure for each criteriaCatalog."""

    heading = models.TextField(null=True, blank=True)
    text = models.TextField()
    criteriaCatalog = models.ForeignKey("CriteriaCatalog",
                                        on_delete=models.CASCADE)
    topicHeadingNumber = models.CharField(blank=True, null=True)
    # useCase = models.OneToOneField("UseCase", on_delete=models.PROTECT)
    parent = models.ForeignKey(
        "Topic",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    imageFilename = models.CharField(max_length=200, null=True, blank=True)
    tag = models.ManyToManyField("Tag", blank=True)
    norms = models.CharField(max_length=300, null=True, blank=True)
    grey = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        """Return string representation of an `Topic`-object"""
        return self.heading

    @property
    def textLineBreaks(self):
        """Add <br> tags where a linebreak should be present"""

        textWithBRs = str(self.text).replace("\n", "<br>")
        templateObj = Template(textWithBRs)

        contextObj = Context({})
        return templateObj.render(contextObj)

class Tag(models.Model):
    """Represent a Tag, which can be assigned to a Topic."""

    name = models.CharField(max_length=100)

    def __str__(self):
        """Return string representation of an `Tag`-object"""
        return self.name


@register.filter
def format_tags(tags):
    return ", ".join(str(tag) for tag in tags.all())
