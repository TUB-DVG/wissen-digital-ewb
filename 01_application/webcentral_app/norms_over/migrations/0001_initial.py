# Generated by Django 3.2.9 on 2023-04-12 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Norms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, help_text='Name der Norm', max_length=150)),
                ('ShortDescription', models.CharField(help_text='Kurzbeschreibung der Norm', max_length=1000)),
                ('Title', models.CharField(blank=True, help_text='Titel der Norm', max_length=1000)),
                ('Source', models.CharField(blank=True, help_text='Quelle der Norm', max_length=100)),
                ('Link', models.CharField(blank=True, help_text='Link zur Norm', max_length=100)),
            ],
        ),
    ]