from django.db import models
#from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class TechnicalStandards(models.Model):
    is_norm = models.TextField(default=True)
    name = models.TextField(max_length = 300,
                                   help_text="name of the norm",
                                   blank = True)
    shortDescription = models.TextField(max_length = 500,
                                   help_text = "short description")
    title = models.TextField(max_length = 255,
                                         help_text = "title of the norm",
                                         blank=True)
    source = models.TextField(max_length = 500,
                                 help_text = "source",
                                 blank = True)
    link = models.TextField(max_length = 500,
                                         help_text = "link",
                                         blank = True)
    
    #image=models.ImageField(default="webcentral_app/tools_over/Media/Default.webp", null=True,blank = True)  #You need to install pillow
    #image=models.ImageField(null=True,blank = True)  #You need to install pillow

    def __str__(self):
        return self.name



