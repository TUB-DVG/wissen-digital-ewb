docker-compose up &
sleep 5
docker-compose exec webcentralcontainer python3 01_application/webcentral_app/manage.py makemigrations
sleep 2
docker-compose exec webcentralcontainer python3 01_application/webcentral_app/manage.py migrate
sleep 1
docker-compose exec webcentralcontainer python3 01_application/webcentral_app/manage.py createsuperuser --no-input
