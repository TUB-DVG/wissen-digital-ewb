FROM python:3.10 AS base

WORKDIR /src
COPY 01_application/requirements.txt .
RUN pip install -r requirements.txt

FROM base AS prod
COPY . /src
