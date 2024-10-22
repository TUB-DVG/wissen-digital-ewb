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

## Docker container structure
After showing the structure of the EWB Wissensplattform on a high abstraction level, a more fine granual description is given.
Mostly all components of the described structure in the last section are not installed nativly but are placed inside a container. This allows to ship the components together with its dependencies, making it easy to deploy the application and allowing to developer across mutliple operating systems.
```{mermaid}
flowchart TD
    Client[Client]

    subgraph Nginx_Container [Docker: Django Container]
        django_webserver[django_webserver]
        django
    end
    
    subgraph Postgresql_Container [Docker: Postgresql Container]
        Postgresql[Postgresql]
    end


    Client -->|HTTP| django_webserver
    django_webserver --> django
    django -->|SQL| Postgresql
```
The above figure shows the container structure of the development mode of the application.

## Docker container and volumes structure
When working with docker containers, a few additional information need to be considered: Docker containers are stateless by design. That means that all data and files, which were saved in the container filesystem are gone after a container restart. That makes it easy to restore a container to a known state but it also introduces the need for a additional mechanism to store persistent data. For that purpose `docker volumes` are used. Here persistent data is stored across container restarts.
```{mermaid}
flowchart TD
    Client[Client]

    subgraph Django_Container [Docker: Django Container]
        django_webserver[django_webserver]
        django[Django Application]
    end
    
    subgraph Postgresql_Container [Docker: Postgresql Container]
        Postgresql[Postgresql]
    end

    subgraph Data_Volume [Docker Volume: Postgresql Data Volume]
        pg_data[(Data Volume)]
    end

    %% Connections
    Client -->|HTTP| django_webserver
    django_webserver --> django
    django -->|SQL| Postgresql
    Postgresql -->|Writes to| pg_data
```
In the development environment the volume `pg_data` is used to store the database.
