
source .env
# this command fills the database
cat postgres/${DATABASE_PLAIN_SQL_FILE} | docker exec -i database psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# load media image files into /vol/webcentral/media
docker container exec webcentral bash -c "cp -r /src/01_application/webcentral_app/media /vol/webcentral/"
