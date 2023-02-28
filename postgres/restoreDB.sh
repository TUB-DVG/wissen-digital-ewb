
cd ..
source .env
cat postgres/db_webcentral_Backup_20220714.sql | docker exec -i database psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
