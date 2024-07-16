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
This template includes two partial templates: The `descriptionContainer.html` and the `fourBoxesContainer.html`-template. With the `descriptionContainer.html`, a partial consisting of a heading and a description text can be included into a page. The text-content needs to be provided by the django-view. When calling the render-function with a page-wide template, a context-dictionary needs to be provided. That collection of key-value pairs need to have the following keys to render the `descriptionContainer.html` properly:
   
    - `focusBorder`: Can take one of the following string values: `ecological`, `operational`, `legal`, `technical`. With that key, the link-color of links inside the description text can be set to the focus-color.
    - pathToImage (optional key-value pair): Specifies a path to a image-icon, which will be displayed left to the heading.
    - `heading`: The heading of the description container.
    - `showMorePresent` (optional key-value pair): Key, which gets a boolean value to determine if the description text should be cut off after a number of character and a expandable box should be present to make the whole text visinble after clicking "show more". If `showMorePresent` is set to `True` the key `charNumberToShowCollapsed` needs to be present with a integer value, representing the number of character, which should be shown in the collapsed state of the collapsable-container.
    - `explanaitionText`: holds the text-content below the heading.

## Search Bar Template Documentation

The Search-Bar HTML-Template is used as a partial on all pages where a search through a collection of elements should be possible.
It makes it possible to search the elements through a text search and by different categories of filters. Furthermore it is possible to trigger the
coparison mode from within the search-bar. It can be included into a page-wide template by adding the following Django-template tag into a page-wide template at the position, where the search-bar should be shown:
```
    {% include "partials/search-bar.html" %}
```
After inlcuding the search-bar, the corresponding context needs to be set in the view-function, which renders the page-wide template. For the search-bar, the following key-value pairs need to be set in the context-dictionary:
    - `optionList`: List of dictionaries
        Based on the value of this key, the select-inputs will be created. The list-length specifies the number of select-elements, which will be rendered. Each list-item is a dictionary with the keys `placeholder`, `objects` and `fieldName`. `placeholder` is put as a placeholder on the select-element. `objects` holds a list of elements, which will be shown as items inside the select input. `fieldName` holds the name of the database attribute name.


     
