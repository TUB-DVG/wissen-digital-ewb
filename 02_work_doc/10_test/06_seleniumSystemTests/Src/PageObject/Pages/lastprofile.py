from selenium.webdriver.common.by import By

from Src.PageObject.Locators import Locator

class Lastprofile(object):
    """
    
    """
    def __init__(self, driver):
        """Constructor of the Lastprofile-Class
        
        """
        driver.implicitly_wait(2)
        self.driver = driver
        

    def getLinkToStromlastTool(self):
        """Returns the link to the Stromlast-Approximation tool.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.stromlastApprLink,
        )

    def getLinkForHeatApproxTool(self):
        """
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.heatApproximationLink,
        )

    def getWeatherServiceLink(self):
        """Returns the link to the weather-service github repo
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.weatherServiceLink,
        )

    def getLoadProfileLink(self):
        """Returns the link to the Link to the standard load profile.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.linkToStandardLoadProdile,
        )
    
    def getReactSelectPlaceholder(self):
        """Returns the select placeholder on the stromlast-page
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.selectPlaceholderCurrentApp,
        )

    def getPlotlyIFrame(self):
        """Return the iframe of the PLotly-Dash app

        It is needed to switch into the iframe to find the react-Webelments
        inside the browser page.
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.iframePlotlyApp,    
        )
    
    def getListOfRadioMonth(self):
        """Return a List of Radio-Button Webelements for the month.
        
        """
        return self.driver.find_elements(
            By.XPATH,
            Locator.radioButtonElements,
        )
    
    def getInputFieldPowerRequirement(self):
        """Return the Input Field, where the powerRequirement should be stated.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.inputPowerRequriement,
        )

    def getReactOptionFromText(self, reactSelect, elementText):
        """Return the option-webelement which has the elementText 
        
        """
        return reactSelect.find_element(By.XPATH, f"//*[contains(text(), '{elementText}')]")

    def getOpenedReactSelect(self):
        """Return the Webelement holding the options of the react-select.

        When the Select-Dropdown was clicked, the Options appear. This div-element holds 
        all options.
        
        """
        return self.driver.find_element(
            By.XPATH,
            Locator.pathToOpenedSelect,
        )       
    
    def getLineElementFromPlotly(self):
        """
        
        """
        breakpoint()
        return self.driver.find_element(
            By.XPATH,
            Locator.pathToLineElementInPlotly,
        )
    
    def getLinePloty(self):
        """
        
        """
        return self.driver.find_element(
            By.XPATH, 
            Locator.pathToLineElementInPlotly,
        )