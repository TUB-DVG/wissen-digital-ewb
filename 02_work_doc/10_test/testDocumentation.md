# Documentation of the automated Tests 
The following Document explain the automated Tests in the folder.

The automated Tests are split into 3 Categories, which are Docker-, Database-, and FrontEnd-Tests.
## Docker-Tests 
The Docker-Tests build and start the docker-compose-development-environment (Heareafter "dev") and the
docker-compose-production-environment (hereafter "prod") and check, if the needed containers are present and healty and if
the needed volumes are present.
## Database-Tests
The Database-Tests test the import functionality of the database. It is checked, 
if the import-functionallity is working: This is done by importing testdata-sets and check, 
if an .yaml-file is produced when conflicts occur. A conflict is present, if a dataset with a referenceNumber
is inserted into the Database, but is already present, with one or more differing fields. In this case 
the conflict is described inside a .yaml-file. The tests check if the written .yaml-files are 
consistent with what is present in the database. 
## FrontEnd-Tests
The Front-End-Tests check, if the userinterface is working as execpted. This is done by 
define programatically  a series of user-actions, like clicking on buttons, hovering over elements
or write text into input fields. It is checked, if the Userinterface acts as expected.
## Quick Start 
To execute the tests, a python virtual environment has to be definied. For that 
the folder needs to be changed into the `10_test`-folder:

```
    cd 02_work_doc/10_test
```

There, the venv-command is executed:

```
    python -m venv testingVenv
```

The `testingVenv` needs to be activated:

```
    . testingVenv/bin/activate
```

Now the python packets are installed into `testingVenv`:

```
    pip install -r requirementsTesting.txt
```

After that, `testingVenv` canbe deactivated:

```
    deactivate
```

The tests cant be executed on an empty database, because then, the `ptjuser` is not present, and the
websites cant be accessed. Thats why an valid dumpfile needs to be specified in the `.env`-file.
For that, go into the webcentral root-directory and check, if the filename in the .env-file, 
which is assigned to `DATABASE_PLAIN_SQL_FILE` environmental-variable is present in `postgres/`-folder.

If you made custom changes to the database, you need to backup it, following the instructions from 
`02_work_doc/05_deployment/02_docker/01_db_backup_strategies/dbBackupStrategies.md`

For executing the tests Bash-scripts are present in `scripts/`. 
One can execute only one of the 3 testcategories by executing the corresponding bash-script from the repo-root-folder:
For the Docker-Test:

```
    bash scripts/runSystemTests.sh
```

For the Database-Tests:

```
    bash scripts/runDBImportTests.sh
```

For the FrontEnd-Tests:

```
    bash scripts/runSeleniumTests.sh
```

If all 3 Testcategories need to be run:

```
    bash scripts/runAllTests.sh
```
