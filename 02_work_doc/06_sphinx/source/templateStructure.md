# Template structure
This document describes the HTML-template structure. This structure follows the idea of small completed components, which compose a website together. This approach helps to minimize the amount of needed HTML-code and therefore decreases the complexitiy and increases the readibility of the code. Furthermore, code-changes can be easily deployed to all sites of the website without rhe need for repetitive work.

In general, there are 2 types of HTML-templates:
    - page
    - partial-templates
The page templates are the entrypoint for the django-render-process. On these templates the django `render()`-function is called at the end of a django view function. An example for a view-function, which refers to one of the page-wide templates can be found inside the `pages/` folder. 
```
def Datenschutzhinweis(request):
    """Call render function for datenschutzhinweis page."""
    return render(request, "pages/Datenschutzhinweis.html")
```
The function `Datenschutzhinweis(request)` calls the `render()` function, with the argument `pages/Datenschutzhinweis.html`, which is a page-wide template.
The following code shows an example for a page-wide template:
```
{% extends 'base.html' %}
{% load i18n %}
{% block title %}{% translate "Geschäftsmodelle – good-practice" %}{% endblock %}

{% load static %}
{% block content %}
    <div class="content container">
        <div class="row">{% include "partials/descriptionContainer.html" %}</div>
        <div class="boxes" id="container-start-focus">
            {% include "common/fourBoxesContainer.html" %}
        </div>
{% endblock %}
```
This template includes two partial templates: The `descriptionContainer.html` and the `fourBoxesContainer.html`-template. 
