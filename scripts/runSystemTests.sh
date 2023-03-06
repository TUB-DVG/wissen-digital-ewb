
cd ..

set -a
. ./.env
set +a


python3 02_work_doc/10_test/02_docker/testDockerCompose.py
