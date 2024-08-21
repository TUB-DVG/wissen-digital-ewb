# weather_data

This repo contains all information related to weather data collected in the Begleitforschung Energiewendebauen by Module 4.

- The DWD provides data through it's  [open data portal](https://opendata.dwd.de/). Documentation is given [here](https://www.dwd.de/DE/leistungen/opendata/hilfe.html). Additional code (e.g. a python implemention to download data ) is given [here](https://github.com/DeutscherWetterdienst).
  - are docker container, maybe to much for the pilot
  - GRIB2 data format: https://www.dwd.de/DE/leistungen/opendata/help/modelle/grib2_erlaeuterungen.pdf?__blob=publicationFile&v=1
    - could understand as kind of Datenbank
    - looks complex in the first impression (usage of docker containers)
    - maybe better to use only a small part for the pilot
    - handling of weather data not trivial (maybe)
    - maybe we should start with the downloader https://github.com/DeutscherWetterdienst/downloader
      - and plot simple curve
- The BBSR provides data for test reference years [TRY](https://www.bbsr.bund.de/BBSR/DE/forschung/programme/zb/Auftragsforschung/5EnergieKlimaBauen/2013/testreferenzjahre/01-start.html;jsessionid=5D9912D230EB887C1F831671303A8A0F.live21304?nn=2544408&pos=2). The TRY provide climate data for the evaluation of thermal behvaviour of buildings. The data can be downloaded for free, but an user account is necessary from this [webpage](https://kunden.dwd.de/obt/index.jsp). The dataformat is csv.  
  - Falk have account
  - download only for one small region 
  

- A cross-plattform software provided by the DOE is [Climate Consulant](https://www.sbse.org/resources/climate-consultant)
- [CCWorldWeatherGen](https://energy.soton.ac.uk/ccworldweathergen/) is an Excel-based tool, that transforms present weather files into files compatible with building perfomance simulation programs.
- The Integrated Carbon Observation System [ICOS](https://data.icos-cp.eu/portal/) provides carbon data.
- The Institute of Ecology at TU Berlin generated a detailed atmospheric [data set](https://www.klima.tu-berlin.de/index.php?show=daten_cer&lan=de) covering the years from 2001 to 2019. 
- A standarised data set on urban climate was developed in the project [UC2](https://dms.klima.tu-berlin.de/). Currently, there is no data available on the webpage.
- [Wetterdienst](https://github.com/earthobservations/wetterdienst) is an open source library based on pandas providing open weather data. They provide access to DWD data and other instituions.
  - very interessting 
  - when not use TRY than this
  
- [BBSR](https://www.bbsr-energieeinsparung.de/EnEVPortal/DE/Regelungen/Testreferenzjahre/GEG/Berechnungen-node.html) provides further information on the usage of TRY in Gebäudeenergiegesetz (GEG). 
- [WUFI](https://wufi.de/de/service/downloads/erstellung-von-wetterdateien/) gives an overview of categories and usage of weather data for simulation.
- Commerical databases and applications like [Meteonorm](https://meteonorm.com/) provide a variety of functions. 
- Information about solar radiation is available via: [PVGIS](https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system_en)
- The [PVLIB Python](https://github.com/pvlib/pvlib-python) provides code to access data [PVGIS data](https://pvlib-python.readthedocs.io/en/stable/_modules/pvlib/iotools/pvgis.html).



# To Do
- Provide overview of data integration in Simulation Tools
- Provide example API for DWD 
