from django.db import models
from embed_video.fields import EmbedVideoField
# Create your models here.

class video (models.Model):
    title =models.CharField(max_length=180)
    url=EmbedVideoField()
    def __str__(self):
        return self.title