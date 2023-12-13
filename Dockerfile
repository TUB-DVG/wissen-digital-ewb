FROM python:3.10 AS base

# ensures, that all python logs are directly 
# send to STDOUT or STDERR and are not kept in
# buffer.
ENV PYTHONUNBUFFERED 1

# creates a directory src and cd's into it
RUN apt update && apt upgrade --yes
RUN apt-get install -y locales locales-all

RUN adduser --home /home/uwsgiguest uwsgiguest -u 1000

COPY 01_application/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
# RUN chmod o+rwx /home/uwsgiguest/.cache
USER uwsgiguest
WORKDIR /home/uwsgiguest
#RUN apt update && apt upgrade --yes && apt install locale-gen && locale-gen de_DE.UTF-8 
# RUN locale-gen de_DE.UTF-8  
ENV LANG de_DE.UTF-8  
ENV LANGUAGE de_DE:de  
ENV LC_ALL de_DE.UTF-8  

# second build stage for production
FROM base AS prod
# 
COPY --chown=uwsgiguest . /src

WORKDIR /home/uwsgiguest
COPY . /home/uwsgiguest --chown=uwsgiguest
