from django.db import models

from project_listing.models import Subproject
from user_integration.models import Literature

class EnvironmentalImpact(models.Model):
    category = models.CharField(max_length=255)
    description = models.TextField()
    name_digital_application = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    funding_label = models.ForeignKey(Subproject, on_delete=models.CASCADE)
    # duration = models.DurationField()
    partner = models.CharField(max_length=255)
    project_website = models.URLField()
    consortium = models.TextField()
    further = models.TextField(blank=True, null=True)
    digitalApplications = models.TextField()
    goals = models.TextField()
    strategies = models.TextField()
    relevance = models.TextField()
    image = models.CharField(max_length=300)
    problem_statement_and_problem_goals = models.TextField()
    implementation_in_the_project = models.TextField()
    evaluation = models.TextField()
    literature = models.ManyToManyField(Literature, blank=True, null=True)


    def __str__(self):
        return self.category

