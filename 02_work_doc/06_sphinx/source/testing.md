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

Selenium makes it possible to remote control the web browser through python commands. In that way a user interaction with the site from the view of a regular user can be made automatically and the results checked agains expected behaviour.
If firefox is used as a browser, additional software needs to be installed to make the remote controlling possible. That additional software is called `geckodriver` and can be downloaded from the Mozilla github page: https://github.com/mozilla/geckodriver/releases. Download the latest release and unzip it:
```
    tar -xzf geckodriver.tar
```
The unzipped geckodriver executable needs to be present in the path of your operating system. Under linux that can be done putting the executable the `/usr/bin` folder, in which on default is searched for executables.
```
    sudo mv geckodriver /usr/bin/
```
Note: Superuser priviliges are needed for that operation.
