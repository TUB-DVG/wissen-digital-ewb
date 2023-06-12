from Src.TestBase.WebDriverSetup import WebDriverSetup

from Src.PageObject.Pages.loginPage import LoginPage

class TestWebcentral(WebDriverSetup):
    """Acts as a parent of all Test-classes
    
    In this class, methods, which are needed in all test-classes
    are put. All testclasses inherit from 'TestWebcentral'
    """

    def login(self):
        """performs a login on startup of the webdriver

        This method opens a instance of the webdriver and performs 
        login to the webcentral-page, so that the login page does 
        not interrupt the tests later on.
        """
        self.driver.get("http://127.0.0.1:8070/login")
        if self.driver.title == "Login":
            loginPage = LoginPage(self.driver)
            loginPage.getLoginButton().click()