source .env
docker container exec database pg_dump -U $POSTGRES_USER $POSTGRES_DB > dump.sql
