## Contents
 - [Set up the Django project and app](#set-up-the-django-project-and-app) 
 - [Create a Hello World view](#create-a-hello-world-view) 
 - [Create Template Pages & Base Layout](#create-template-pages-and-base-layout) 
 - [Bring Bootstrap stuff to live](#bring-bootstrap-stuff-to-live) 
 - [Set up pic from static](#set-up-pic-from-static) 
 - [Adaption of the static content](#adaption-of-the-static-content) 
 - [Set up the about page](#setup-the-about-page) 
 - [Set up the Postgres database](#set-up-the-postgres-database) 
 - [Add the first models](#add-the-first-models) 
 - [Set up the Django admin](#set-up-the-django-admin) 
 - [Automatic implementation of data via scripts](#automatic-implementation-of-data-via-scripts) 
- [Testing developing tools/advices](#testing-developing-tools-and-advices) 
- [Views](#views) 
- [Build page for one project in detail](#build-page-for-one-project-in-detail) 
- [Button to switch to a page with content of one project](#button-to-switch-to-a-page-with-content-of-one-project) 
- [Build real views using templates](#build-real-views-using-templates) 
- [Add new app based on hard coded templates](#add-new-app-based-on-hard-coded-templates) 

## Set up the Django project and app

Create a parent directory and initialize git repo
```
mkdir djangodemo
cd djangodemo
git init
```

Activate the `venv` Python environment and start the Django project `mysite`.
```
source venv/bin/activate                                                                    
django-admin startproject mysite
```

Alternatively, clone `mysite` from git. In this case, create a new environment with
```
conda create -n mysiteenv python=3.X
or: python3 -m mysiteenv
activate mysiteenv
or: source mysiteenv/bin/activate
pip install django 
```

Run server
```
cd mysite
python3 manage.py runserver
```

This creates the folder structure `djangodemo/mysite/mysite`. The [Django Tutorial](https://docs.djangoproject.com/en/1.10/intro/tutorial01/#creating-the-polls-app) installs an app in the `djangodemo/mysite` directory at the level of the `manage.py` file, ...
> ... so that it can be imported as its own top-level module, rather than a submodule of mysite.

Therefore, go to `djangodemo/mysite` and start the `myapp` app
```
python3 manage.py startapp pages
```

Thus, `djangodemo/mysite` now contains both a `mysite` and a `myapp` folder.

## Create a Hello World view
### put link to the Application definition
- add following to INSTALLED_APPS in webcentral_app/settings.py
```
    'pages.apps.PagesConfig',
```
### add urls.py in pages folder
add the following text to the urls.py
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index')
]
```
### add function to views.py (define whats happened, when index is surfed)
```
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Hello World</h1>')

```
### to make the new page name known put a reference to webcentral_app/urls.py
add the following to urlpatterns
```
from django.urls import path, include

urlpatterns = [
    path('',include('pages.urls')),
    path('admin/', admin.site.urls),
]
```

## create template pages and Base Layout
### folder of templates (where to look for templates)
- add to webcentral_app/settings.py 
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'templates')],
```
- create folder in webcentral_app named templates
- create in templates a folder named pages
- create in pages 2 files:
    - index.html
    - about.html
- names are not strict, but good to use
- put some content to the .html-file, like  ``<h1>home</h1>``
### make the about-page known
- add to pages/urls.py : 
    path('about', views.about, name='about'),
- add and adjust methods to the views.py
```
def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')
```
### setup base template
- create file base.html in template folder
- put here the basic stuff:
```
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=divice-width, initial-scale=1.0"/>
        <meta http-equiv="X-UA-Compatible" content="ie=edge"/>
         <title>{% block title %} {% endblock %}</title>
    </head>
    <body>
        {% block content %} {% endblock %}
    </body>
</html>
```
- {% %} is [jinja](https://en.wikipedia.org/wiki/Jinja_(template_engine)) syntax, own, kind of php language 
### adapte index.html
- change the code in index.html using base.html
```
{% extends 'base.html' %} 

{% block content%}
<h1>home</h1>
{% endblock %}
```
### bootstrap template (static)
- build up a static bootstrap page or use bootstrap page 
- here i copy the static page from my udemy course https://www.udemy.com/share/101WqE3@FyjsaFOyT0m5_Q4t9JOL9H9tw7nB-pl75FYbae56vt-6vqLpMogdG3CeDAxR6l7Z/
#### make folder
- mkdir static in webcentral_app in webcentral_app
#### copy need stuff: css, fonts, pics, static html page
- cp -r
  ~/Nextcloud/01_Digital_Falk/04_DjangoUdemy/btre_resources/btre_resources/btre_theme/dist/assets/css
  static
- cp -r
  ~/Nextcloud/01_Digital_Falk/04_DjangoUdemy/btre_resources/btre_resources/btre_theme/dist/assets/js
  static
- cp -r
  ~/Nextcloud/01_Digital_Falk/04_DjangoUdemy/btre_resources/btre_resources/btre_theme/dist/assets/webfonts
  static
- cp -r ~/Nextcloud/01_Digital_Falk/04_DjangoUdemy/btre_resources/btre_resources/btre_theme/dist/assets/img/lightbox
   img
- copy of TUB, ECDF, BMWi
#### integrate static stuff
- edit webcentral_app/settings.py
```
STATIC_ROOT= Path.joinpath(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS= [
    Path.joinpath(BASE_DIR, 'webcentral_app/static')
]

```
- run collection the developing static stuff to our official staic stuff in
root of the project
```
 python3 manage.py collectstatic
```

## bring bootstrap stuff to live
### connect bootrap stuff to the base.html
- edit base.html
```
{% load static %}
```
- copy stuff from bootrap index.html in to the base.html, here form the udemy
  tutorial
- after meta
```
        <!-- Font Awesome -->
        <link rel="stylesheet" href="{% static '/css/all.css' %}">
        <!-- Bootstrap -->
        <link rel="stylesheet" href="{% static '/css/bootstrap.css' %}">
        <!-- Custom -->
        <link rel="stylesheet" href="{% static '/css/style.css' %}">
        <!-- Ligthbox -->
        <link rel="stylesheet" href="{% static '/css/lightbox.min.css' %}">
```
- end of body
```
<script src="{% static 'js/jquery-3.3.1.min.js' %}"></script>
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
<script src="{% static 'js/lightbox.min.js' %}"></script>
<script src="{% static 'js/main.js' %} "></script>

```
- remaining some error, which will corrected later
### add footer, navbar and topbar
topbar und navbar copy at the top of the body
```
  <!-- Top Bar -->
  <section id="top-bar" class="p-3">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <i class="fas fa-phone"></i> (617)-555-5555
        </div>
        <div class="col-md-4">
          <i class="fas fa-envelope-open"></i> contact@btrealestate.co
        </div>
        <div class="col-md-4">
          <div class="social text-right">
            <a href="#">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#">
              <i class="fab fa-facebook"></i>
            </a>
            <a href="#">
              <i class="fab fa-linkedin"></i>
            </a>
            <a href="#">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#">
              <i class="fab fa-pinterest"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
    <div class="container">
      <a class="navbar-brand" href="index.html">
        <img src="assets/img/logo.png" class="logo" alt="">
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <ul class="navbar-nav">
          <li class="nav-item active mr-3">
            <a class="nav-link" href="index.html">Home</a>
          </li>
          <li class="nav-item mr-3">
            <a class="nav-link" href="about.html">About</a>
          </li>
          <li class="nav-item mr-3">
            <a class="nav-link" href="listings.html">Featured Listings</a>
          </li>
        </ul>

        <ul class="navbar-nav ml-auto">
          <li class="nav-item mr-3">
            <a class="nav-link" href="register.html">
              <i class="fas fa-user-plus"></i> Register</a>
          </li>
          <li class="nav-item mr-3">
            <a class="nav-link" href="login.html">
              <i class="fas fa-sign-in-alt"></i>

              Login</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>


```
copy the footer at the end of the body, before the JavaScript stuff

```
       <!-- Footer -->
        <footer id="main-footer" class="py-4 bg-primary text-white text-center">
            Copyright &copy;
            <span class="year"></span> TU Berlin, DVG 
        </footer>

```
### make partials of the base.html
- mkdir  templates/partials
- make files: _footer.html, _navbar.html, _topbar
- cut from base.html and past to the files respectively
- base.html connect to the partial files
```
        <!-- Top Bar -->
        {% include 'partials/_topbar.html' %}
        <!-- Nav Bar -->
        {% include 'partials/_navbar.html' %}
        <!-- Main Content -->
        {% block content %} {% endblock %}

        <!-- Footer -->
        {% include 'partials/_footer.html' %}

```

## set up pic from static
- here for the navbar
- add to _navbar.html
```
{% load static %} // new
 <!-- Navbar -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
            <div class="container">
                <a class="navbar-brand" href="index.html">
  // adapted                  <img src="{% static 'img/TU_Logo_lang_RGB_rot.svg' %}" class="logo" alt="">
                </a>
```

## Adaptation of the static content
### phone number and email at topbar
- in  _topbar.html
- search for the content and change
### colors of the navbar
- Info: used bootstrap template use sass, lightbox is for handling the fic
  showing
- https://www.youtube.com/watch?v=pB7EwxwSfVk
- https://www.youtube.com/watch?v=4sosXZsdy-s&t=186s

## setup the about page
### put the main structure in
- use the structure from the tutorial
- replace `<h1>about</h1>` with your content

#### add figure
- copy figure into the folder 01_application/webcentral_app/static 
- to collect the static file run
```
 python3 manage.py collectstatic 
```
- add and adjust code in about.html
- add after "extends" 
```
{% load static %}
```
- adjust the link of the figure
```
<img src="{% static '/img/ER_Diagramm_Draft6-SourceByTabels.png' %}" alt="">
```
#### Linking
- replace links to .html with jinja references in the following kind
- these keys are defined in pages/urls.html
```
<a class="navbar-brand" href="index.html">
to
<a class="navbar-brand" href="{% url 'index' %}">
```
#### highlighting the name of the active page
- it is done by if statements checking the path of the page
- for example for the index page 
- it is done in the _navbar.html
```
   <li class="nav-item active mr-3">
   to
   <li
   {% if '/' == request.path %}
   class="nav-item active mr-3"
  {% else %}
  class="nav-item mr-3"
  {% endif %}
  >
```
- for about 'about' in instate of '/' ==  
### Create a listing app 
- we will us this for the overall project view
- create new app
```
python3 manage.py startapp project_listing
```
- creates new folder
#### connect the new app project_listing to the django project
- new folder in pages/templetes project_listings
- here the related html templetes should be stored
- create:
    - project_list.html
    - project_view.html
    - search.html
- create a separate url.py in project_listing
- put similar content then pages/urls.py , but some adjustments
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='project_listing'),
    path('<int:FKZ>', views.project_view, name='project_view'),  # regarding
    the FKZ, content will shown
    path('search', views.search, name='search'),
]

```
- make a link into the main url.py in webcentral_app folder
- add following:
```
path('project_listing',include('project_listing.urls')),
```
- add the new app to the settings.py in webcentral_app folder into the section INSTALLED_APPS
```
'project_listing.apps.ProjectListingConfig',
```  
#### create view methods for the 3 htmls (project_list, project_view, search)
- edit project_listing/views.py
```
def index(request):
    """
    shows the list of all projects including some key features
    """
    return render(request, 'project_listing/project_list.html')

def project_view(request):
    """
    shows of the key features one project
    """
    return render(request, 'project_listing/project_view.html')

def search(request):
    """
    search page
    """
    return render(request, 'project_listing/search.html')
```
- put simple content to the 
    - project_list.html
    - project_view.html
    - search.html
#### general structure / references of urls
- Top level: webcentral_app/urls.py
    - includes in urlpatterns mostly references to other urls.py files
    - mostly no connection to view-methods included
    - connects the apps (project_listing) and the path extension (project_list)
    - e.g. path('project_list', include('project_listing/urls.py'))
- Mid level: project_listing/urls.py
    - includes the link to the views of this app
    - connect view-methode (e.g. views.search) and path extension (e.g. search)
    - e.g. path('search', views.search, name='search')
- Bottom level: project_listing/views.py 
    - view methodes
    - call the html pages in the templates folder
    - e.g. return render(request, 'project_listing/search.html')
### extend the base.html to the app html pages
- include to 
    - project_list.html
    - project_view.html
    - search.html
    the following:
```
{% extends 'base.html' %}

{% block content %}
<h1>XXXXX </h1>
{% endblock %}

```
### add project list to the html page
- include bootrap code from the tutorial
- code is static in the first step
- adapted the links of the template html code for the django project
- adjust the links and highlighting at the navabr at _navabr.html
```
 <li
                            {% if 'project_list' in request.path %}
                            class="nav-item active mr-3"
                            {% else %}
                            class="nav-item mr-3"
                            {% endif %}
                        >
                            <a class="nav-link" href="{% url 'project_list' %}">Projektliste</a>
                        </li>
```

## Set up the Postgres database 
### Install postgres on system
- *macOS* https://postgresapp.com/
- *windows* https://www.postgresql.org/download/windows/
- *Linux* https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart
    - includes also the setup of the postgres DB
### pgAdmin
- grafical User Interface for PostgreSQL-DB
- https://www.pgadmin.org/
Make sure *psycopg2* (`pip install psycopg2` and `pip install pscopy2-binary`) 
and of course Postgres are installed.
### Postgres Database & User Setup (via terminal)
```
# sudo -u postgres psql
```
You should now be logged into the pg shell
#### Create a database
```
CREATE DATABASE M4_data;
```
#### Create user
```
CREATE USER dbadmint WITH PASSWORD 'abc123!';
```
#### Set default encoding, tansaction isolation scheme (Recommended from Django)
```
ALTER ROLE dbadmint SET client_encoding TO 'utf8';
ALTER ROLE dbadmint SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbadmint SET timezone TO 'UTC';
```
#### Give User access to database
```
GRANT ALL PRIVILEGES ON DATABASE M4_data TO dbadmint;
```
#### Quit out of Postgres
```
\q
```
#### Delate Database
- see  https://www.postgresqltutorial.com/postgresql-drop-database/
Drop, if open connection
```
SELECT *
FROM pg_stat_activity
WHERE datname = '<database_name>';

SELECT	pg_terminate_backend (pid)
FROM	pg_stat_activity
WHERE	pg_stat_activity.datname = '<database_name>';


DROP DATABASE <database_name>;
```
### Postgres Database & User Setup (via pgAdmin) 
In *PGAdmin*'s `Login/Group roles` create a user `dbuser` with all priviledges
granted. Then, create a database `djangodemo` and set `dbuser` as owner.
Connect the database by clicking on it in the tree-view.
### setupt postgresql in django
In `mysite/settings.py`, replace the `DATABASES` part with
Attention: only lower case for the database name
```Python
DATABASES = {  
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'data_m4',
        'USER': 'dbadmint',
        'PASSWORD': 'abc123',
        'HOST': 'localhost',
#        'PORT': '5432',
    }
}
```
### migrate data to the database
Stop server.
Then, migrate the default `INSTALLED_APPS` to the database with `python manage.py migrate`.
Start the server again.
### planing structure of the database
- drawio is a good tool to do this
- for this project see ER_Diagramm_Draft6.drawio in folder 02_work_doc

## Add the first models
- infos: https://docs.djangoproject.com/en/3.2/topics/db/models/#
- possible fields: https://docs.djangoproject.com/en/4.0/ref/models/fields/
- in the first step, here I build a simple structure
### make model for the app project_listing
- edit models.py in folder project_listing
- problem: consistent structure for database and html-pages
- add model teilprojekt (German names, but snake_case style for variables, Upper case 1st letter for classes/tables)
```python
from django.db import models

class Teilprojekt(models.Model):
    fkz = models.CharField(max_length=10, primary_key=True)
    # when  there is a problem try related_name
    enargus_daten = models.ForeignKey('Enargus', null=True, on_delete=models.DO_NOTHING)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.fkz  # maybe change to the shortname of the project


class Enargus(models.Model):
    enargus_id = models.AutoField(primary_key=True)
    laufzeitbeginn = models.DateTimeField(blank=True)
    laufzeitende = models.DateTimeField(blank=True)
    thema = models.CharField(max_length=500, blank=True)
    verbundbezeichnung = models.CharField(max_length=200, blank=
                                          True)
    # forschung = models.ForeignKey('Forschung', null=True, on_delete=models.DO_NOTHING)
    # return as name, when class is called, eg. tables in admin page
    def __str__(self):
        return self.verbundbezeichnung  # maybe change to the shortname of the project



# class Forschung(models.Model):
#     forschung_id = models.AutoField(primary_key=True)
#     bundesministerium = models.CharField(max_length=10, blank=True)
```
- python3 command
```
python3 manage.py makemigrations

python3 manage.py migrate
```
- check in pgAdmin for the tables and variables (right mouse, View/Edit data, all rows)
### extra information
In `myapp/models.py`, add the first model definitions. Don't forget to add the
`str` representations. And note that it is also possible to add custom methods:
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
The app's model file needs to be activated by registering it in the
`settings.py` file:
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
- advice while testing: cudok, abc123

To make the models visible in the Admin page, add them in `project_listing/admin.py`, e.g.:
```Python
from django.contrib import admin

from .models import Teilprojekt, Enargus, Forschung

admin.site.register(Teilprojekt)
admin.site.register(Enargus)
admin.site.register(Forschung)
```
#### more Background regarding Django and build up models
- https://www.youtube.com/watch?v=mOu9fpfzyUg&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=5
- https://www.youtube.com/watch?v=wIPHER2UBB4&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=6

#### reset migrations
- https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html

## automatic implementation of data via scripts
### overview video
- fits not perfect, but helps
- https://www.youtube.com/watch?v=t3BdM6JlAmY

- https://dev.to/guin/writing-a-django-data-migration-with-real-world-example-40m
### practical done
- new py-file in /project_list/ data_import.py 
- important django function ´get_or_create´
- script run in django shell_plus (see below)
- ipython-shell: %run project_listing/data_import
## testing developing tools and advices
### django shell
- simple
- included in django
- python3 manage.py shell

### django shell_plus
- more advanced than django shell
- included in django-extensions
- pip install django-extensions
- https://django-extensions.readthedocs.io/en/latest/installation_instructions.html
- needs ipython to use ipython
- needs add 'django_extensions' to Installed_apps in webcentral_app/settings.py
- ./manage.py shell_plus --ipython
### reload modules in ipython
- https://switowski.com/blog/ipython-autoreload
- %load_ext autoreload
- %autoreload 2

## Views
- views are pages for public outside of the admin area
- for this we use templates
- in views.py templates and models are called (here in folder project_listing)
  - import the needed models
  - load content of the models
  - put content to a variable (here context)
  - make the content available in the html template
```Python
from .models import Teilprojekt # maybe I need also the other models

# Create your views here.

def index(request):
    """
    shows the list of all projects including some key features
    """
    projects = Teilprojekt.objects.all() # reads all data from table Teilprojekt

    context = {
        'projects': projects
    }

    return render(request, 'project_listing/project_list.html', context)

```
- in the template (here project_list.html), bring content in
- make the page dynamic via the data of the content by loops
- general structure:
```Python
{% if projects %}
  {% for project in projects %}
     # html code including content from the db
  {% endfor %}
{% else %}
    <div class="col-md-12">
       <p>No prject in the DB</p>
    </div>
{% endif %}

```
- dynamic content
```Python

{{ project.fkz }} # {{ loopvariable.model_variable }}
{{ project.enargus_daten.laufzeitbeginn }} # {{ loopvariable.foreign_keyName.model_variable }}
```

### django queries including foreign key query
- overview video youtube:
   - https://www.youtube.com/watch?v=PD3YnPSHC-c
   - https://www.youtube.com/watch?v=HhjnQIpXqPc&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=9
   - https://www.youtube.com/watch?v=7a23TbUXfWE&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=9  - https://www.youtube.com/watch?v=HhjnQIpXqPc&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=9
   - https://docs.djangoproject.com/en/4.0/topics/db/queries/

## build page for one project in detail
- fkz is the key, which will passed to the page
- regarding fkz data will be load
- in urls.py '<str:fkz>' must passed, here str instead of int needs to be used,
  because it is a string ;)
- in views.py of the project_listing app the the data is loaded
```Python
def project_view(request, fkz):
    """
    shows of the key features one project
    """
    projekt = get_object_or_404(Teilprojekt, pk= fkz)
    context = {
        'projekt': projekt
    }

    return render(request, 'project_listing/project_view.html', context)

```
- in the html template project_view in templates/project_listing the dynamic
content will be implemented as following example
- replace static content by {{ context_variabel }}
- for foreign key connected table use following 
{{ project.enargus_daten.laufzeitbeginn }} # {{ context_variabel.foreign_keyName.model_variable }}
```html
 <div class="col-md-12">
          <h1 class="display-4">{{ projekt.fkz }}</h1>
          <p class="lead">
            <i class="fas fa-map-marker"></i>{{ projekt.enargus_daten.laufzeitbeginn }}</p>
 </div>

```
## Button to switch to a page with content of one project
- pass the page and the id (here the fkz)
- button at the project_list.html
```html
<a href="{% url 'project_view' project.fkz %}" class="btn btn-primary btn-block">More Info</a>
```
- template tag: {% url 'project_view' project.fkz %} #{% url 'name_of_url_in_urls.py' variabel_to_pass %} 

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

## Add new app based on hard coded templates

- here at the example 'tools overview'

### create new app

```
python3 manage.py startapp tools_over
```
### add model (class) to models.py of the new app
- and delete the class form form the models.py, when moving class from one app to another
- ATTENTION: the table and data from the former app will wiped from the data base by doing the migration 

### activate models of the new app 
- in settings.py of the main 
```Python
INSTALLED_APPS = [
    'pages.apps.PagesConfig',
    'project_listing.apps.ProjectListingConfig',
    'tools_over.apps.ToolsOverConfig',
    'django.contrib.humanize',
    'django.contrib.admin'
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

```
### migrate the new models / tables to the data base
```
python manage.py makemigrations myapp
python manage.py migrate
``` 

### make the new table visible at the admin area
add them in `tools_over/admin.py`, e.g.:
```Python
from django.contrib import admin

from .models import *

admin.site.register(Tools)

```

### Add pages for new app
- In `templates` create new folder for the app, in this case `templates/tools_over`.
Here we used the Eduport-template https://themes.getbootstrap.com/preview/?theme_id=103332.
- Copy the html-template-file from `02_templates/eduport_v1.1.0/template` which you want to use into `templates/tools_over`. In this case we used the template-files `02_templates/eduport_v1.1.0/template/course-grid.html` for `templates/tools_over/tool-listings.html` and `02_templates/eduport_v1.1.0/template/course-detail.html` for `templates/tools_over/tool-detail.html`.
- Copy the parts of the `<head></head>` you need to the head of the base-html-file `templates/base.html`.
- If you want to use a header or navbar and footer or other partials (see [partials section](#add-footer-navbar-and-topbar)) and want to adapt them to the template-design then copy the navbar part of the template into the navbar-partial (e.g. `templates/partials/_navbar.html`) and adapt it to your idea of a navbar/footer/... . 
- Remove the header and footer or other partials-part from your template files and add
```html 
{% extends 'base.html' %}

{% block title %} Your page title {% endblock %}

{% load static %}
{% block content%}
```
and at the end of the file
```
{% endblock content%}
```
- Then edit your template and give it the content you want.

### Displaying and linking all the tools on the tool-listings page
- Here we hand over the id of the tool we want to link as a parameter to the `tool_view` url which then is processed in `tool_view(request, id)` in `tools_over/views.py`.
```html 
<!-- Course Grid START -->

<div class="row g-4">
  {% for tool in page.object_list %} 
    
	<!-- Card item START -->
    <div class="col-sm-6 col-lg-4 col-xl-3">
      <div class="card shadow h-100">
        
		<!-- Image -->
	    {%if tool.image %}
	      <img src=" {{ tool.image.url }}" class="card-img-top" alt="tool image (if=db)">
	    {% else %}

          <img src=" {%static 'img/Default.webp' %}" class="card-img-top" alt="tool image (else)">

        {% endif %}

        <!-- Card body -->
        <div class="card-body pb-0">

          <!-- Title -->
          <h5 class="card-title"><a href="{% url 'tool_view' tool.id %}"> {{ tool.bezeichnung }}</a></h5>
          
		  ...
		  
          <!-- Rating star -->
          <ul class="list-inline mb-0">
            ...
          </ul>
        </div>
 
        <!-- Card footer -->
        <div class="card-footer pt-0 pb-3">
		  ...
        </div>
      </div>
    </div>

	<!-- Card item END -->

 {% endfor %}

</div>
```

### The page for one tool in detail
We have one template `templates/tools_over/tool-detail.html` for all the tool-detail pages. See [how to build page for one project in detail](#build-page-for-one-project-in-detail).
-   id is the key, which will passed to the page
-   regarding id data will be loaded
-   in `tools_over/urls.py` '[str:id](str:id)' must be passed, here str instead of int needs to be used, because it is a string 
`tools_over/urls.py` looks like this:
```python
urlpatterns = [
 path('', views.index, name='tool_list'),
 path('<str:id>', views.tool_view, name='tool_view'),
 path('Post_Review/<str:id>', views.Post_Review, name='Post_Review'),
]
```
-   in views.py of the tools_over app the the data is loaded and preprocessed for display:
```python
class UpdateProperties:
 def __init__(self, class_name, label, color_class):
 self.class_name = class_name
 self.label = label
 self.color_class = color_class

... 

def tool_view(request, id):

 """
 shows of the key features one tool
 """

 tool = get_object_or_404(Tools, pk= id)
 kategorien = tool.kategorie.split(", ")
 lebenszyklusphasen = tool.lebenszyklusphase.split(", ")
 laufende_updates = tool.letztes_update
 letztes_update = UpdateProperties('bi bi-patch-exclamation-fill', 'letztes Update', 'text-danger')
 laufende_updates = UpdateProperties('fas fa-sync', 'Updates', 'text-success')
 
 #changing labels and icon

 update_properties = letztes_update

 if (tool.letztes_update == 'laufend'):
   update_properties = laufende_updates

 context = {
   'tool': tool,
   'kategorien': kategorien,
   'lebenszyklusphasen': lebenszyklusphasen,
   'letztes_update': update_properties,
   'letztes_update_class': update_properties.class_name,
   'letztes_update_color': update_properties.color_class,
   'letztes_update_label': update_properties.label
 }

 return render(request, 'tools_over/tool-detail.html', context)
 ```
We want to have dynamic labels and icons for the display of the last update as it can be "laufend" or a specific date. Hence we check which one the last update is and hand over the classes, and the label to the template.
- In the template we display the information like this
 ```html
 <ul class="list-inline mb-0">
   {% if  tool.average_rating != 0 %}
	 <li class="list-inline-item h6 me-3 mb-1 mb-sm-0"><i class="fas fa-star text-warning me-2"></i>{{tool.average_rating}}/5.0</li>
   {% endif %}
   {% if tool.letztes_update %}
     <li class="list-inline-item h6 me-3 mb-1 mb-sm-0"><i class="{{ letztes_update_class }} {{ letztes_update_color }} me-2"></i>{{tool.letztes_update}}</li>
   {% endif %}
 </ul>
 ```

### Partials - BMWK
Every content that is used in more than one page should be done as a partial.
For example we have this "gefördert durch das BMWK"-section on the home and about page.
So add a new template `_gefoerdert_bmwk.html` to `templates/partials`, add the content and show it on the home and the about page through:
```html
 {% include '../partials/_gefoerdert_bmwk.html' %}
```

## Use generic views

[Continue here](https://docs.djangoproject.com/en/1.10/intro/tutorial04/#use-generic-views-less-code-is-better)


# Useful infos and links
## Structure
- https://django-project-skeleton.readthedocs.io/en/latest/index.html
- https://djangobook.com/mdj2-django-structure/
- https://www.jamesbeith.co.uk/blog/how-to-structure-django-projects/
- 