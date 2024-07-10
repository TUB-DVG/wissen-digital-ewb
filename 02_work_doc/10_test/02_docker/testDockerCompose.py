"""Tests, if the Prod-Env and the Dev-Env start without errors.

This Module acts as a Unittest-Testcase to automatically test the
Docker-compose-startup of the Development- and the Production-
Environment. The Tests can be executed by creating a 
virtual environemnt from the `requirementsTesting.txt`. After 
activation, the tests can be started via:
```
    python3 testDockerCompose.py
```
If it outputs 'Ok', all tests passed.
"""
from os import system
import time
from unittest import (
    TestCase,
    main,
    )
from subprocess import (
    run,
    PIPE,
)
# import docker


class TestDockerComposeEnvironments(TestCase):
    """Test-Class for Testing if the Docker-Compose-project executes

    This Class inherits from `unittest.TestCase`. It runs the 
    Docker-compose Production-Env and the Docker-compose Development-
    Env and checks if any errors occur.
    """

    # def setUpClass() -> None:
    #     """Stops all running containers before test-execution.
    #
    #     This static-class-method is executed before the 
    #     instanciation of `TestDockerComposeEnvionemnts`. It ensures,
    #     that all running containers are stoped before the test
    #     execution starts.
    #
    #     Parameters
    #     ----------
    #
    #     Returns
    #     -------
    #     None
    #     """
    #
    #     os.system("docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --remove-orphans")
    #     os.system("docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --remove-orphans")
    #     dockerInstance = docker.DockerClient(
    #         base_url='unix://var/run/docker.sock',
    #     )
    #     for container in dockerInstance.containers.list():
    #         container.stop()
    #
    # def setUp(self):
    #     """setUp-method, which is called before every test.
    #
    #
    #     """
    #     self.dockerInstance = docker.DockerClient(
    #         base_url='unix://var/run/docker.sock',
    #     )
    #
    # def tearDown(self) -> None:
    #     """Closes the open Socket-connection to the docker-socket
    #
    #     This `tearDown`-method gets executed after every test. It
    #     closes the connection to the Docker-SOCKET. Otherwise an
    #     error is printed to the console.
    #
    #     Parameters
    #     ----------
    #
    #     Returns
    #     -------
    #     None
    #     """
    #     self.dockerInstance.close()
    #
    def testRunScriptDevBuild(self):
        """Test if the call of './run build dev' runs without errors
        """
        result = system("./run build dev")
        self.assertTrue(result == 0)

    # def testProd(self) -> None:
    #     """Tests if the production-environment can be run without errors.
    #
    #     This method automatically runs the docker-compose production
    #     envirionment and checks if all needed containers are running 
    #     and all needed volumes were created.
    #
    #     Parameters
    #     ----------
    #
    #     Returns
    #     -------
    #     None
    #     """
    #
    #     os.system(
    #         "docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d",
    #     )
    #
    #     print("Waiting 3 seconds, to start Docker-Compose-Project...")
    #     time.sleep(3)
    #
    #     self.assertEqual(
    #         len(self.dockerInstance.containers.list()),
    #         3,
    #         "Testing-Production-env: The number of running containers does not match 3!",
    #     )
    #
    #     dictToBeComparedWith = {
    #         "proxy": "running",
    #         "webcentral": "running",
    #         "database": "running",
    #     }
    #
    #     dictNameToStatus = {}
    #     for container in self.dockerInstance.containers.list():
    #         dictNameToStatus[container.name] = container.status
    #
    #     self.assertTrue(
    #         dictNameToStatus == dictToBeComparedWith,
    #         "Testing Production-env: Expected Name and Status of Containers doesnt match the expected values!",
    #     )
    #
    #     listOfVolumeNames = []
    #     for volume in self.dockerInstance.volumes.list():
    #         if "static-data" in volume.name or "pgdata" in volume.name:
    #             listOfVolumeNames.append(volume.name)
    #
    #     self.assertEqual(2,
    #                     len(listOfVolumeNames),
    #                     "Testing Production-env: Number of found volumes, with the name static-data and pgdata should be 2!",
    #     )
    #
    #     os.system("docker container stop proxy")
    #     os.system(
    #         "docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes",
    #     )
    #
    #
    #     time.sleep(1)
    #
    # def testDev(self) -> None:
    #     """Tests if the Development Environment can be run.
    #
    #     This method tests if the docker-compose development-
    #     environment rus without errors. Therefore it starts the envionment
    #     and checks if the number of running container is 2 and the number 
    #     of volumes with the name `pgdata` is one.
    #
    #     Parameters
    #     ----------
    #
    #     Returns
    #     -------
    #     None
    #     """
    #     os.system(
    #         "docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d",
    #     )
    #
    #     print("Waiting 3 seconds, to start Docker-Compose-Project...")
    #     time.sleep(3)
    #
    #     self.assertEqual(
    #         len(self.dockerInstance.containers.list()),
    #         2,
    #         "Testing-Development-env: The number of running containers does not match 2!",
    #     )
    #
    #     dictToBeComparedWith = {
    #         "webcentral": "running",
    #         "database": "running",
    #     }
    #
    #     dictNameToStatus = {}
    #     for container in self.dockerInstance.containers.list():
    #         dictNameToStatus[container.name] = container.status
    #
    #     self.assertTrue(
    #         dictNameToStatus == dictToBeComparedWith,
    #         "Testing Development-env: Expected Name and Status of Containers doesnt match the expected values!",
    #     )
    #
    #     listOfVolumeNames = []
    #     for volume in self.dockerInstance.volumes.list():
    #         if "pgdata" in volume.name:
    #             listOfVolumeNames.append(volume.name)
    #
    #     self.assertEqual(1,
    #                     len(listOfVolumeNames),
    #                     "Testing Development-env: Number of found volumes, with the name static-data and pgdata should be 1!",
    #     )
    #
    #     os.system(
    #         "docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes",
    #     )
    #     time.sleep(1)

if __name__ == "__main__":
    main()
