#FROM nginx:stable

# pull the nginx-unprivileged image from docker-hub.
# this image runs nginx from an unprivileged user
FROM nginxinc/nginx-unprivileged




# copy configuration- and script files to the docker image
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

# we set default values for the environmental variables
# these env-vars are also set in the .env file
ENV LISTEN_PORT=8080
ENV APP_HOST=webcentral
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# optional
VOLUME /vol/static

# siwtch to non-root user
#USER nginx

# script starts nginx in the foreground of the container
CMD ["./run.sh"]
