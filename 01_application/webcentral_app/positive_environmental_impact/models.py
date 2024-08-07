from django.db import models

from project_listing.models import Subproject
from user_integration.models import Literature

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

