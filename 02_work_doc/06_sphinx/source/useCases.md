## Use Cases 

The Use Cases provide a visualization for interdependencies of digitalization and the research framework. 

The general dash integration is described at [Plotly Apps](./plotlyApps.md).

Besides the dash integration, as Django app is developed. 

## `UseCase` Model Documentation

The `UseCase` model in this Django application represents a django app.

### Fields

- **`item_code`** (`CharField`, `max_length=25`):  
  A unique code representing the item or service. Is used as an item identifier. 

- **`useCase`** (`CharField`, `max_length=50`):  
  Describes the specific service or scenario that is being referenced. In our case SRI Service E-12: Reporting information regarding electricity consumption. 

- **`sriLevel`** (`CharField`, `max_length=255`, `verbose_name="SRI-Zuordnung"`):  
  Indicates the Smart Readiness Indicator (SRI) level associated with the use case. This classification provides insights into the smart readiness and functionality level of the service. In our case: 
  
  -- Functionality level 0 (as non-smart default) : None, 
  -- Functionality level 1 	: Reporting on current electricity consumption on building level,
  -- Functionality level 2 	: Real-time feedback or benchmarking on building level,
  -- Functionality level 3 	: Real-time feedback or benchmarking on appliance level,
  -- Functionality level 4  : Real-time feedback or benchmarking on appliance level with automated personalized recommendation.


- **`levelOfAction`** (`CharField`, `max_length=100`):  

  Defines the level at which the use case is examined. In our case: 
  
  - spatial, 
  - temporal.


- **`degreeOfDetail`** (`CharField`, `max_length=100`):  

  Specifies the granularity or detail level of the level of action: 
  
  - spatial,
  -- euqipment,
  -- one building, 
  -- three buildings, 
  - temporal, 
  -- 5 seconds,
  -- 1 hour, 
  -- 1 month.

- **`focus`** (`ManyToManyField` to `Focus` model):

  Represents the focus areas impacted by the use case. In our cse:
  
  -- economic,
  --ecological, 
  -- user perspective, 
  --or technical aspects.

- **`idPerspectiveforDetail`** (`PositiveIntegerField`):  
  A reference to the perspective or detail level for further classification. This integer represents specific perspectives on the effects or impacts.

- **`effectEvaluation`** (`CharField`, `max_length=1`, `choices=[('+', 'Positive'), ('-', 'Negative'), ('o', 'Neutrale')]`):  

  Categorizes the effect of the use case as positive, negative, or neutral. This provides a quick overview of the intended or achieved outcome by repsective focus. 


- **`effectName`** (`CharField`, `max_length=255`):  

  Name for the specific effect or impact resulting from the use case. 

- **`effectDescription`** (`TextField`):  

  Provides a detailed description of the effect or impact of the use case. 

- **`furtherInformation`** (`TextField`, `blank=True`, `null=True`):  

  Offers additional details or context regarding the use case that are not covered in other fields. This is an optional field.

- **`icon`** (`TextField`, `blank=True`, `null=True`):  

  Contains a text-based icon representation related to the use case. This could be used for visual representation in user interfaces.


## Use Cases plotly documentation 


The IDEAL dataset was used to illustrate these effects in more detail. This dataset contains monitoring data for 255 households from the UK and Scotland. Of these, 39 households were monitored within a closely-meshed system. For the purpose of illustration, the closely-monitored households 62, 105, and 106 were utilized. Despite this close monitoring, it is evident that not all sensors function properly at all times (as seen in household 106). Due to the size of the data, only one day is displayed. 

The data presented includes the average consumption over time intervals of five seconds, 15 minutes, and one hour. Both the individual values of the households and the sum of the load profiles (three buildings) are shown. The exemplary representation demonstrates how different aggregations (temporal and spatial) affect the visibility of certain effects. Through high-frequency measurements, individual effects can be observed clearly, which may be lost in other aggregations. The aim is to provide users with a quantitative and qualitative understanding of the effects of digitalization and their interactions. For example, resources and energy are required for the creation and operation of measurement technology; however, more precise measurements also enable more individualized feedback to users or more accurate detection of faults.

The goal is to uncover the different effects of digitalization and to highlight the interaction of various requirements. In doing so, we address several key questions:

  -  How does the frequency (5 seconds, 15 minutes, 1 hour) affect the visibility of effects?
  -  How do individual aggregations (appliances, total consumption, three buildings) affect the visibility of effects?
  -  What can be observed in the graph?

## Further Information 

[Smart Readiness Indicator](https://energy.ec.europa.eu/topics/energy-efficiency/energy-efficient-buildings/smart-readiness-indicator/implementation-tools_en)

[IDEAL Data: Pullinger et al., The IDEAL household energy dataset, electricity, gas, contextual sensor data and survey data for 255 UK homes, ci Data 2021 May 28;8(1):146. doi: 10.1038/s41597-021-00921-y.](https://www.nature.com/articles/s41597-021-00921-y)