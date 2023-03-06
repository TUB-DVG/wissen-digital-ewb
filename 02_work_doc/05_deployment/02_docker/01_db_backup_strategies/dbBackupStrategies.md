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
Zum Einspielen des Datenbank-Abbildes muss die erstellte `.sql`-Datei in den `postgres/`-Ordner verschoben werden. Weiterhin muss in der `.env`-Datei
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
Für das Kopieren sind root-Rechte nötig.


