set -a
. ./.env
set +a


python3 01_application/webcentral_app/tests/testDockerCompose.py
