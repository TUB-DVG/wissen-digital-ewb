"""This Module shows, how selenium can be used as a testting tool, to perform
system-/accpetance tests. These tests are from a customer/user perspective and
test the functionality of the system as a whole. The tests are often testing a
user-Story. This is a typical use of the system.
In this example, selenium is used together with the unittest-framework
"""
import os
import time
import pdb
from unittest import (
    TestCase,
    main,
    )

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from django.tests import TestCase


class TestLogin(TestCase):
    """This class tests the login of the webCentral Web app.

    """
    def setUp(self):
        """This method gets executed before every testcase. 
        It creates a new browser window and opens the webcentral app.

        """
        self.browser = webdriver.Firefox()
        self.localAdress = "http://127.0.0.1:" + os.environ.get("PORT_TO_OUTSIDE")
        self.browser.get(self.localAdress)

    def tearDown(self):
        self.browser.quit()

    def testIfSuperuserIsPresent(self):
        """

        """

        #pdb.set_trace()

        self.assertTrue("Wissensplattform" in self.browser.title)

        print("Trying to log-in with superuser-credentials from .env-file...")
        self.browser.get(self.localAdress + "/admin")
        
        time.sleep(1)
        
        usernameField = self.browser.find_element("xpath", '//input[@name="username"]')
        usernameField.send_keys(os.environ.get("DJANGO_SUPERUSER_USERNAME"))

        passwordField = self.browser.find_element("xpath", '//input[@name="password"]')
        passwordField.send_keys(os.environ.get("DJANGO_SUPERUSER_PASSWORD"))

        submitButton = self.browser.find_element("xpath", '//input[@type="submit"]')
        submitButton.click()

        time.sleep(1)
        #pdb.set_trace()

        self.assertFalse(
            self.browser.title == "Log in | Django site admin", 
            "Couldnt log-in as superuser. Check if automated superuser creation was successful.",
        )

        self.browser.get(self.localAdress)

        linkToToolList = self.browser.find_element("xpath", '//a[@href="/tool_list/"]')
        linkToToolList.click()

        time.sleep(1)

        listOfCards = self.browser.find_elements("xpath", '//div[@class="card-body pb-0"]')
        self.assertNotEqual(len(listOfCards), 0, "Es sind keine Elemente in der Liste der digitalen Werkzeuge!")

    # def testPopulateDB(self):
    #     """this testcase tests if an empty db can be populated 
    #     from outside the mult-container app using a shell-script.
    #     Therefore it checks, if the site 'Digitale Werkzeuge' is accessible.
    #     On an empty db instance the ptjuser is not present and the site cant be
    #     accessed. In this case, the database is populated.

    #     """

        #pdb.set_trace()


        # if "Login" in self.browser.title:
        #     os.system("bash postgres/restoreDB.sh")

        #     time.sleep(3)
        #     self.browser.find_element("xpath", '//input[@type="submit"]').click()

        #     time.sleep(1)
        #     pdb.set_trace()


if __name__ == "__main__":
    main()
