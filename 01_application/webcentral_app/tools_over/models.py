from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Rating (models.Model):
    ratingFrom = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ratingFrom')
    ratingFor = models.ForeignKey("Tools", on_delete=models.SET_NULL, null=True, related_name='ratingFor')
    comment=models.CharField(max_length=1000,blank=True)
    score=models.IntegerField  ( default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
     )
    def __str__(self):
        return self.ratingFor.name

class Tools(models.Model):
    name = models.CharField(max_length = 150,
                                   help_text="name",
                                   blank = True)
    shortDescription = models.CharField(max_length = 1000,
                                   help_text = "short description")
    # use the Enum Functional API to concisely use the labels #https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    """
    class ApplicationArea(models.TextChoices):
        verwaltung = 'VW', _('Verwaltung') 
        forschung_lehre =  'FL', _('Forschung/Lehre')
        industrie = 'IN', _('Industrie')
    """
    applicationArea = models.CharField(max_length = 1000,
                                         help_text = "application area",
                                         #choices = ApplicationArea.choices,
                                         blank=True)
    # class usage
    usage = models.CharField(max_length = 100,
                                 help_text = "usage",
                                 blank = True)
    lifeCyclePhase  = models.CharField(max_length = 100,
                                         help_text = "Life cycle phase of buildings where the application is used",
                                         blank = True)
    userInterface = models.CharField(max_length = 300,
                                           help_text = "userInterface",
                                           blank = True)
    targetGroup = models.CharField(max_length = 300,
                                  help_text = "Which group of people is the tool targeted at?",
                                  blank = True)
    lastUpdate = models.CharField(max_length = 100,
                                  help_text = "time (year/month/date) of the last update",
                                  blank = True)
    licence = models.CharField(max_length = 200,
                              help_text = "licence",
                              blank = True)
    furtherInformation = models.CharField(max_length = 500,
                                          help_text = "further information",
                                          blank = True)
    alternatives = models.CharField(max_length = 300,
                                    help_text = "similar tool(s) that can serve as alternatives",
                                    blank = True)
    specificApplication= models.CharField(max_length = 500,
                                          help_text = "specific application of the tool in EWB projects (project name + fkz)",
                                          blank = True)
    userEvaluation = models.DecimalField(max_digits=2, decimal_places=1,
                                            help_text = "evaluation of the application by users (range: 1-5 (best), with one decimal place)",
                                            blank = True, null = True)
    #image=models.ImageField(default="webcentral_app/tools_over/Media/Default.webp", null=True,blank = True)  #You need to install pillow
    image=models.ImageField(null=True,blank = True)  #You need to install pillow



    def averageRating(self):
        counter = 0
        totalRatings = 0
        for item in Rating.objects.filter(ratingFor=self):
            counter += 1
            totalRatings += item.score
        if counter>0:#
                
            return  round((totalRatings / counter) * 2) / 2  
        else:
            return 0

    

    def __str__(self):
        return self.name



