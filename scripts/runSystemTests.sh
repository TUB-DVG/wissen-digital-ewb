

set -a
. ./.env
set +a

. 02_work_doc/10_test/testingVenv/bin/activate

python3 02_work_doc/10_test/02_docker/testDockerCompose.py
deactivate

