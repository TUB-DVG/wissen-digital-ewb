# Generated by Django 4.2.1 on 2024-08-14 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "component_list",
            "0005_component_globalwarmingpotentialprodsup_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="component",
            name="operationTimeSup",
        ),
    ]