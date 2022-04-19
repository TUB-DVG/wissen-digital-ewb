from django.db import models

# Create your models here.

class Schlagwortregister_erstsichtung(models.Model):
    schlagwortregister_erstsichtung_id = models.AutoField(primary_key=True,help_text="Auto.generiert ID")
    schlagwort_1 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_2 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_3 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_4 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_5 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_6 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)
    schlagwort_7 = models.CharField(max_length = 200,
                                   help_text="Schlagwort, Erstsichtung der Projekte über die Kurzbeschreibung (Ende 2020)",
                                   blank = True)

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
