# Nginx in production environment
In the production environement of the app a docker container is added, which holds an instances of the nginx webserver. It is used as a reverse-proxy,
getting requests over HTTPS and redirecting the plain HTTP request internally to the addressed service.
Because of security considerations the image `nginxinc/nginx-unprivileged` is used as a base image for the nginx docker container, which is called `proxy` in the
`docker-compose.prod.yml`-file. This file makes it possible to run nginx as a non-priviliged user `nginx`.
When specifying a custom `nginx.conf` the location of the pid-file has to be set to
```
    pid        /tmp/nginx.pid;
```
Furthermore the default listing port of the image has changed to port `8080`. That means, that a port mapping is needed in the 
compose file of the form
```
    ports:
      - 443:8080
```

