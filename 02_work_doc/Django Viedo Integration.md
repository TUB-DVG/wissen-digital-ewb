# Video integration:
There are 2 ways to add videos to a django webpage.

- Through an embedded Url django application : link to a youtube 
or vimeo(Video exists on the internet we can link it).
- Through filefield ( file is available on local machine or webpage server)
- Directly through html iframes.


## Embedded Url Method django application:
1. install the "django-embed-video" package:
```
pip install django-embed-video
```
2. Add embed_video to INSTALLED_APPS in your Django project settings:
```
INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'embed_video'
   
   ]
```
3. create a Django model for the videos (Recommeneded to create an app solely
for the videos):

```
from embed_video.fields import EmbedVideoField

class video (models.Model):
    title =models.CharField(max_length=180)
    url=EmbedVideoField()
    def __str__(self):
        return self.title

```

4. Register model on the admin page:
```
from .models import video

# Register your models here.
admin.site.register(video)
```
5. Create Viewfunction for video display:
```
#In this example, we are displaying a particular video titled "Test Video" 
def index(request):
	videos=video.objects.get(title="Test Video")
	return render(request, 'pages/index.html',context={'vid':videos})

```

6. Usage of template tags:
```
#This must be added at the top of the html display file:
{% load embed_video_tags %}


# embed shortcut of how to call video in html:
<div>
{% video vid.url '600x400'%}
</div>
```

## html iframes:

One way to embed a youtube video in html is through using the Iframe tag:
```
<iframe width="560" height="315" src="https://www.youtube.com/embed/N_WP7Llytis" 
title="YouTube video player" frameborder="0" 
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; 
picture-in-picture" allowfullscreen></iframe>

# This whole tag can be generated in the youtbe using the share video button 
and then choosing the embed option.

```


