# Generated by Django 4.2.1 on 2024-08-02 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criteria_catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='norms',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]