# Structure of the EWB Wissensplattform
In the following section the structure of the application is described.
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP Request| Webserver
    Webserver -->|Route to| Application
    Application --> Database
```
The above figure shows a high-level overview of the EWB Wissensplattform. The client comunicates 
via HTTP-requests with a webserver. the webserver parses the request and redirects it to the application layer,
where the request is processed. That processing may include fetching data from the database layer. 
The application layer returns data to the webserver, which sends a HTTP response to the client.

The EWB Wissensplattform comes with 2 operation modes: Development and production. The structure of the 2 operation modes is shown in the two following pictures:
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP Request| Django_dev_webserver
    Django_dev_webserver -->|Route to| Django
    Django --> Postgresql
```
```{mermaid}
flowchart TD
    Client[Client] -->|HTTP Request| nginx
    nginx -->|Route to| uwsgi
    uwsgi ---> Django
    Django --> Postgresql
```

