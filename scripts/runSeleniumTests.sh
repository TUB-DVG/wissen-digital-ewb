
set -a
. ./.env
set +a
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --volumes
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build --detach
sleep 5
bash postgres/restoreDB.sh > log

cd 02_work_doc/10_test/06_seleniumSystemTests/
. ../testingVenv/bin/activate
siteUnderTest=http://127.0.0.1:8070 HEADLESS=1 python Test/TestSuite/TestRunner.py
deactivate
cd ../../../
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down