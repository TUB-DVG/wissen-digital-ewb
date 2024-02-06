#FROM nginx:stable

# pull the nginx-unprivileged image from docker-hub.
# this image runs nginx from an unprivileged user
FROM nginxinc/nginx-unprivileged




# copy configuration- and script files to the docker image
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./localDefault.conf.tpl /etc/nginx/localDefault.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params



# we set default values for the environmental variables
# these env-vars are also set in the .env file
ENV LISTEN_PORT=8080
ENV APP_HOST=webcentral
ENV APP_PORT=9000

USER root

COPY --chown=nginx:nginx ./conf/ /etc/nginx/ssl/

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf

# optional
VOLUME /vol/static

# siwtch to non-root user
USER nginx
