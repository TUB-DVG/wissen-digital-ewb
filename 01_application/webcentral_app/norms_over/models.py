from django.db import models
#from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class TechnicalStandards(models.Model):
    isNorm = models.BooleanField(default=True)
    name = models.CharField(max_length = 150,
                                   help_text="name of the norm",
                                   blank = True)
    title = models.CharField(max_length = 250,
                                         help_text = "title of the norm",
                                         blank=True)
    shortDescription = models.TextField(max_length = 600,
                                   help_text = "short description")
    source = models.CharField(max_length = 100,
                                 help_text = "source",
                                 blank = True)
    link = models.CharField(max_length = 150,
                                         help_text = "link",
                                         blank = True)
    
    #image=models.ImageField(default="webcentral_app/tools_over/Media/Default.webp", null=True,blank = True)  #You need to install pillow
    #image=models.ImageField(null=True,blank = True)  #You need to install pillow

    def __str__(self):
        return self.name



