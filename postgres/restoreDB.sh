
source .env
cat postgres/${DATABASE_PLAIN_SQL_FILE} | docker exec -i database psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
