from django.db import models
from sqlalchemy import null, true

# Create your models here.


class KeywordRegisterFirstReview(models.Model):
    keywordRegisterFirstReview_id = models.AutoField(
        primary_key=True, help_text="Auto.generiert ID"
    )
    keyword1 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword1",
    )
    keyword2 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword2",
    )
    keyword3 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword3",
    )
    keyword4 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword4",
    )
    keyword5 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword5",
    )
    keyword6 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword6",
    )
    keyword7 = models.ForeignKey(
        "Keyword",
        null=true,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="keyword7",
    )

    def __str__(self):
        return str(self.keywordRegisterFirstReview_id)


class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True, help_text="Auto.generiert ID")
    keyword = models.CharField(max_length=200, help_text="keyword", blank=True)
    keywordDefiniton = models.CharField(
        max_length=1500, help_text="Definition of the keyword", blank=True
    )
    literature = models.CharField(
        max_length=1500, help_text="Literature for the keyword", blank=True
    )

    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.keyword
