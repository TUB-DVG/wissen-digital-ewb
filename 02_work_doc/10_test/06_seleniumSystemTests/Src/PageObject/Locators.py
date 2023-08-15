class Locator(object):
    
    # locators on main-page:
    linkToImpressum = "//a[@id='impressumLink']"
    inputSearchField = "//*[@id='search-input-general']"
    resultElements = "//tr"
    firstColumnToRow = "//td"

    # locators of NavBar:
    toolListLink = "//a[@href='/tool_list/']"
    LogoImage = "//a/img[@alt='logo']"
    navStartButton = "//li/a[contains(text(), 'Start')]"
    navTechFocus = "//*[@id='technicalDropdown']/img"
    digitalApps = "//li/a[contains(text(), 'Digitale Anwendungen')]"
    weatherDataItem = "//li/a[contains(text(), 'Wetterdaten')]"
    lastProfileItem = "//li/a[contains(text(), 'Lastprofile')]"
    # locators in Home

    # locators in tool-list
    toolListSearchInput = "//input[@id='search-input-tools']"
    toolItemsIdentifer = "//div[@class='col-sm-6 col-lg-4 col-xl-3 card_hover']"
    searchStrBoxX = "//a[@href='/tool_list/?searched=&k=&l=&lzp=']"
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
    
    # locators in loginPage
    loginButtonElement = "//input[@class='btn login_btn']"

    # locators of lastprofile:
    stromlastApprLink = "//a[@href='/LastProfile/stromlast']"
    heatApproximationLink = "//a[@href='/LastProfile/warmelast']"
    weatherServiceLink = "//a[contains(text(), 'Wetterdienst')]"
    linkToStandardLoadProdile = "//a[contains(text(), 'Standard-Lastprofile beim BDEW')]"

    # locators for CurrentLoadApproximation-Page
    selectTypeOfAppr = "//div[@class='Select-value']"
    headingOfCurrentLoadApproxSite = "//h1"
    currentLoadIFrame = "//iframe"

    # locators for  HeatApproximation-Page
    headingOfHeatApproxSite = "//h1"

    # locators of about page:
    aboutPageTopHeading = "//h2"
    aboutPageSubHeading = "//h3"
    aboutPageEWBImage = "//img[@src='/static/static/img/Energiewendebauen.png']"
    aboutPageEinsteinCenterLink = "//a[@href='https://ewb.innoecos.com/Group/Einstein.Center.Digital.Future']"
    aboutPageUDKLink = "//a[@href='https://ewb.innoecos.com/Group/Berlin.Career.College.Zentralinstitut.fuer.Weiterbildung.ZIW']"
    aboutPageLinkToIOeW = "//a[@href='https://ewb.innoecos.com/Group/IOeW/']"
    aboutPageImgOfEinsteinCenter = "//img[@src='/static/static/img/ECDF.png']"
    aboutPageImgOfTUBerlin = "/html/body/section[2]/div/div[2]/div/a[2]/img"
    aboutPageImgOfUDK ="//img[@src='/static/static/img/UdK.png']"
    aboutPageImgOfIOEW = "//img[@src='/static/static/img/ioew.png']"

    # Admin Page locators
    adminPageUsernameInput = "//input[@id='id_username']"
    adminPagePasswordInput = "//input[@type='password']"
    adminPageSubmit = "//input[@type='submit']"
