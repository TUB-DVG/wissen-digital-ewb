class Locator(object):
    
    # locators on main-page:
    linkToImpressum = "//a[@id='impressumLink']"
    inputSearchField = "//*[@id='search-input-general']"
    resultElements = "//tr"
    firstColumnToRow = "//td"
    linkToBuisnessApp = "//a[contains(text(), 'Geschäfts­modell­anwendungen')]"

    # locators of NavBar:
    toolListLink = "//a[@href='/tool_list/']"
    LogoImage = "//a/img[@alt='logo']"
    navStartButton = "//li/a[contains(text(), 'Start')]"
    navTechFocus = "//*[@id='technicalDropdown']/img"
    digitalApps = "//li/a[contains(text(), 'Digitale Anwendungen')]"
    weatherDataItem = "//li/a[contains(text(), 'Wetterdaten')]"
    lastProfileItem = "//li/a[contains(text(), 'Lastprofile')]"

    # locators in tool-list
    toolListSearchInput = "//input[@id='search-input-tools']"
    toolItemsIdentifer = "//div[@class='col-sm-6 col-lg-4 col-xl-3 card_hover']"
    searchStrBoxX = "//a[@href='/tool_list/?searched=&u=&l=&lcp=']"
    searchCategorieSelect = "//select[@id='kategorie-input-tools']"
    searchLicenceSelect = "//select[@id='lizenz-input-tools']"
    searchLifecycleSelect = "//select[@id='lzp-input-tools']"
    searchMagniferButton = "//button[@id='search-submit-tools']"
    activeSearchFilter = "//li[@class='list-inline-item']"
    searchResetButton = "//h6[contains(text(), 'Alle')]"
    showMoreLink = "//a[@href='#collapseInfoTools']"
    listInExpandedText = "//li[@class='lead']"
    showLessLink = "//a[@href='#collapseInfoTools']"
    cookieButton = "//button[@class='cookie-btn']"
    
    # locators in Business Apps:
    businessCardLocator = "//div[@class='card-body pb-0']"
    businessSearchField = "//input[@id='search-input-tools']"
    businessDetailsFurtherInfo = "//a[@id='furtherInfoLink']" 
    businessDetailsTags = "//ul[@id='tagsUlElement']/li"

    # locators in loginPage
    loginButtonElement = "//input[@class='btn login_btn']"

    # locators of lastprofile:
    stromlastApprLink = "//a[@href='/LastProfile/stromlast']"
    heatApproximationLink = "//a[@href='/LastProfile/warmelast']"
    weatherServiceLink = "//a[contains(text(), 'Wetterdienst')]"
    linkToStandardLoadProdile = "//a[contains(text(), 'Standard-Lastprofile beim BDEW')]"

    # locators inside stromlast-app
    selectPlaceholderCurrentApp = "/html/body/div/div/div[1]/div/div/div/div[1]"
    iframePlotlyApp = "/html/body/div[1]/iframe"
    radioButtonElements = "//input[@type='radio']"
    inputPowerRequriement = "//input[@id='powerRequirement']"
    pathToOpenedSelect = "/html/body/div/div/div[1]/div"
    pathToLineElementInPlotly = '//*[name() = "path"][@class="js-line"]'
    buttonCSVDownload = "//button[@id='btnDownloadCsv']"

    # locators for CurrentLoadApproximation-Page
    selectTypeOfAppr = "//div[@class='Select-value']"
    headingOfCurrentLoadApproxSite = "//h1"
    currentLoadIFrame = "//iframe"

    # locators for  HeatApproximation-Page
    headingOfHeatApproxSite = "//h1"

    # locators of about page:
    aboutPageTopHeading = "//h2"
    aboutPageSubHeading = "//h3"
    aboutPageEWBImage = "//img[@id='ewbImage']"
    aboutPageEinsteinCenterLink = "//a[@href='https://ewb.innoecos.com/Group/Einstein.Center.Digital.Future']"
    aboutPageUDKLink = "//a[@href='https://ewb.innoecos.com/Group/Berlin.Career.College.Zentralinstitut.fuer.Weiterbildung.ZIW']"
    aboutPageLinkToIOeW = "//a[@href='https://ewb.innoecos.com/Group/IOeW/']"
    aboutPageImgOfEinsteinCenter = "//img[@src='/static/img/ECDF.png']"
    aboutPageImgOfTUBerlin = "/html/body/section[2]/div/div[2]/div/a[2]/img"
    aboutPageImgOfUDK ="//img[@id='udkImage']"
    aboutPageImgOfIOEW = "//img[@id='ioewImage']"

    # Admin Page locators
    adminPageUsernameInput = "//input[@id='id_username']"
    adminPagePasswordInput = "//input[@type='password']"
    adminPageSubmit = "//input[@type='submit']"
