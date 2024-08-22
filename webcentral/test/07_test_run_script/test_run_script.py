"""This module holds testcases for the `run`-script, which is the entrypoint to 
the dockerized application.

"""

from unittest import TestCase, main
from subprocess import run, PIPE, CalledProcessError
from os import system, listdir 

class TestRunScript(TestCase):
    """Class to wrap the testcases as methods.

    """

    def testPreEnargus(self):
        """test if the pre_enargus command can be called from the
        command-line. It should expect 2 arguments.

        """
        result = run(["./run pre_enargus"], stdout=PIPE, stderr=PIPE, text=True, shell=True)
        
        # if calling the command without any arguments it should exit with a error message:
        self.assertEqual(result.stdout, "pre_enargus: Execute the preprocessing step to convert xml-enargus data to csv-data\\n./run pre_enargus <source-xml-file> <target-csv-file>\n")

        # recall the command and give the rght number of args:
        # result = subprocess.run(["./run pre_enargus "], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)


    
    def testBuildDockerCompose(self):
        """test if the docker-compose build from dev and prod works without errors.

        """
        try:
            result = run(['./run', 'build', "dev"], check=True, stdout=PIPE, stderr=PIPE, text=True)
        except CalledProcessError as e:
            self.fail(e.stderr)

    # def testRunUpDev(self):
    #     """test if the command `./run up dev` starts the development environment of the 
    #     application without errors.
    #     """
    #     try:
    #         result = run(['./run', 'up', "dev"], check=True, stdout=PIPE, stderr=PIPE, text=True)
    #     except CalledProcessError as e:
    #         self.fail(e.stderr)
    #
    def testStartSystemTest(self):
        """Test if the selenium system test can be started by the run-script. 

        """
        result = run(["./run", "test"], check=True, stdout=PIPE, stderr=PIPE, text=True)
        self.assertEqual(result.stdout, 'test-command usage: ./run test <type> <opt1> <opt2>\\ntype: Selenium\nopt1: Optional parameter specifing which Testclass to execute\nopt2: Optional parameter specifing the testmethod to execute\n')
        
        # test should also work, if not testingVenv is present:
        # check if testingVenv is present:
        if "testing_venv" in listdir("webcentral/test/"):
            system("rm -rf webcentral/test/testing_venv")
        try:
            result = run(["./run", "test", "Selenium"], check=True, stdout=PIPE, stderr=PIPE, text=True)
        except CalledProcessError as e:
            self.fail(e.stderr)
        

        



if __name__ == "__main__":
    main()
