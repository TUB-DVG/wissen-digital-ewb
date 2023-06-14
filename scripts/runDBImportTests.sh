#!/bin/bash
# Please execute the script as sudo, otherwise the .yaml-files wont be deleted!
# echo "Build Dev-Environment..."
# docker-compose -f docker-compose.yml -f docker-compose.dev.yml 

echo "Start Test of docker-dev environment..."
echo "Deleting current Volumes..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes

# start docker-env:
echo "Start Docker Dev-Environemnt..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d &
sleep 5

echo "Restore the Database State to the Dump-State, which lies in postgres/ ..."
bash postgres/restoreDB.sh > log
sleep 2

echo "Executing Tests..."
docker exec -w /src/01_application/webcentral_app/ webcentral python3 manage.py test testDatabaseFilling.checkDifferencesInDatabase

echo "Delete the created yaml- and yml-files..."
sudo rm -f 01_application/webcentral_app/testFiles/*.yaml
sudo rm -f 01_application/webcentral_app/testFiles/*.yml
sleep 1

echo "Delete the Docker Volumes..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes

# echo "Build Prod-Environment..."
# docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

echo "Start Docker-Compose Production Environment..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d &
sleep 10

echo "Restore Database state of Production-Environment..."
bash postgres/restoreDB.sh > log
sleep 2

echo "Execute Tests in Production Environment..."
docker container exec -w /src/01_application/webcentral_app/ webcentral python3 manage.py test testDatabaseFilling.checkDifferencesInDatabase

echo "Delete .yaml- and .yml-files in webcentral-container..."
docker container exec webcentral rm -f /src/01_application/webcentral_app/testFiles*.yaml
docker container exec webcentral rm -f /src/01_application/webcentral_app/testFiles*.yml

docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --volumes 