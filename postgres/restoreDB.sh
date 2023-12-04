
source .env
# this command fills the database
cat postgres/${DATABASE_PLAIN_SQL_FILE} | docker exec -i database psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# load media image files into /vol/webcentral/media
docker container exec webcentral bash -c "cp -r /src/01_application/webcentral_app/media /vol/webcentral/"

#docker container exec webcentral python3 /src/01_application/webcentral_app/manage.py makemigrations

docker container exec webcentral python3 /src/01_application/webcentral_app/manage.py migrate

# docker container exec webcentral python3 /src/01_application/webcentral_app/manage.py createsuperuser --noinput