# Structure of the EWB Wissensplattform
In the following section the structure of the application is described.
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP| Webserver
    Webserver --> Application
    Application --> Database
```
The above figure shows a high-level overview of the EWB Wissensplattform. The client comunicates 
via HTTP-requests with a webserver. the webserver parses the request and redirects it to the application layer,
where the request is processed. That processing may include fetching data from the database layer. 
The application layer returns data to the webserver, which sends a HTTP response to the client.

The EWB Wissensplattform comes with 2 operation modes: Development and production. The structure of the 2 operation modes is shown in the two following pictures:
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP| Django_dev_webserver
    Django_dev_webserver --> Django
    Django --> Postgresql
```
The above picture shows a high-level overview of the development version of the EWB Wissensplattform. It consists of the python full-stack framework `django` and the open-source database management system (DBMS) `postgresql`. `Django` comes with a development webserver, which can be used locally to view changes made in development. 
```{note}
Please note, that the development version of the EWB Wissensplattform should not be used in production, since it is not considered secure. Use the production version instead.
```
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP| nginx
    nginx -->|uwsgi| uwsgi
    uwsgi ---> Django
    Django -->|SQL| Postgresql
```
The above figure shows an high-level overview of the production version of the EWB Wissensplattform. As a webserver `nginx` is used. It is used in the reverse-proxy mode. That means, that it forwards reuqests to the underlying application layer. Furthermore it deals with encryption, if HTTPS is used. It decrypts incomming HTTPS-requests, parses the HTTP-pakets and encodes the information in the uwsgi-protocol. These pakets are then send to the uwsgi-interpreter and from there to the django application.
Since a second web application is also part of the EWB Wissensplattform a complete high-level overview of the application is shown in the following figure:
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP| nginx
    nginx -->|uwsgi| uwsgi
    nginx -->|HTTP| cesiumJs
    cesiumJs -->|HTTP| DjangoCityGML
    nginx -->|HTTP| DjangoCityGML
    DjangoCityGML -->|SQL| 3dCityDB
    uwsgi --> Django
    Django -->|SQL| Postgresql
```
In the above diagram the components of the `cityGML visulizations` web application were included. The structure of the application is different from the EWB Wissensplattform. Here the application has a frontend and a backend part. CesiumJs acts as a frontend while a django instance acts as a backend. The cesium frontend can make API-calls to request data, while the API can also called directly. Behind the `djangoCityGML`-backend the 3DCityDB-database is connected.
