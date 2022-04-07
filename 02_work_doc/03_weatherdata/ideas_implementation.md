Here should stored the general idea how to implement the weather data at our
Wissensplattform. Also the todos should added here.

author: Falk
date: march 2022

# Genearal points

## data set
- DWD: XXX , TRY from bbsr (put csv into db as independent table and plot data form here,
  should be the elegant way, Dirty way put csv into the app)
- [ ] choose data set
- [ ] decision: data set included to our data base, or online connection  
## general layout of the page/s
### should include
- source of the data set
- description of the data set
- *active* plot of different values of the data set
  - values: 
    - temperature
    - pressure
    - humidity
    - rain
    - wind velocity
    - ...
  - region should be chooseable
  - maybe choose by a drop down menu
  - maybe also possible to plot more the an value 
### layout
- [ ] choose basic layout/s
- [ ] general structur of the html pages (one page with subpages or is one page
      enough)
## implementation into the start-page
- get there own menu entry next to Anwendungen
- Question: behind the login?
## tools
- [ ] choose plot tool/s


## workflow implementation
1. small test maybe not in django (this test/demo could also provided by out
   Wissensplattform)
2. small test implemented in django (own app)
3. discuss the full implantation, what we do 
4. implement the to the django project (own app) 
5. deployment (to the server)

# general focus of presentation of the weather data
- make it easy to use 
- with simple examples, maybe the examples from the DWD are simple enough, Im not sure right now

# Todos from Falks container
- [ ] Umsetzen Wetterdaten als Inhalt für die Wissensplattfrom
  - [ ] Recherche
  - [ ] Designvorschlag erarbeiten
  - [ ] Workflow erarbeiten
  - [ ] Inplementieren
  - [ ] Testen
  - [ ] Dokumentieren (am Besten paralell machen)

# Wetterdaten Anbieter Display
- Name des Anbieters
- Kurzbeschreibung der Art von Daten
- Datenkategorien als Tags ? (Wind, Wasserqualität, Temperatur, ...)
- Link zur Homepage
- Bild/Logo
- Woher die Daten? (open data, Messungen eines Instituts, ...)
- Plot
- Start (und Ende) der Datenaufnahme (je nach Kategorie, generell)