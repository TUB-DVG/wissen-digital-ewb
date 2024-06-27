How is the description-text loaded?
-----------------------------------

This document explains how the static introductory description texts on each overview site is loaded onto the site.
On default, django uses HTML-templates, where data is rendered into on the backend-site. 
When having different overview sites like (tools-overview, business models-overview, ...) for each overview site an HTML-template is needed.
That adds a huge overhead of HTML pages and also makes the maintanance difficult, since if changes are needed to make in the general structure, they 
have to be made on every HTML file.

Due to that reason it is tried to only use one template for the description on all sites.
That means, that the content has to be provided from the backend. For now the static content is defined in the corresponding
django view function and given to the django page render-function in form as a python dictionary, which is often referred to as context. 
The django-render function then puts the content inside the context-dictionary into the template. Therefore it uses the django-template-lanugage, which is a subset of the jinja2-template language.
The names of the placeholders definied in the HTML-templates correspond to the keys in the context-dictionary.

The description-template is a partial, which is included into a page-template or a app-specific page-template. It has the following DTL variables, which have to be present in the context dictionary given to the
django render function.