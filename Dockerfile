FROM python:3.10 AS base
MAINTAINER "DVG"

# ensures, that all python logs are directly 
# send to STDOUT or STDERR and arnt kept in
# buffer.
ENV PYTHONUNBUFFERED 1

# creates a directory src and cd's into it
WORKDIR /src

COPY 01_application/requirements.txt .
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
# create a venv, upgrade pip, install packages, ...
# RUN python -m venv /py && \
#     /py/bin/pip install --upgrade pip && \
#     /py/bin/pip install -r requirements.txt && \
#     adduser --disabled-password --no-create-home appuser && \
#     mkdir -p /vol/webcentral/static && \
#     mkdir -p /vol/webcentral/media && \
#     chown -R appuser:appuser /vol && \
#     chmod -R 755 /vol

# make scripts and venv executables accessible, through path
#ENV PATH="/scripts:/py/bin:$PATH"


# second build stage for production

FROM base AS prod

# change user to non-root appuser
#USER appuser

# activate venv
#ENV PATH="/scripts:/py/bin:$PATH"

# copy the source code into /src and 
# change the ownership to the non-root
# user
#COPY --chown=appuser . /src
COPY . /src

# execute scripts/run.sh, which 
# executes collectstatic and migrate
#CMD ["sh", "run.sh"]
