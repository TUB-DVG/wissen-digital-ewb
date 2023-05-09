# Wetterdienst Python Library :
A more detailed and in depth Documentation can be found 
at https://wetterdienst.readthedocs.io/en/latest/index.html

This Library serves as an API( application interface) for easy access to 
the data made available by 4 providers:
- DWD ( German Weather Service)
- ECCC ( Environment and Climate change canada)
- NOAA ( NAtional OCeanic and Atmospheric Administration)
- WSV ( Federak Waterways and Shipping Administration of Germany)

The wetterdienst Library does not provide any innate graphing features, 
but provides feautres that help the user filter, sort and display the data available
from the 4 providers through their different networks.

# Coverage :

This is an overview of the data that can be accessed through the wetterdienst Library:

### 1. DWD (Deutscher Wetterdienst / German Weather Service / Germany)

        Historical Weather Observations

                - Historical (last ~300 years), recent (500 days to yesterday), now (yesterday up to last hour)

                - Every minute to yearly resolution

                - Time series of stations in Germany

        Mosmix 
                - statistical optimized scalar forecasts extracted from weather models

                - Point forecast

                - 5400 stations worldwide

                - Both MOSMIX-L and MOSMIX-S is supported

                - Up to 115 parameters

        Radar

                - 16 locations in Germany

                - All of Composite, Radolan, Radvor, Sites and Radolan_CDC

                - Radolan: calibrated radar precipitation

                - Radvor: radar precipitation forecast

### 2. ECCC (Environnement et Changement Climatique Canada / Environment and Climate Change Canada / Canada)

        Historical Weather Observations

                - Historical (last ~180 years)

                - Hourly, daily, monthly, (annual) resolution

                - Time series of stations in Canada

### 3. NOAA (National Oceanic And Atmospheric Administration / National Oceanic And Atmospheric Administration / United States Of America)

        Global Historical Climatology Network

                - Historical, daily weather observations from around the globe

                - more then 100k stations

                - data for weather services which don’t publish data themselves

### 4. WSV (Wasserstraßen- und Schifffahrtsverwaltung des Bundes / Federal Waterways and Shipping Administration)

        Pegelonline

                - data of river network of Germany

                - coverage of last 30 days

                - parameters like stage, runoff and more related to rivers

Note: this provider is not available after installing the Library, in addition a provider called eumetnet is available in the data but not accessable.

# Accessing Data:

## Available APIs:
The available APIs can be accessed by the top-level API Wetterdienst. 
This API also allows the user to discover the available APIs of each service included:
```
In [1]: from wetterdienst import Wetterdienst

In [2]: Wetterdienst.discover()
Out[2]: 
{'DWD': ['OBSERVATION', 'MOSMIX', 'RADAR'],
 'ECCC': ['OBSERVATION'],
 'NOAA': ['GHCN']} 
```
To load any of the available APIs pass the provider and the network of 
data to the Wetterdienst API:
```
In [3]: from wetterdienst import Wetterdienst

In [4]: API = Wetterdienst(provider="dwd", network="observation")
```

## Request classes :
#### Request arguments :

Data can be accessed through a request class defined in the wetterdienst 
Library (each service/network has its own required class).
**Note:** For the Radar service the class is named values instead of request.

Example:
- to pull DWD historical obervations data, the corresponding class is called **DwdObservationRequest**.

- for DWD mosmix data , the corresponding class is called **DwdMosmixRequest**.

In general, the classes of wetterdienst follow a 3-part naming pattern:
The abreviation of the provider ( Mentioned above ) with 
the first letter in caps, followed by the network abreviation with 
the first letter in caps, followed by the class name with the first 
letter being in caps.

For example, the class to pull data from DWD Mosmix network is 
the request class and its call would be:
- DwdMosmixRequest

#### Parameters :
##### <ins> General :</ins> 
Typical requests are defined by five arguments:

- parameter/dataset
- resolution
- period
- start_date
- end_date

Arguments start_date and end_date are possible replacements for the period
argument if the period of a weather service is fixed. In case both arguments
are given they are combined thus data is only taken from the given period 
and between the given time span.


Each of the 3 arguments (parameter,resolution,period) have different options,
depending on the network, that are defined in an enum class 
( naming of these classes follows the same convention as above) :

- parameter/dataset : available in the Dataset enum class or 
the Paremeter class ( not an enum class).
    -  **Notes** : The parameter class holds more options 
    than the Dataset class but a specific resolution is required (example below ).
    - Some dataset options are not available for all resolutions (Refer to table below).
- resolution : available in the Resolution enum class 
- period : available in the Period enum class.

<div class="md-typeset__scrollwrap"><div class="md-typeset__table"><table>
<colgroup>
<col style="width: 24%">
<col style="width: 11%">
<col style="width: 11%">
<col style="width: 11%">
<col style="width: 11%">
<col style="width: 11%">
<col style="width: 11%">
<col style="width: 11%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>ParameterGranularity</p></th>
<th class="head"><p>1_minute</p></th>
<th class="head"><p>10_minutes</p></th>
<th class="head"><p>hourly</p></th>
<th class="head"><p>subdaily</p></th>
<th class="head"><p>daily</p></th>
<th class="head"><p>monthly</p></th>
<th class="head"><p>annual</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><cite>PRECIPITATION = “precipitation”</cite></p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>TEMPERATURE_AIR = “air_temperature”</cite></p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>TEMPERATURE_EXTREME = “extreme_temperature”</cite></p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>WIND_EXTREME = “extreme_wind”</cite></p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>SOLAR = “solar”</cite></p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>WIND = “wind”</cite></p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>CLOUD_TYPE = “cloud_type”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>CLOUDINESS = “cloudiness”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>DEW_POINT = “dew_point”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>PRESSURE = “pressure”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>TEMPERATURE_SOIL = “soil_temperature”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>SUNSHINE_DURATION = “sun”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>VISBILITY = “visibility”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>WIND_SYNOPTIC = “wind_synop”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>MOISTURE = “moisture”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-odd"><td><p><cite>CLIMATE_SUMMARY = “kl”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
</tr>
<tr class="row-even"><td><p><cite>PRECIPITATION_MORE = “more_precip”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
</tr>
<tr class="row-odd"><td><p><cite>WATER_EQUIVALENT = “water_equiv”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
</tr>
<tr class="row-even"><td><p><cite>WEATHER_PHENOMENA = “weather_phenomena”</cite></p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>-</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
<td><p>+</p></td>
</tr>
</tbody>
</table></div></div>


The user can define them in three different ways:
- by using the exact enumeration e.g.

        Parameter.CLIMATE_SUMMARY

- by using the enumeration name (our proposed name) e.g.

        "climate_summary" or "CLIMATE_SUMMARY"

- by using the enumeration value (most probably the original name) e.g.

        "kl"

This leaves a lot of flexibility to the user defining the arguments either by what they know from the weather service or what they know from wetterdienst itself.

Enumerations for resolution and period arguments are given at the main level e.g.
```
In [1]: from wetterdienst import Resolution, Period
```
or at the domain specific level e.g.
```
In [2]: from wetterdienst.provider.dwd.observation import DwdObservationResolution, DwdObservationPeriod
```
Both enumerations can be used interchangeably however the weather services 
enumeration is limited to what resolutions and periods are actually 
available while the main level enumeration is a summation of all kinds 
of resolutions and periods found at the different weather services.

Example:
```
parameter_option1=DwdObservationParameter.DAILY.PRECIPITATION_MORE
parameter_option2=DwdObservationDataset.PRECIPITATION_MORE
resolution=DwdObservationResolution.DAILY
period=DwdObservationPeriod.HISTORICAL

# To display all the available options for the classes above, the following commands can be used:

# Enumeration at main level:
In[1]: 
from wetterdienst.provider.dwd.observation import DwdObservationPeriod, \
DwdObservationResolution, DwdObservationDataset, DwdObservationParameter

print(DwdObservationPeriod._member_names_) # Display options of Period argument
print(DwdObservationResolution._member_names_) # Display options of Resolution argument
print(DwdObservationDataset._member_names_) # Display options of Parameter argument
print(dir(DwdObservationParameter)) # Display resolution options of Parameter argument
print(dir(DwdObservationParameter.DAILY)) # Display options of Parameter argument for daily resolution

# NOTE: parameter argument seems to have some inconsistencies for some options from DwdObservationParameter.

Out[1]:
DwdObservationPeriod
['HISTORICAL', 'RECENT', 'NOW']

DwdObservationResolution
['MINUTE_1', 'MINUTE_10', 'HOURLY', 'SUBDAILY', 'DAILY', 'MONTHLY', 'ANNUAL']

DwdObservationDataset
['PRECIPITATION', 'TEMPERATURE_AIR', 'TEMPERATURE_EXTREME', 'WIND_EXTREME', 'SOLAR', 'WIND', 'CLOUD_TYPE', 'CLOUDINESS', 'DEW_POINT', 'PRESSURE', 'TEMPERATURE_SOIL', 'SUN', 'VISIBILITY', 'WIND_SYNOPTIC', 'MOISTURE', 'SOIL', 'CLIMATE_SUMMARY', 'PRECIPITATION_MORE', 'WATER_EQUIVALENT', 'WEATHER_PHENOMENA', 'WEATHER_PHENOMENA_MORE']

DwdObservationParameter
['ANNUAL', 'DAILY', 'HOURLY', 'MINUTE_1', 'MINUTE_10', 'MONTHLY', 'SUBDAILY', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']       

DwdObservationParameter.DAILY
['CLIMATE_SUMMARY', 'CLOUD_COVER_TOTAL', 'COUNT_WEATHER_TYPE_DEW', 'COUNT_WEATHER_TYPE_FOG', 'COUNT_WEATHER_TYPE_GLAZE', 'COUNT_WEATHER_TYPE_HAIL', 'COUNT_WEATHER_TYPE_RIPE', 'COUNT_WEATHER_TYPE_SLEET', 'COUNT_WEATHER_TYPE_STORM_STORMIER_WIND', 'COUNT_WEATHER_TYPE_STORM_STRONG_WIND', 'COUNT_WEATHER_TYPE_THUNDER', 'HUMIDITY', 'KL', 'MORE_PRECIP', 'MORE_WEATHER_PHENOMENA', 'PRECIPITATION_FORM', 'PRECIPITATION_HEIGHT', 'PRECIPITATION_MORE', 'PRESSURE_AIR_SITE', 'PRESSURE_VAPOR', 'RADIATION_SKY_LONG_WAVE', 'RADIATION_SKY_SHORT_WAVE_DIFFUSE', 'RADIATION_SKY_SHORT_WAVE_DIRECT', 'SNOW_DEPTH', 'SNOW_DEPTH_EXCELLED', 'SNOW_DEPTH_NEW', 'SOIL_TEMPERATURE', 'SOLAR', 'SUNSHINE_DURATION', 'TEMPERATURE_AIR_MAX_200', 'TEMPERATURE_AIR_MEAN_200', 'TEMPERATURE_AIR_MIN_005', 'TEMPERATURE_AIR_MIN_200', 'TEMPERATURE_SOIL', 'TEMPERATURE_SOIL_MEAN_002', 'TEMPERATURE_SOIL_MEAN_005', 'TEMPERATURE_SOIL_MEAN_010', 'TEMPERATURE_SOIL_MEAN_020', 'TEMPERATURE_SOIL_MEAN_050', 'TEMPERATURE_SOIL_MEAN_100', 'WATER_EQUIV', 'WATER_EQUIVALENT', 'WATER_EQUIVALENT_SNOW_DEPTH', 'WATER_EQUIVALENT_SNOW_DEPTH_EXCELLED', 'WEATHER_PHENOMENA', 'WEATHER_PHENOMENA_MORE', 'WIND_GUST_MAX', 'WIND_SPEED', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

# Enumeration at specific level:
# ( Not recommended since some enumerations are availalbe for some networks but not for others)

In[2]: 
from wetterdienst import Period, Resolution

print(Resolution._member_names_)
print(Period._member_names_)

Out[2]:
['MINUTE_1', 'MINUTE_5', 'MINUTE_10', 'HOURLY', 'HOUR_6', 'SUBDAILY', 'DAILY', 'MONTHLY', 'ANNUAL', 'UNDEFINED', 'DYNAMIC']
['UNDEFINED', 'HISTORICAL', 'RECENT', 'NOW', 'FUTURE']
```
#
##### <ins> Service Specific :</ins>
As mentionned above not all requests require the 5 arguments mentionned above.

**Only the parameter, start_date and end_date** argument may be needed 
for a request, as the resolution and period of the data may be 
fixed (per station or for all data) within individual services.
However if the period is not defined, it is assumed that the user 
wants data for all available periods and the request is handled that way.

The following command can be used to display all possible arguments for
the requests of the different services/networks.
```
In[1]:
from wetterdienst.provider.eccc.observation import EcccObservationRequest

from wetterdienst.provider.dwd.observation import DwdObservationRequest

from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest

from wetterdienst.provider.noaa.ghcn import  NoaaGhcnRequest

import inspect

argspec = inspect.getfullargspec(EcccObservationRequest).args
signature  = inspect.getfullargspec(DwdObservationRequest).args
signature2  = inspect.getfullargspec(NoaaGhcnRequest).args
signature3  = inspect.getfullargspec(DwdMosmixRequest).args
signature4  = inspect.getfullargspec(DwdRadarValues).args

print('EcccObservationRequest')
print(argspec)

print('DwdObservationRequest')
print(signature)

print('DwdMosmixRequest')
print(signature3)

print('NoaaGhcnRequest')
print(signature2)

print('DwdRadarValues')
print(signature4)

Out[1]:
# self is to be ignored.
EcccObservationRequest
['self', 'parameter', 'resolution', 'start_date', 'end_date']

DwdObservationRequest
['self', 'parameter', 'resolution', 'period', 'start_date', 'end_date']

DwdMosmixRequest
['self', 'parameter', 'mosmix_type', 'start_issue', 'end_issue', 'start_date', 'end_date']

NoaaGhcnRequest
['self', 'parameter', 'start_date', 'end_date']

DwdRadarValues
['self', 'parameter', 'site', 'fmt', 'subset', 'elevation', 'start_date', 'end_date', 'resolution', 'period']

```


#### Querying data :
When it comes to values one can either query all data by request.all() 
or typically query by station_id via request.filter_by_station_id().

Alternatively the API offers various possibilities to query stations 
by geographic context. Further details can be found below.

To check all query options the **dir()** command can be used.
```
In[1]:
from wetterdienst.provider.dwd.observation import DwdObservationRequest
print(dir(DwdObservationRequest))

Out[1]:
['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', 
'__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
'__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__weakref__', '_abc_impl', '_all', '_base_columns', 
'_coerce_meta_fields', '_data_range', '_dataset_accessor', '_dataset_base', 
'_format_unit', '_get_periods', '_has_datasets', '_has_tidy_data', 
'_historical_interval', '_interval', '_now_interval', '_now_local', '_parameter_base', 
'_parameter_to_dataset_mapping', '_parse_dataset_and_parameter', '_parse_parameter',
'_parse_parameter_and_dataset', '_parse_period', '_parse_station_id', '_period_base',
'_period_type', '_recent_interval', '_resolution_base', '_resolution_type', 
'_setup_discover_filter', '_tz', '_unique_dataset', '_unit_tree', '_values', 'all',
'convert_timestamps', 'datasets', 'describe_fields', 'discover', 'filter_by_bbox', 
'filter_by_distance', 'filter_by_name', 'filter_by_rank', 'filter_by_sql', 
'filter_by_station_id', 'frequency', 'kind', 'provider', 'tz']
```

#### Accessing data example :
```
# Get station information for a given parameter/dataset, resolution and period.

In [1]: from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationDataset, DwdObservationPeriod, DwdObservationResolution

In [2]: stations = DwdObservationRequest(
   ....:     parameter=DwdObservationDataset.PRECIPITATION_MORE,
   ....:     resolution=DwdObservationResolution.DAILY,
   ....:     period=DwdObservationPeriod.HISTORICAL
   ....:     ).all()

In [3]: df = stations.df
In [4]: print(df.head())
Out[4]:
  station_id  ...                state
0      00001  ...    Baden-Württemberg
1      00002  ...  Nordrhein-Westfalen
2      00003  ...  Nordrhein-Westfalen
3      00004  ...  Nordrhein-Westfalen
4      00006  ...    Baden-Württemberg

[5 rows x 8 columns]
```
The above function returns a Pandas DataFrame with information about the available stations.

```
# Filter for specific station ids:

In [1]: from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationDataset, DwdObservationPeriod, DwdObservationResolution

In [2]: stations = DwdObservationRequest(
   ....:     parameter=DwdObservationDataset.PRECIPITATION_MORE,
   ....:     resolution=DwdObservationResolution.DAILY,
   ....:     period=DwdObservationPeriod.HISTORICAL
   ....:     ).filter_by_station_id(station_id=("1048",))

In [3]: df = stations.df
In [4]: print(df)
Out[4]:
    station_id                 from_date  ...               name    state
928      01048 1926-04-25 00:00:00+00:00  ...  Dresden-Klotzsche  Sachsen

[1 rows x 8 columns]
```

After selecting the right stations, data can be accessed.
```
In[5]:  print(next(stations.values.query()))
Out[5]:

        station_id             dataset       parameter  \
0           01048  precipitation_more              rs
1           01048  precipitation_more              rs
2           01048  precipitation_more              rs
3           01048  precipitation_more              rs
4           01048  precipitation_more              rs
...           ...                 ...             ...
117023      01048  precipitation_more  snow_depth_new
117024      01048  precipitation_more  snow_depth_new
117025      01048  precipitation_more  snow_depth_new
117026      01048  precipitation_more  snow_depth_new
117027      01048  precipitation_more  snow_depth_new

                            date  value  quality
0      1926-04-25 00:00:00+00:00    0.0      1.0
1      1926-04-26 00:00:00+00:00    0.0      1.0
2      1926-04-27 00:00:00+00:00    0.0      1.0
3      1926-04-28 00:00:00+00:00    0.0      1.0
4      1926-04-29 00:00:00+00:00    0.0      1.0
...                          ...    ...      ...
117023 2021-12-27 00:00:00+00:00    0.0      3.0
117024 2021-12-28 00:00:00+00:00    0.0      3.0
117025 2021-12-29 00:00:00+00:00    0.0      3.0
117026 2021-12-30 00:00:00+00:00    0.0      3.0
117027 2021-12-31 00:00:00+00:00    0.0      3.0

[117028 rows x 6 columns]
```


# Geospatial support :

Inquiring the list of stations by geographic coordinates:

- Calculate weather stations close to the given coordinates and set of parameters.

- Select stations by

    - rank (n stations)

    - <ins>distance</ins> (km, mi,…) : geographic distance of station <= <ins>distance</ins>

    - bbox:
        - A bounding box (usually shortened to bbox) is an area defined by 
        two longitudes and two latitudes, where:
            * Latitude is a decimal number between -90.0 and 90.0.
            - Longitude is a decimal number between -180.0 and 180.0.

            They follow the standard format of:
            ```
            bbox = left,bottom,right,top
            bbox = min Longitude , min Latitude , max Longitude , max Latitude  
            ```

** Distance with default (kilometers)
```
# Filtering by Distance

In [1]: from datetime import datetime

In [2]: from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationDataset, DwdObservationPeriod, DwdObservationResolution

In [3]: stations = DwdObservationRequest(
   ....:     parameter=DwdObservationDataset.TEMPERATURE_AIR,
   ....:     resolution=DwdObservationResolution.HOURLY,
   ....:     period=DwdObservationPeriod.RECENT,
   ....:     start_date=datetime(2020, 1, 1),
   ....:     end_date=datetime(2020, 1, 20)
   ....: )
   ....: 

# Filter the stations that fit the parameters above and with distance up to 30 km.
In [4]: df_distance = stations.filter_by_distance(
   ....:     latitude=50.0,
   ....:     longitude=8.9,
   ....:     distance=20,
   ....:     unit="km"
   ....: ).df
   ....: 

In [5]: print(df_distance)
  station_id                 from_date  ...   state   distance
0      02480 2004-09-01 00:00:00+00:00  ...  Bayern   9.759385
1      04411 2002-01-24 00:00:00+00:00  ...  Hessen  10.156943
2      07341 2005-07-16 00:00:00+00:00  ...  Hessen  12.891318

[3 rows x 9 columns]

# Filtering by bounding box

In [6]: df_bbox = stations.filter_by_bbox(
   ....:     left=8.9,
   ....:     bottom=50,
   ....:     right=9,
   ....:     top=52,
   ....: ).df

In [7]: print(df_bbox)

     station_id                 from_date                   to_date  height  \
0      02480 2004-09-01 00:00:00+00:00 2022-05-02 00:00:00+00:00   108.0
1      02907 1991-01-01 00:00:00+00:00 2022-05-02 00:00:00+00:00     7.0
2      05014 2004-07-01 00:00:00+00:00 2022-05-02 00:00:00+00:00     7.0
3      05133 2004-09-01 00:00:00+00:00 2022-05-02 00:00:00+00:00   295.0

   latitude  longitude                   name               state
0   50.0643     8.9930              Kahl/Main              Bayern
1   54.7903     8.9514                   Leck  Schleswig-Holstein
2   53.2758     8.9857  Worpswede-Hüttenbusch       Niedersachsen
3   51.3344     8.9132   Twistetal-Mühlhausen              Hessen

[4 rows x 8 columns]
```

