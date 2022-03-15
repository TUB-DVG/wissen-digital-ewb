from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Rating (models.Model):
    rating_from = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rating_from')
    rating_for = models.ForeignKey("Tools", on_delete=models.SET_NULL, null=True, related_name='rating_for')
    score=models.IntegerField  ( default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
     )
    def __str__(self):
        return self.rating_for.bezeichnung

class Tools(models.Model):
    bezeichnung = models.CharField(max_length = 150,
                                   help_text="Name der Anwendung",
                                   blank = True)
    kurzbeschreibung = models.CharField(max_length = 1000,
                                   help_text = "Kurzbeschreibung der Anwendung")
    anwendungsbereich = models.CharField(max_length = 1000,
                                         help_text = "Anwendungsbereich der Anwendung",
                                         blank=True)
    kategorie = models.CharField(max_length = 100,
                                 help_text = "Kategorie in der die Anwendung eingeordnet werden kann",
                                 blank = True)
    lebenszyklusphase = models.CharField(max_length = 100,
                                         help_text = "Lebenszyklusphase von Gebäuden\
                                         in der die Anwendung genutzt wird",
                                         blank = True)
    nutzerschnittstelle = models.CharField(max_length = 300,
                                           help_text = "Nutzerschnittstelle \
                                           (wie wird die Anwendung vom Nutzer genutzt)",
                                           blank = True)
    zielgruppe = models.CharField(max_length = 300,
                                  help_text = "Zielgruppe der Anwendung",
                                  blank = True)
    letztes_update = models.CharField(max_length = 100,
                                      help_text = "letztes Update der Anwendung",
                                      blank = True)
    lizenz = models.CharField(max_length = 200,
                              help_text = "Lizenz der Anwendung",
                              blank = True)
    weitere_informationen = models.CharField(max_length = 500,
                                             help_text = "weitere Informationen zur Anwendung",
                                             blank = True)
    alternativen = models.CharField(max_length = 300,
                                    help_text = "Alternativen zu der jeweiligen Anwendung",
                                    blank = True)
    konk_anwendung= models.CharField(max_length = 500,
                                     help_text = "konkrete Anwendung in EWB Projekten",
                                     blank = True)
    nutzerbewertungen = models.DecimalField(max_digits=3, decimal_places=1,
                                            help_text = "Bewertung der Anwendung durch Nutzende \
                                            (geplant max. 10 mit einer Kommastelle, max. 10.0)",
                                            blank = True, null = True)
    image=models.ImageField(default="Default.webp", null=True,blank = True)  #You need to install pillow



    def average_rating(self):
        counter = 0
        total_ratings = 0
        for item in Rating.objects.filter(rating_for=self):
            counter += 1
            total_ratings += item.score
        if counter>0:#
                
            return  round((total_ratings / counter) * 2) / 2  
        else:
            return 0

    

    def __str__(self):
        return self.bezeichnung
