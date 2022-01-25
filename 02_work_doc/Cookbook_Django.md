## Set up the Django project and app

Create a parent directory and initialize git repo

```
mkdir djangodemo
cd djangodemo
git init
```

Activate the `django` Python environment and start the Django project `mysite`.

```
activate django
django-admin startproject mysite
```

Alternatively, clone `mysite` from git. In this case, create a new environment with
```
conda create -n mysiteenv python=3.5
activate mysiteenv
pip install django 
```

This creates the folder structure `djangodemo/mysite/mysite`. The [Django Tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/#creating-the-polls-app) installs an app in the `djangodemo/mysite` directory at the level of the `manage.py` file, ...
> ...so that it can be imported as its own top-level module, rather than a submodule of mysite.

Therefore, go to `djangodemo/mysite` and start the `myapp` app
```
cd mysite
python manage.py startapp myapp
```

Thus, `djangodemo/mysite` now contains both a `mysite` and a `myapp` folder.

## Create a Hello World view

Add the Hello World text to `myapp/views.py`:

```Python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the index.")
```

Then, create a new file for the urlconfs of this app at `myapp/urls.py` and enter

```Python
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

Finally, point the top-level urlconf at `mysite/urls.py` to the app's urlconfs at `myapp/urls.py` (both are in the top-level `mysite` folder):

```Python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^myapp/', include('myapp.urls')),
    url(r'^admin/', admin.site.urls),
]
```

Go to the top `mysite` folder, activate the Django Python environment and run the test server with `python manage.py runserver`. The Hello World view is rendered at http://localhost:8000/myapp/.

## Set up the Postgres database (on Windows)

[This tutorial](http://gregblogs.com/tlt-setting-up-postgres-with-django-on-windows/) is quite helpful.

Make sure *psycopg2* (`pip install psycopg2`) and of course Postgres are installed.

In *PGAdmin*'s `Login/Group roles` create a user `dbuser` with all priviledges granted. Then, create a database `djangodemo` and set `dbuser` as owner. Connect the database by clicking on it in the tree-view.

In `mysite/settings.py`, replace the `DATABASES` part with

```Python
DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangodemo',
        'USER': 'dbuser',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

While at it, the [Django tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial02/#database-setup) recommends to set the time zone to the local one, i.e. `TIME_ZONE = 'Europe/Berlin'`

Then, migrate the default `INSTALLED_APPS` to the database with `python manage.py migrate`.


## Add the first models

In `myapp/models.py`, add the first model definitions. Don't forget to add the `str` representations. And note that it is also possible to add custom methods:

```Python
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

The app's model file needs to be activated by registering it in the `settings.py` file:

```Python
INSTALLED_APPS = [
    'myapp.apps.MyappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Then, make the migrations and migrate:

```
python manage.py makemigrations myapp
python manage.py migrate
```

## Set up the Django admin

Run `python manage.py createsuperuser` to create the `admin` login.

To make the models visible in the Admin page, add them in `myapp/admin.py`, e.g.:

```Python
from .models import Choice, Question

admin.site.register(Question)
admin.site.register(Choice)
```

## Build real views using templates

More views can be added to `myapp/views.py`:

```Python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myapp/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(question.id,)))
```

These need to be wired into the urlconf:

```Python
from django.conf.urls import url

from . import views

app_name = 'myapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /myapp/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /myapp/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /myapp/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```

In order to use templates, the safest way is to create a folder `myapp/templates/myapp/`. This avoids mixed up templates from different apps.

Add templates like `myapp/templates/myapp/index.html`:

```HTML
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'myapp:detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

`myapp/templates/myapp/detail.html`:

```HTML
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'myapp:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

`myapp/templates/myapp/results.html`:

```HTML
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'myapp:detail' question.id %}">Vote again?</a>
```

## Use generic views

[Continue here](https://docs.djangoproject.com/en/1.10/intro/tutorial04/#use-generic-views-less-code-is-better)