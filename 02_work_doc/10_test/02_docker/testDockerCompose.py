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


    def _loginAsSuperUser(self):
        """This protected method is used internally to login as superuser in the different testcases.

        """

        self.browser.get(self.localAdress + "/admin")

        time.sleep(1)

        usernameField = self.browser.find_element("xpath", '//input[@name="username"]')
        usernameField.send_keys(os.environ.get("DJANGO_SUPERUSER_USERNAME"))

        passwordField = self.browser.find_element("xpath", '//input[@name="password"]')
        passwordField.send_keys(os.environ.get("DJANGO_SUPERUSER_PASSWORD"))

        submitButton = self.browser.find_element("xpath", '//input[@type="submit"]')
        submitButton.click()

        time.sleep(1)

    def testIfSuperuserIsPresent(self):
        """This Testcase checks if it is possible to login with the superuser-credentials
        from the .env-file.

        """

        #pdb.set_trace()

        self.assertTrue("Wissensplattform" in self.browser.title)

        print("Trying to log-in with superuser-credentials from .env-file...")
        
        self._loginAsSuperUser()

        self.assertFalse(
            self.browser.title == "Log in | Django site admin", 
            "Couldnt log-in as superuser. Check if automated superuser creation was successful.",
        )

        #self.browser.get(self.localAdress)

    def testDatabaseDumpIsLoaded(self):
        """This Testcase checks, if the database is filled, by going to the "Digitale Werkzeuge"-site 
        and checking if the list is empty.

        """
        print("Checking, if Digitale Werkzeuge is populated...")
        self._loginAsSuperUser()

        self.browser.get(self.localAdress)

        linkToToolList = self.browser.find_element("xpath", '//a[@href="/tool_list/"]')
        linkToToolList.click()

        time.sleep(1)

        listOfCards = self.browser.find_elements("xpath", '//div[@class="card-body pb-0"]')
        self.assertNotEqual(len(listOfCards), 0, "Es sind keine Elemente in der Liste der digitalen Werkzeuge!")
    
    def testImagesInToolList(self):
        """This TestCase tests if the images of the Tools are present on the Tab Digitale Werkzeuge.
        It does this by loading the src of the image. If the returned page has 'Page not found' in title,
        the image is not present, and an assertation error is thrown. This test is done for 5 images.

        """
        print("Checking if images are present in the Tool List...")
        self._loginAsSuperUser()

        self.browser.get(self.localAdress)

        linkToToolList = self.browser.find_element("xpath", '//a[@href="/tool_list/"]')
        linkToToolList.click()

        time.sleep(1)

        

        # check 5 cards:
        for numberOfCheckedImages in range(5):
            listOfCardImg = self.browser.find_elements("xpath", '//img[@alt="tool image (if=db)"]')
            urlToImage = listOfCardImg[numberOfCheckedImages].get_attribute("src")
            self.browser.get(urlToImage)
            self.assertFalse("Page not found" in self.browser.title, "Image not found!")

            self.browser.get("http://127.0.0.1:8070/tool_list/")




if __name__ == "__main__":
    main()
