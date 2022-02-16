In this document the main ideas of the workflow is documented.

# workflow data into data base

## automatic data implementation

The raw data (source) processed by python scripts and functions into file in common
data formats like csv or json (maybe later specify the format). The generated
file pushed/migrated into the data base with python tools.

**source >python> csv >python> DB**

### places of the functions and scripts

- [ ] the places of the functions and scripts (maybe in our central DVG repo)

## manual edit
The data can edit manually at "admin pages".

# Structure of the data base
## actual structure and sources of the csv-DB
see [figure](./sources2db-csv-db.png)
[drawio](./sources2db.drawio)
## structure and sources of the postgreSQL
see [figure](./sources2db-postgreSQL_projected.png) 
[drawio](./sources2db.drawio)
- the file we implement into the data base have to have the right names of the
  columns and use the Foerderkennzeichen (fkz) as primary key


The structure is shown the Entity Relationship Model 
- [ ] insert Link to the model
The specific connection between the sources and the tables in the data base is
documented in the table
- [ ] insert Link to the table


Idea 1: table of the data base are related to the sources of the data; dont
mix the data

Idea 2: Source is code into the name of the feature

note: the unit can be stored with the feature, there is a "data type" called "Numeric with Unit"

# design
## bootstrap theme 
- challenge: color schema and suitable page arrangement 
- related to the EWB-color-schema
- needed page types:
  - external:
   - Start page
   - About page
   - Tables with search and Download function
   - Graphs with choice possibilities
   - Contact page with data upload
   - Overview content/publication
   - Interactive plots/graphs (nice to have)
   - Interactive calculator, like https://hri-pira.github.io/
   - Survey tool / banchmarking
   - Tags activate and deactivate to move through the structured tree (iöw und udK)
  - internal
   - Tables with search function (tables editable, downloadable)
   - Graphs with choice function
   
- "wir nutzen Bootstrap als moderenes Frontend-Framework. Es liefert
  standardiseirte Bausteine für ein User-Interface."
- "we use bootstrap as modern frontend framework. It provides standarized
  objects(bricks) for the user interface"
- getbootstrap.com
  - https://around.createx.studio/
  - https://themes.getbootstrap.com/preview/?theme_id=103332
    - tool with figures
  - https://themes.getbootstrap.com/preview/?theme_id=7340
# Tests

## Add column to a table at the data base
1. add a new column to the db via django models
- it works
2. add a data set to this column
    - csv with fkz and content for this new column
    - I'm not shure how it works to bring, the data in to data base when
      ForeignKeys are used
# Open questions / raw ideas

## Authentication ( User Groups):
This youtube series explains User Registration, Login Authentication and User Role Based Permissions very thoroughly.
https://www.youtube.com/watch?v=tUqUdu0Sjyc&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&index=14

The implementation of these features need to be discussed: How far do we want to add user authentication? (Front-End: Do we have pages that we want to restrict?)
## ERD

Must be the feature name equal to the primary key of the connected table?
How can I include data types, descriptions and units (where to put?)
we use the [Martin-Notation](https://de.wikipedia.org/wiki/Martin-Notation)

## store only strings?

# Done Tests
## Add column to a table at the data base
add a new column to the db via django models ( a default value must be given,
 since the addition can happen even with filled datasets) add a data set to
 this column
    - csv with fkz and content for this new column


# Solved Questions
## models django
How to add descriptions and units of the attributes aka features?
https://docs.djangoproject.com/en/dev/ref/models/fields/#help-text

help_text is a variable that we can add when defining fields in models.py:
Exp: myfield = models.CharField(max_length=100, help_text="This is the grey text")

## enargus format not straight
- column ´thema´ sometimes without ´ ¨ ´
- [ ] check the xml file 
