# Generated by Django 3.2.9 on 2023-03-13 11:46

from django.db import migrations, models
import django.db.models.deletion
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        ('project_listing', '0004_auto_20220714_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anschrift',
            name='adresse',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='anschrift',
            name='land',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='anschrift',
            name='ort',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='anschrift',
            name='plz',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='ausfuehrende_stelle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_listing.ausfuehrende_stelle'),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='datenbank',
            field=models.CharField(blank=True, default=sqlalchemy.sql.expression.null, help_text='Datenbank Information/Enargus Intern', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='foerdersumme',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Foerdersumme in EUR', max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='kurzbeschreibung_de',
            field=models.TextField(blank=True, default=sqlalchemy.sql.expression.null, help_text='Deutsche Kurzbeschreibung', null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='kurzbeschreibung_en',
            field=models.TextField(blank=True, default=sqlalchemy.sql.expression.null, help_text='Englische Kurzbeschreibung', null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='laufzeitbeginn',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='laufzeitende',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='thema',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='verbundbezeichnung',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='enargus',
            name='zuwendsempfanger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_listing.zuwendungsempfaenger'),
        ),
        migrations.AlterField(
            model_name='forschung',
            name='bundesministerium',
            field=models.CharField(blank=True, help_text='Akronym des Bundesministeriums', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='forschung',
            name='foerderprogramm',
            field=models.CharField(blank=True, help_text='Name des Forderprogramms', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='forschung',
            name='forschungsprogramm',
            field=models.CharField(blank=True, help_text='Name des Forschungsprogramms', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='forschung',
            name='projekttraeger',
            field=models.CharField(blank=True, help_text='Name des Projektraegers', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='modulen_zuordnung_ptj',
            name='priority_1',
            field=models.CharField(blank=True, help_text='Projektzuordnung mit der Prioritat 1, ag: ausgelaufen', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='modulen_zuordnung_ptj',
            name='priority_2',
            field=models.CharField(blank=True, help_text='Projektzuordnung mit der Prioritat 2, ag: ausgelaufen', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='modulen_zuordnung_ptj',
            name='priority_3',
            field=models.CharField(blank=True, help_text='Projektzuordnung mit der Prioritat 3, ag: ausgelaufen', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(help_text='Email_Adresse der Person', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(help_text='Name der Person', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='titel',
            field=models.CharField(help_text='Titel der Person', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='vorname',
            field=models.CharField(help_text='Vorname der Person', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='zuwendungsempfaenger',
            name='anschrift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_listing.anschrift'),
        ),
    ]