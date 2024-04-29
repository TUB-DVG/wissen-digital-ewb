# Translation of Content
This document describes how the content of the website can be translated to english.
For the static content the django-internationalization middleware is used, which is called "i18n" internally.
For the translation of the database-content the python-package "model-translation" is used.
In the following sections the procedutre to translate the static content and of the dynamic content is summarized.

## Translation of Static content
(Source: https://docs.djangoproject.com/en/4.2/topics/i18n/)
To translate static content the django internationalization middleware is used. The process is composed of 
an internationalization step and an translation step. Thereby means internationalization the step of marking all strings that should be translated inside the 
source code, while localization is the step of actually providing translations.

### Internationalization
German content, which should be shown in english, needs to be tagged explictily. In a template that can be done using the
{% translate %} or the {% blocktranslate %}{% endblocktranslate %} tags.
E.g. 
```
   {% translate "Hallo" %}
   {% blocktranslate %}Hallo{% endblocktranslate %}
```
both would mark the string "Hallo" as a translation string. 
Note: These django-tags can be used after the tags are loaded with the the tag {% load i18n %}. 
This tag needs to be specified in each template, in which {% translate %} or {% blocktranslate %} is used.

When strings inside python-code should be translated, the string is given to the django `gettext`-method.
In the django-documentation it is imported as a underscore `_`:
```
   from django.utils.translation import gettext as _
```
So the following python-statement would mark `Hallo` to be translated:
```
   greetings = _("Hallo")
```

After marking all strings, which should be translated, in the HTML-templates and in the python-code a language file can be created
in which the mapping between the string inside the source code and the translation together with the location inside the source code

### Localization
The translation for the marked trings is provided inside a language-file. This file can be created using the Django `makemessages` command. 
To go through all source-code files and finding all marked strings the following command canbe executed:
```
   python3 manage.py makemessages -a
```
Since this command has to be specfied inside the container, at first a webcentral-container shell has to be opened. Alternativly the `run`-script can be
used to directly execute the `makemessages`-command from the host-terminal:
```
   ./run makemessages
```
This command creates an up-to-date text-version of a language file. It is located in `/01_application/webcentral_app/locale/en/LC_MESSAGES/django.po`. It is composed of different blocks, whereby for each marked translation string in the source code one block in the language-file is created. An block looks like this: 
```
    #: StartSearch/views.py:231
    msgid "Forschungsprojekt"
    msgstr ""
```
The first line marks the location inside the source-code, where the translation-string was marked. The second line represents the marked translation-string and the third line shows the english-translation. To translate the marked string a translation has to be entered into the quotes. An translated block could look as follows:
```
     #: StartSearch/views.py:231
    msgid "Forschungsprojekt"
    msgstr "Research project"
```
After every block has been translated, the file needs to be compiled to a binary state. In that way  the look-up will be much faster. To do that, the following django-command needs to be executed inside the docker-webcentral-container:
```
   python manage.py compilemessages
```
Alternativly the run script can be used:
```
./run compilemessages
```
After that, wehen seleting the english-website the english-string should be shwon instead of the german version.

## Translation of database-content
For the transdlation of the database-content the python-package "model-translation" is used, which is installed as dependency inside the webcentral-container.