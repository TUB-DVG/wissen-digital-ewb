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


The idea: table of the data base are related to the sources of the data; dont
mix the data

# Tests

## Add column to a table at the data base
1. add a new column to the db via django models
2. add a data set to this column
    - csv with fkz and content for this new column
