# Generated by Django 4.2.1 on 2024-08-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "component_list",
            "0004_rename_yearofuseperyear_component_operationtime",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="component",
            name="globalWarmingPotentialProdSup",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="component",
            name="globalWarmingPotentialUsePhaseSup",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="component",
            name="operationTimeSup",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="component",
            name="powerUseCasePhaseActiveSuperscript",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]