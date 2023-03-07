# Database backup strategies
Various strategies for backing up and migrating the database are described below.
## Stratgy 1: Backup via textual/binary backup file
### Create the backup
Using the Postgres client, an image of the database can be saved in binary or as text in a file.
The command to create the image is:
```
pg_dump dbname > dumpfile
```
Where `dbname` is the name of the database to be backed up and `dumpfile` is the filename to which the image is written.
The image consists of sql commands that set a database to the state of `dbname` at the time `pd_dump` is executed.
Depending on what environment the Webcentral web application was in, a separate way of backing up the database is required:
*docker-compose-production-environment*:
In the root directory of the Webcentral repository (where the .env file is located), the following commands must be executed:
```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```
This will start the webcentral multi-container app in production mode. The following commands must then be executed in a new terminal:
```
source .env
docker container exec database pg_dump -U $POSTGRES_USER $POSTGRES_DB > dump.sql
```
This saves the database image in the `dump.sql` file.
The `docker container exec` command executes a command in the running `database` container. The command that is executed is the
`pg_dump` command, which is called with the `-U` option to specify the database user. If this is not specified postgres uses the
default user `postgres` with which it is not possible to access the dtaen with sub. `pg_dump` writes the output to STDOUT, which is dumped via the `>`
to the file `dump.sql`.
To backup the static data, the files uploaded by users must be backed up. These files are located in the Docker volume `static-data`,
```
docker cp webcentral:/vol/webcentral/media ../mediaBACKUP
```
This copies the media files to a folder `mediaBACKUP`-which is located in the parent directory of the current directory.
*Docker-Compose Development-Environment*
To create the database image, the same procedure can be followed as for the Production environment.
The static media files are stored under `01_application/webcental_app/media` and can be copied manually.
### Importing the backup
To import the database image, the created `.sql` file must be moved to the `postgres/` folder, which is located in the git root directory. Furthermore, in the `.env` file
the environment variable `DATABASE_PLAIN_SQL_FILE=db_webcentral_Backup_20220714.sql` must be updated to the sql filename. Furthermore the backed up
media files must be copied to the folder `01_application/webcentral_app/media`.

The import of the image is then performed by running the `restoreDB.sh` script:
```
    bash postgres/restoreDB.sh
```
It is important that the script is executed from the project root directory, otherwise the `.env` file cannot be loaded.
In this way, both the database and the static data was brought up to the state of the backup.
## Strategy 2: Direct copying of Docker volumes
The Docker volume `pgdata`, which contains the postgres database, or `static-data`, which contains the static data, can be copied directly. They are located in the `/var/lib/docker/volumes` folder.
For the copy operation, the script `scripts/migrateDockerVolumes.sh` exists, which migrates a Docker volume from the machine `SOURCE_HOST_ADDRESS` with the user `SOURCE_HOST_USER` to the machine `TARGET_HOST_ADDRESS` with the user `TARGET_HOST_USER`. These environment variables are set in the `.env` file for the current working machine as the source machine and the VServer as the target machine. During the copy process the user of the source machine as well as the user of the target machine will be asked several times for the password. FURTHER, it should be noted that the user on the target machine must be in the docker user group for the script to run without errors. The script must be run from the root of the git repo and the name of the volume to be copied must be specified as the first argument:
```
    bash scripts/migrateDockerVolumes.sh src_pgdata
```
This command copies the src_pgdata volume to the target computer.

*Translated to german on 07.03.2023*

# Datenbank-Backup Strategien
Im Folgenden werden verschiedene Strategien zum sichern und migrieren der Datenbank beschrieben.
## Stratgie 1: Sicherung über textuelle/binäre Sicherungsdatei
### Erstellen der Sicherung
Mithilfe des Postgres-Clients kann ein Abbild der Datenbank im binären bzw. als Text in einer Datei gespeichert werden.
Der Befehl zum Erstellen des Abbilds lautet:
```
pg_dump dbname > dumpfile
```
Dabei bezeichnet `dbname` den Namen der Datenbank, die gesichert werden soll und `dumpfile` den Dateinamen, in den das Abbild geschirieben wird.
Das Abbild besteht aus sql-Befehlen, welche eine Datenbank auf den zustand von `dbname` zum Zeitpunkt der Befehlausführung von `pd_dump` setzen.
Je nachdem, in welcher Umgebung die Webcentral-Web-Applikation vorlag, ist ein gesonderter Weg zur Sicherung der Datenbank nötig:
*Docker-Compose Production-Umgebung*:
Im Wurzelverzeichnis des Webcentral-Repositories (dort wo die .env-Datei liegt) müssen die Folgenden Befehle ausgeführt werden:
```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```
Dies startet die webcentral-Multi-Container-App im Production-Modus. In einem neuen Terminal müssen dann die Folgenden Befehle ausgeführt werden:
```
source .env
docker container exec database pg_dump -U $POSTGRES_USER $POSTGRES_DB > dump.sql
```
Dies speichert das Datenbank-Abbild in der Datei `dump.sql`.
Der `docker container exec`-Befehl führt ein Kommando in dem laufenden Container `database` aus. Bei dem ausgeführten Befehl handelt es sich um den
`pg_dump`-Befehl, welcher mit der `-U`-Option aufgerufen wird, um den Datenbank-Nutzer zu spezifizieren. Ist dieser nicht angegeben verwendet postgres den
Standart-User `postgres` mit dem es mit Unter nicht möglich ist, auf die Dtaen zuzugreifen. `pg_dump` schreibt die Ausgabe nach STDOUT, welche über den `>`
in die Datei `dump.sql` umgeleitet wird.
Zum Backup der statischen Daten müssen die durch Benutzer hochgeladene Dateien gesichert werden. Diese Dateien befinden sich im Docker-Volumen `static-data`,
```
docker cp webcentral:/vol/webcentral/media ../mediaBACKUP
```
Dies kopiert die media-Dateien in einen Ordner `mediaBACKUP`-welcher im Eltern-Verzeichnis des aktuellen Verzeichnisses liegt.
*Docker-Compose Development-Umgebung*
Zum Erstellen des Datenbank-Abbilds kann genauso wie für die Production-Umgebung vorgegangen werden.
Die statischen Media-Dateien werden unter `01_application/webcental_app/media` gespeichert und können manuell kopiert werden.

### Einspielen der Sicherung
Zum Einspielen des Datenbank-Abbildes muss die erstellte `.sql`-Datei in den `postgres/`-Ordner verschoben werden, welcher sich im git-Wurzelverzeichnis befindet. Weiterhin muss in der `.env`-Datei
die Umgebungsvariable `DATABASE_PLAIN_SQL_FILE=db_webcentral_Backup_20220714.sql` auf den sql-Dateinamen aktualisiert werden. Weiterhin müssen die gesicherten
Media-Dateien in den Ordner `01_application/webcentral_app/media` kopiert werden.

Das Einspielen des Abbilds wird dann durch Ausführung des `restoreDB.sh`-Skripts durchgeführt:
```
    bash postgres/restoreDB.sh
```
Dabei ist wichtig, dass das Skript aus dem Projekt-Wurzelverzeichnis ausgeführt wird, da sonst das `.env`-Datei nicht geladen werden kann.
Auf diese Weise wurde sowohl die Datenbank-, als auch die statischen-Daten auf Stand der Sicherung gebracht.

## Strategie 2: Direktes Kopieren der Docker-Volumes
Das Docker-Volume `pgdata`, welches die postgres-Datenbank enthält, bzw. `static-data`, welches die statischen Daten enthält, können direkt kopiert werden. Sie befinden sich im Ordner `/var/lib/docker/volumes`.
Für den Kopiervorgang existiert das Skript `scripts/migrateDockerVolumes.sh`, welches von der Maschine `SOURCE_HOST_ADDRESS` mit dem Benutzer `SOURCE_HOST_USER` ein Docker Volume auf die Maschine `TARGET_HOST_ADDRESS` mit dem Benutzer `TARGET_HOST_USER` migriert. Diese Umgebungsvariablen sind im `.env`-File für die momentane Arbeitsmaschine als Quellrechner und den VServer als Zielrechner gesetzt. Während des Kopiervorgangs wird mehrmals nach dem Passwort, sowohl vom Benutzer der Quellmaschine, als auch vom Benutzer des Zielrechner gefragt. WEiterhin sollte beachtet werden, dass der Benutzer auf dem Zielrechner in der docker-Benutzergruppe sein muss, damit das Skript ohne Fehler abläuft. Das Skript muss aus dem Wurzelverzeichnis des git-Repos ausgeführt werden und der Name des zu kopierenden Volumes muss als erstes Argument spezifiziert werden:
```
    bash scripts/migrateDockerVolumes.sh src_pgdata
```
Dieser Befehl kopiert das src_pgdata Volume auf den Zielrechner.

