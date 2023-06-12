
set -a
. ./.env
set +a

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --force-recreate --detach

bash postgres/restoreDB.sh
clear
cd 02_work_doc/10_test/06_seleniumSystemTests/
. ../testingVenv/bin/activate
python Test/TestSuite/TestRunner.py
deactivate