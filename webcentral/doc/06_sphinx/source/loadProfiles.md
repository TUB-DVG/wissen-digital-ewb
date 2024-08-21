# Load Profiles

This page gives a short overview of the content, data and models used for generation of heating, tapwater and electricity load profiles. Data can be displayed and downloaded as csv.

## Framework 

The load profiles are written in dash, where the graph is generated and integrated into the frontend with an iframe. Detailed Descriptions is given in: [Plotly Apps](./plotlyApps.md)

Factors and the Test Reference Year (TRY) are stored using csv. The data is loaded, and with user input turned into a plotly dash graph.Real weather data is obtained from Deutscher Wetterdienst using the wetterdienst Library. 

## Theoretical Background 

- For the electricity loadprofiles the [Standard Load Profiles by BDEW](https://www.bdew.de/energie/standardlastprofile-strom/) are used. 
- For the Heat approximation the method of [Marcus Hellwig, 2003, "Entwicklung und Anwendung parametrisierter Standard-Lastprofile"](https://mediatum.ub.tum.de/download/601557/601557.pdf) is applied. 
- For gathering weather data, we use the open source library [wetterdienst](https://github.com/earthobservations/wetterdienst).
