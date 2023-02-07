FROM python:3.10 AS base

RUN useradd --create-home appuser
USER appuser

WORKDIR /src
COPY 01_application/requirements.txt .
RUN pip install -r requirements.txt

FROM base AS prod

USER appuser

COPY --chown=appuser . /src
