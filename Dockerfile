FROM python:3.10 AS base

# ensures, that all python logs are directly 
# send to STDOUT or STDERR and are not kept in
# buffer.
ENV PYTHONUNBUFFERED 1

# creates a directory src and cd's into it
WORKDIR /src

COPY 01_application/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# second build stage for production
FROM base AS prod

COPY . /src

# build the sphinx-docs
# RUN sphinx-apidoc -f -o 02_work_doc/06_sphinx/source/ 01_application/webcentral_app/ \
#     && sphinx-build 02_work_doc/06_sphinx/source 01_application/webcentral_app/webcentral_app/static/

