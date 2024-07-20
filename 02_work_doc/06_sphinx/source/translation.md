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
For the translation of the database-content the python-package "model-translation" is used, which is installed as dependency inside the webcentral-container.
That packet uses additional database attributes to store different translations for a database-attribute. First, all django-model-fields which should be translated, have to be marked for translation. This is done by adding a additional python script called `translation.py` to the django-app, which model-fields should be translated. For each model-class inside the apps `models.py` a class is created which inherits from `TranslationOptions`. It has a fields attribute in which the names of all model-fields are provided, which should be translated.
Finally the created class gets registered with the corresponding model-class:
```
    class ToolsTranslationOptions(TranslationOptions):
        fields = (
            "shortDescription", 
            "userInterfaceNotes",
            "lastUpdate",
            "licenseNotes",
            "furtherInformation",
            "provider",
            "yearOfRelease",
        )
    translator.register(Tools, ToolsTranslationOptions)
```
"model translation" expects now for each of the provided model-field names additional database attributes for each present language. In case of the Wissensplattform for each specified attribute a "_de" and "_en" attribute is execpted. E.g. besides "shortDescription" there should also be "shortDescription_de" and "shortDescription_en" inside the "Tools" table. Otherwise an database-lookup error is thrown and the App doesnt work. The missing attributes can be added manually, which would look similar to the following code:
```
ALTER TABLE public.publications_type
ADD COLUMN "bibtex_types_de" varchar(256);
```
The above example adds the german version of the "bibtex_types"-attribute to the publications_type-table. 
Alternativly the `sync_translation_fields` can be used, which is a interactive utility to alter the database table. It can be executed by calling it together with the `manage.py` file:
```
    python manage.py sync_translation_fields
```
Or the `run`-script can be used:
```
    ./run sync_translation_fields 
```
After the database is set up correctly the default german content needs to be copied into the "_de"-field. E.g. for all rows the content of "shortDescription" has to be copied inside "shortDescription_de". This can be done with a custom django command:
```
   python manage.py update_translation_fields
```
After that only the english attribute needs to be filled with content. A convenient way is via the django-admin panel.
