FROM python:3.10 AS base

# ensures, that all python logs are directly 
# send to STDOUT or STDERR and are not kept in
# buffer.
ENV PYTHONUNBUFFERED 1
ARG WEBCENTRAL_UNPRIVILEGED_USER

# creates a directory src and cd's into it
RUN apt update && apt upgrade --yes
RUN apt-get install -y locales locales-all

ENV LANG de_DE.UTF-8  
ENV LANGUAGE de_DE:de  
ENV LC_ALL de_DE.UTF-8  

# second build stage for production
FROM base AS prod
RUN adduser --home /home/${WEBCENTRAL_UNPRIVILEGED_USER} ${WEBCENTRAL_UNPRIVILEGED_USER} -u 1000
COPY 01_application/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
RUN chown -R ${WEBCENTRAL_UNPRIVILEGED_USER} /usr/local/lib/python3.10/site-packages/

USER ${WEBCENTRAL_UNPRIVILEGED_USER}
WORKDIR /home/${WEBCENTRAL_UNPRIVILEGED_USER}

COPY --chown=${WEBCENTRAL_UNPRIVILEGED_USER} . /home/${WEBCENTRAL_UNPRIVILEGED_USER} 

# second build stage for dev environment
FROM base AS dev

RUN apt-get install -y gettext
WORKDIR /webcentral/
COPY 01_application/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
