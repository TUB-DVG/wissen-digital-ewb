FROM nginxinc/nginx-unprivileged:1-alpine
# pull the nginx-unprivileged image from docker-hub.
# this image runs nginx from an unprivileged user

# copy configuration- and script files to the docker image
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

# we set default values for the environmental variables
# these env-vars are also set in the .env file
ENV LISTEN_PORT=8000
ENV APP_HOST=webcentral
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

# optional
VOLUME /vol/static

# switch back from root-user to unprivileged user
USER nginx

CMD ["./run.sh"]
