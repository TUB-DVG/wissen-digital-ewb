# Generated by Django 3.2.9 on 2022-04-07 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools_over', '0002_auto_20220317_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tools',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]