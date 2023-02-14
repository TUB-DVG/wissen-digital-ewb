FROM python:3.10 AS base

ENV PYTHONUNBUFFERED 1

# RUN useradd --create-home appuser
# # add a env variable user, because some apps read this variable
# ENV USER="appuser"
# USER appuser

WORKDIR /src
# make sure the ssrc directory is owned by the appuser
# RUN chown appuser:appuser -R /src

COPY 01_application/requirements.txt .
# RUN pip install -r requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    adduser --disabled-password --no-create-home appuser && \
    mkdir -p /vol/webcentral/static && \
    mkdir -p /vol/webcentral/media && \
    chown -R appuser:appuser /vol && \
    chmod -R 755 /vol

# make scripts and venv executables accessible, through path
ENV PATH="/scripts:/py/bin:$PATH"

# second build stage for production

FROM base AS prod
USER appuser
COPY --chown=appuser . /src
#chmod -R +x /scripts
CMD ["run.sh"]
