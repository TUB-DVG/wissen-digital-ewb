# Generated by Django 3.2.9 on 2023-04-14 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('norms_over', '0002_alter_norms_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='norms',
            name='Link',
            field=models.CharField(blank=True, help_text='Link zur Norm', max_length=100),
        ),
    ]