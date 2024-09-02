from django.db import models
from django.template import Template, Context

from common.models import Literature


class ProArgument(models.Model):
    proArgument = models.TextField()

    def __str__(self):
        return self.proArgument

    @property
    def proArgumentRendered(self):
        template = Template(self.proArgument)
        context = Context({})
        return template.render(context)


class ConArgument(models.Model):
    conArgument = models.TextField()

    def __str__(self):
        return self.conArgument

    @property
    def conArgumentRendered(self):
        template = Template(self.conArgument)
        context = Context({})
        return template.render(context)


class UserEngagement(models.Model):
    category = models.CharField(max_length=255, blank=True, null=True)
    categoryShortDescription = models.TextField(blank=True, null=True)
    subCategory = models.CharField(max_length=255, blank=True, null=True)
    subCategoryShortDescription = models.TextField(blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    timeRequired = models.TextField(blank=True, null=True)
    groupSize = models.TextField(blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    # advantages = models.TextField(blank=True, null=True)
    # disadvantages = models.TextField(blank=True, null=True)
    conductedBy = models.CharField(max_length=255, blank=True, null=True)
    successFactors = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    procedureItem = models.ManyToManyField(
        "ProcedureItem", null=True, blank=True
    )
    # specificGoals = models.TextField(blank=True, null=True)
    # specificProcedure = models.ManyToManyField("SpecificProcedureItem",
    #    null=True,
    #    blank=True)
    proArgument = models.ManyToManyField(ProArgument, blank=True, null=True)
    conArgument = models.ManyToManyField(ConArgument, blank=True, null=True)
    participantObservations = models.CharField(
        max_length=255, blank=True, null=True
    )
    persons = models.CharField(max_length=255, blank=True, null=True)
    imageIcon = models.CharField(max_length=255, blank=True, null=True)
    imageIconSelected = models.CharField(max_length=255, blank=True, null=True)
    goodPracticeExample = models.TextField(null=True, blank=True)
    literature = models.ManyToManyField(Literature, blank=True, null=True)

    def __str__(self):
        return self.category

    @property
    def description(self):
        template = Template(self.subCategoryShortDescription)
        context = Context({})
        return template.render(context)

    @property
    def shortDescription(self):
        template = Template(self.categoryShortDescription)
        context = Context({})
        return template.render(context)

    @property
    def groupSizeRendered(self):
        template = Template(self.groupSize)
        context = Context({})
        return template.render(context)

    @property
    def goodPracticeExampleRendered(self):
        template = Template(self.goodPracticeExample)
        context = Context({})
        return template.render(context)


class ProcedureItem(models.Model):
    procedureItem = models.TextField()

    def procedureItemRendered(self):
        """This method should be called, when the procedureItem attribute of a
        object of type ProcedureItem is called. It renders the text inside the
        object as a django-template.
        """
        template = Template(self.procedureItem)
        context = Context({})
        return template.render(context)

    def __str__(self):
        return self.procedureItem


# class SpecificProcedureItem(models.Model):
#     specificProcedureItem = models.CharField(max_length=255,
#                                              blank=True,
#                                              null=True)

#     def __str__(self):
#         return self.specificProcedureItem
