# Generated by Django 4.2.1 on 2024-08-15 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("project_listing", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subproject",
            name="questionnaire2021",
        ),
        migrations.DeleteModel(
            name="Questionnaire2021",
        ),
    ]