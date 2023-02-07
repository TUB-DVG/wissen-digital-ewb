FROM python:3.10 AS base

RUN useradd --create-home appuser
# add a env variable user, because some apps read this variable
ENV USER="appuser"
USER appuser

WORKDIR /src
# make sure the ssrc directory is owned by the appuser
RUN chown appuser:appuser -R /src

COPY 01_application/requirements.txt .
RUN pip install -r requirements.txt

# second build stage for production

FROM base AS prod
USER appuser
COPY --chown=appuser . /src
