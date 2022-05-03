from django.db import models
from sqlalchemy import null, true
# Create your models here.

class Schlagwortregister_erstsichtung(models.Model):
    schlagwortregister_id = models.AutoField(primary_key=True,help_text="Auto.generiert ID")
    schlagwort_1=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_1')
    schlagwort_2=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_2')
    schlagwort_3=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_3')
    schlagwort_4=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_4')
    schlagwort_5=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_5')
    schlagwort_6=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_6')
    schlagwort_7=models.ForeignKey("Schlagwort", null=true, on_delete=models.SET_NULL,blank=True, related_name='schlagwort_7')


class Schlagwort(models.Model):
    schlagwort_id = models.AutoField(primary_key=True,help_text="Auto.generiert ID")
    schlagwort = models.CharField(max_length = 200,
                                   help_text="Name des Schlagworts",
                                   blank = True)
    schlagwort_definiton = models.CharField(max_length = 1500,
                                   help_text="Definition des Schlagworts",
                                   blank = True)
    literatur = models.CharField(max_length = 1500,
                                   help_text="Literaturquellen zum Schlagwort",
                                   blank = True)
    
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.schlagwort  
