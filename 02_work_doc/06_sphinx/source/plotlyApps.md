### Plotly Apps 

To integrate timeseries in an interactive way we use [plotly Dash](https://plotly.com/examples/). Basically, within a django app, a dash app is initated and exported to the HTML frame. 

Currently, three different dash apps are provided: 

- [Loadprofiles](02_work_doc\06_sphinx\source\loadProfiles.md)
-- Heat and DHW
-- Electricity Demand 
- [Use Cases](02_work_doc\06_sphinx\source\useCases.md)

In this part of the documentation, the general technical setup and requirements are explained. The apps themself and data are explained in the specific documents. 

## Framework 

The implementation of the dashp app will be epxlained examplary with the "Stromlast App". However, general functionality of the framework is the same for each of the apps. 

For each dash app, a folder is created called "Dash_app" within the respective Django app. E.g. in the Case of "Stromlast App" ''../../../01_application/webcentral_app/LastProfile/Dash_app''. 

Each app has three key components and needs to be integrated into the frontend. 

### Layout Definition

The application's layout is defined using Dash's `html` and `dcc` components:

- **Title**: Displays a centered title "Stromlast Approximation".
- **Dropdown**: Allows users to select the type of application (e.g., household, agricultural business) from a list of options.
- **Input Field**: Provides a field for the user to input the annual energy requirement in kWh/a.
- **RadioItems**: Allows users to select a specific month or view data for the entire year.
- **Buttons**: Two buttons are included:
  - One to start the approximation process.
  - Another to download the data as a CSV file.
- **Graph**: A loading component that wraps a Plotly graph, which will display the power load profile based on user inputs.

### Callbacks

Several callbacks are defined to handle the interactive components of the application:

- **`update_layout`**: This callback updates the text and options in the dropdown, radio items, and buttons based on the current language. It ensures that the labels and placeholders are appropriately localized.

- **`updatePowerGraph`**: This callback generates and updates the power load profile graph based on the user's selected application type, energy requirement, and the month to display. The graph is created using Plotly's `Scatter` plot and customized with appropriate labels and titles.

- **`downloadAsCsv`**: This callback handles the CSV download functionality. When the download button is clicked, it generates a CSV file of the data, including headers that reflect the user's input for energy requirements and selected application type.


### Django Intgreation 

To add plotly to Django add the following things too the settings.py :


```
INSTALLED_APPS = [
    ...
    "LastProfile.apps.LastprofileConfig",
    "django_extensions",
    "django_plotly_dash",
    ...
]

MIDDLEWARE = [
    ...
    "django_plotly_dash.middleware.BaseMiddleware",
    ...
]

```

### Fronted Integration 

The graph is exported and integrated in the HTML frontend with an iframe. In the respective HTML the dash app needs to be added. 

```
<div class= "container" style="height: 100vh ;">
<iframe src="/django_plotly_dash/app/Stromlast/" style="
top: 0;
left: 0;
width: 100%;
  height: 100%;
" sandbox="allow-downloads allow-scripts allow-same-origin" frameborder="0"></iframe>
</div>
```