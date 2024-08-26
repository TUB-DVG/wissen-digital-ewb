from django.db import models
from django.template import Template, Context

from project_listing.models import Subproject
from common.models import Literature

class EnvironmentalImpact(models.Model):
    category = models.CharField(max_length=255)
    description = models.TextField()
    name_digital_application = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    funding_label = models.ManyToManyField(Subproject, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    partner = models.CharField(max_length=255, blank=True, null=True)
    project_website = models.URLField(blank=True, null=True)
    consortium = models.TextField(blank=True, null=True)
    further = models.TextField(blank=True, null=True)
    digitalApplications = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    strategies = models.TextField(blank=True, null=True)
    relevance = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, null=True)
    problem_statement_and_problem_goals = models.TextField(blank=True, null=True)
    implementation_in_the_project = models.TextField(blank=True, null=True)
    evaluation = models.TextField(blank=True, null=True)
    literature = models.ManyToManyField(Literature, blank=True, null=True)


    def __str__(self):
        return self.category

    @property
    def literatureList(self):
        """The pname property."""
        
        combinedText = "<ul>"
        for literature in self.literature.all():
            if literature.literature.startswith("<sup"):
                combinedText += "<li id='footnote1'>" + literature.literature + "</li>"
            else:
                linkName = literature.linkName.replace('\n', '')
                combinedText += f"<li id='{linkName}'>" + literature.literature + "</li>"

        combinedText += "</ul>"
        templateObj = Template(combinedText)
        contextObj = Context({})
        return templateObj.render(contextObj)

    @property
    def evaluationRendered(self):
        """The  property."""
        return Template(self.evaluation).render(Context({}))

    @property
    def implementation_in_the_project_rendered(self):
        """The  property."""
        return Template(self.implementation_in_the_project).render(Context({}))
