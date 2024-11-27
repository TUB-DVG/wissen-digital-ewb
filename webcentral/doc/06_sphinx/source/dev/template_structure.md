# Template structure
The django template language allows to load dynamic content into HTML-templates. These templates can be composed together from different smaller templates, allowing to follow a DRY-approach and increase readability and maintainability. In the following section the structure of the templates used in EWB-Wissensplattform is described in detail.

## Grid listing pages
The grid listing style page is used several times on the website to show and filter collections of tools, datasets, norms- & technical standards etc. The following figure shows the template components, which combined together build a listing-grid style page. This is done for the use-cases page: 
```{mermaid}
graph TD;
    pages/listing_grid.html --> partials/explanation_show_more.html;
    pages/listing_grid.html --> partials/search_bar.html;
    partials/explanation_show_more.html --> use_cases/explanation.html;
    pages/listing_grid.html --> partials/listing_results.html;
    partials/listing_results.html --> partials/pagination.html;
```
A template from the `pages/`-template folder acts as a base template. Into this template partial-temlates are included from the template folder `partials/`. 
A partial can also contain a template: The `partials/explanation_show_more.html`-template provides the general structure for the collapsable-component, which holds the explanation text for the current-site. The explanation text itself is app-specific static content, which is loaded from the app-template directory, in the example above from the `use_cases/`-directory.
The universal templates from the folders `partials/` and `pages/` need data from the app specific `views.py` method as context. The needed data is described in the following sections.

### Context for listing_grid.html
The following key value pairs need to be given in a dictionary to the django `render()`-method when rendering the `pages/listing_grid.html` template. 
`title`: Page title of the listing page.
`focusBorder`: Can be `technical`, `operational`, `ecological`, `legal` or `global`. Based on the used focus name, the border of the content container is colored in the color put inside the `_variables.scss`-file in `/webcentral/src/webcentral_app/static/css/`

### Context for explanation_show_more.html
`focusBorder`: Can be `technical`, `operational`, `ecological`, `legal` or `global`. Based on the selected value, the expanded explanation container will have the color of the respective focus.
`title`: Global heading of the listing page.
`introductionText`: Introductionary text shown under the `title`
`pathToExplanationTemplate`: Describes where the template-engine can find the app-specific explanation template. An example is `use_cases/explanation.html`, which holds the markup text, which is shown when clicking on the `+ Learn more about the topic` text on the [use-cases](https://wissen-digital-ewb.de/en/useCases_list/) listing page.
![Pages associated with app](../img/context_for_explanation_template.png)
The image above shows where the context variables are rendered.


### Context for search_bar.html

