# Testing the Wissensplattform
In web-development it is a good practice to write tests, which can run automatically and ensure that a expected behaviour is met. 
In general testing can be made on different layers of the application and from different viewpoints. Here two tyes of tests are implemented: Unit tests and system tests. 

 - Unit tests test the functionality of the smallest portions of the code, so called units. These units should meet some expected functionality and are often written from a white-box perspective: That means that the testing person, who writes the test does know the programming code and how the unit works internally.
 - a system test checks the system from the outside (from the user-persepective) and assumes the system as a black-box. 

 For the system tests the selenium webdriver is used. It can be installed by creating a python virtual environment and installing the requirements into that environement. The following commands need to be executed in the terminal:
```
   cd 02_work_doc/06_seleniumSystemTest
```
Create the virtual environment:
```
    python -m venv testingVenv
```
Activate the virtual environement:
```
    source testingVenv/bin/activate
```
Install the requirements:
```
    pip install -r requirementsTesting.txt
```

Selenium makes it possible to remote control the web browser through python commands. In that way a user interaction with the site from the viewpoint of a regular user can be made automatically and the results checked against expected behaviour.
If firefox is used as a browser, additional software needs to be installed to make the remote controlling possible. That additional software is called `geckodriver` and can be downloaded from the Mozilla github page: https://github.com/mozilla/geckodriver/releases. Download the latest release and unzip it:
```
    tar -xzf geckodriver.tar
```
The unzipped geckodriver executable needs to be present in the path of your operating system. Under linux that can be done putting the executable the `/usr/bin` folder, in which on default is searched for executables.
```
    sudo mv geckodriver /usr/bin/
```
Note: Superuser priviliges are needed for that operation.
Now, the `run`-script can be used to execute the integration tests. To execute the script, change the directory to the root-project folder. The integration tests can then be executed by running the following command:
```shell
./run test Selenium
```
Note: Since the application is tested from the outside, it should already be running in a seperate terminal.

On default, the locally running web-application running on `http://127.0.0.1:8000` is tested. But it is also possible to test the remotly running web-application (e.g. on `https://wissen-digital-ewb.de`). To test against that target the environmental variable `siteUnderTest` needs to be changed. That can be done by providing the new value in the `.env`-file for `siteUnderTest`. 

If only the integration tests for one specfic site should be executed, that can be done by appending the name of the test-file to the test execution command. E.g. to only execute the test for the Tools site the command looks as follows:
```shell
./run test Selenium TestDigitalTools
```
Note: All test-files can be found under `/02_word_doc/06_seleniumSystemTest/Test/Scripts/`.

If only one specfic test-method should be executed, it can also be appended to the command. E.g. if only the method `testFilteringAndPagination()` from the file `TestDigitalTools.py` should be executed the command has the following form:
```shell
./run test Selenium TestDigitalTools testFilteringAndPagination 
```

