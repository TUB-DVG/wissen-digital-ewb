# Generated by Django 4.2.1 on 2024-08-06 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_listing', '0001_initial'),
        ('user_integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentalImpact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('category_de', models.CharField(max_length=255, null=True)),
                ('category_en', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('description_de', models.TextField(null=True)),
                ('description_en', models.TextField(null=True)),
                ('name_digital_application', models.CharField(max_length=255)),
                ('name_digital_application_de', models.CharField(max_length=255, null=True)),
                ('name_digital_application_en', models.CharField(max_length=255, null=True)),
                ('project_name', models.CharField(max_length=255)),
                ('project_name_de', models.CharField(max_length=255, null=True)),
                ('project_name_en', models.CharField(max_length=255, null=True)),
                ('partner', models.CharField(max_length=255)),
                ('partner_de', models.CharField(max_length=255, null=True)),
                ('partner_en', models.CharField(max_length=255, null=True)),
                ('project_website', models.URLField()),
                ('consortium', models.TextField()),
                ('consortium_de', models.TextField(null=True)),
                ('consortium_en', models.TextField(null=True)),
                ('further', models.TextField(blank=True, null=True)),
                ('further_de', models.TextField(blank=True, null=True)),
                ('further_en', models.TextField(blank=True, null=True)),
                ('digitalApplications', models.TextField()),
                ('digitalApplications_de', models.TextField(null=True)),
                ('digitalApplications_en', models.TextField(null=True)),
                ('goals', models.TextField()),
                ('goals_de', models.TextField(null=True)),
                ('goals_en', models.TextField(null=True)),
                ('strategies', models.TextField()),
                ('strategies_de', models.TextField(null=True)),
                ('strategies_en', models.TextField(null=True)),
                ('relevance', models.TextField()),
                ('relevance_de', models.TextField(null=True)),
                ('relevance_en', models.TextField(null=True)),
                ('image', models.CharField(max_length=300)),
                ('problem_statement_and_problem_goals', models.TextField()),
                ('problem_statement_and_problem_goals_de', models.TextField(null=True)),
                ('problem_statement_and_problem_goals_en', models.TextField(null=True)),
                ('implementation_in_the_project', models.TextField()),
                ('implementation_in_the_project_de', models.TextField(null=True)),
                ('implementation_in_the_project_en', models.TextField(null=True)),
                ('evaluation', models.TextField()),
                ('evaluation_de', models.TextField(null=True)),
                ('evaluation_en', models.TextField(null=True)),
                ('funding_label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_listing.subproject')),
                ('literature', models.ManyToManyField(blank=True, null=True, to='user_integration.literature')),
            ],
        ),
    ]