# Dash :
Dash is a low-code frameword for building data apps and rendering them in the web browser. Since Dash apps are viewed in the web browser, Dash is inherently cross-platform and mobile ready.

## Alternatives to Plotly_Dash:

 ### IBM Watson Studio:
 Watson Studio, formerly Data Science Experience or DSX, is IBM’s software platform for data science. The platform consists of a workspace that includes multiple collaboration and open-source tools for use in data science.

In Watson Studio, a data scientist can create a project with a group of collaborators, all having access to various analytics models and using various languages (R/Python/Scala). Watson Studio brings together staple open source tools including RStudio, Spark and Python in an integrated environment, along with additional tools such as a managed Spark service and data shaping facilities, in a secure and governed environment.

 ### R Studio
RStudio is an integrated development environment for R, a programming language for statistical computing and graphics. It is available in two formats: RStudio Desktop is a regular desktop application while RStudio Server runs on a remote server and allows accessing RStudio using a web browser. 

###  Jupyter Dashboards:
https://jupyter-dashboards-layout.readthedocs.io/en/latest/
The dashboards layout extension is an add-on for Jupyter Notebook. It lets you arrange your notebook outputs (text, plots, widgets, …) in grid- or report-like layouts. It saves information about your layouts in your notebook document

### Other:
https://www.trustradius.com/products/plotly-dash/competitors

## Why Dash:
Dash by Plotly looks like a great way for a Python developer to create interactive web apps without having to learn Javascript and Front End Web development. Since django is also Python based, the integration of Dash with the Django framework is well documented and a specific app has been already developped(Django_Plotly_Dash).

## Classic Dash vs Django app Dash:
https://django-plotly-dash.readthedocs.io/en/latest/introduction.html


Since our webframework is entirely based on Django, it would stand to reason that we should opt to use the django_plotly_dash app for a variety of reasons:

1. Tracebility: Most of the features that we already implemented into our webframework are through django apps: Import_export,CMS and our different apps that we created and most of them can be traced back in the settings file and any missing packages can be easily identified. In addition, any error that occurs in the webframework would be django based which makes debugging much easier.

2. According to the documentation of the django-plotly-dash app, the purpose of django-plotly-dash is to enable Plotly Dash applications to be served up as part of a Django application, in order to provide these features:

    * Multiple dash applications can be used on a single page.
    * Separate instances of a dash application can persist along with internal state.
    * Leverage user management and access control and other parts of the Django infrastructure.
    * Consolidate into a single server process to simplify scaling.


3. Easy integration with different django apps: Since we already have a variety of data sets available in our webframework, instead of creating a specific plotly app for each. By using the django_plotly_dash app, we gain access to a skeleton plotly app that we simply need to update and with the app (as mentionned above), we could display multiple dash applications on a signle page.







