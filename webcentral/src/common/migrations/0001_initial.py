# Generated by Django 4.2.1 on 2024-08-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DbDiff",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("identifer", models.CharField(max_length=100)),
                ("diffStr", models.TextField()),
                ("executed", models.BooleanField(default=False)),
            ],
        ),
    ]