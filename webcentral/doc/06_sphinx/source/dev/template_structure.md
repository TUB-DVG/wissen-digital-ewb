# Template structure
The django template language allows to load dynamic content into HTML-templates. These templates can be composed together from different smaller templates, allowing it to follow a DRY-approach and increase readability and maintainability. In the following section the structure of the templates used in EWB-Wissensplattform prject is described in detail.

## Grid listing pages
The grid listing style page is used several times on the website to show and filter collections of tools, datasets, norms- & technical standards etc. The following figure shows the template components, which combined together build a listing-grid style page. This is done for the use-cases page: 
```{mermaid}
graph TD;
    pages/listing_grid.html --> partials/explanation_show_more.html;
    pages/listing_grid.html --> partials/search_bar.html
    partials/explanation_show_more.html --> use_cases/explanation.html;

```
A template from the `pages/`-template folder acts as a base template. Into this template partial-temlates are included from the template folder `partials/`. 
A patial can also contain a template: The `partials/explanation_show_more.html`-template provides the general structure for the collapsable-component, which holds the explanation text for the current-site. The explanation text itself is app-specific static content, which is loaded from the app-temaplate directory `use_cases/`. 

