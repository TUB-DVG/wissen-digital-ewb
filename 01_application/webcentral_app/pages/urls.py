"""Include url conneced to view functions."""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('coming', views.coming, name='coming'),
    path('Datenschutzhinweis', views.Datenschutzhinweis,
         name='Datenschutzhinweis'),
    path('businessModelsChallenge', views.businessModelsChallenge,
         name='businessModelsChallenge'),
    path('businessModelsPractice', views.businessModelsPractice,
         name='businessModelsPractice'),
    path('userIntegrationPractice', views.userIntegrationPractice,
         name='userIntegrationPractice'),
    path('userIntegrationMethod', views.userIntegrationMethod,
         name='userIntegrationMethod'),
    path('environmentalIntegrityNegativ', views.environmentalIntegrityNegativ,
         name='environmentalIntegrityNegativ'),
    path('environmentalIntegrityPositiv', views.environmentalIntegrityPositiv,
         name='environmentalIntegrityPositiv'),
    path('benchmarkingChallenges', views.benchmarkingChallenges,
         name='benchmarkingChallenges'),
    path('dataSufficiency', views.dataSufficiency,
         name='dataSufficiency'),
]
