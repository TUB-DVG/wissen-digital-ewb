class Locator(object):
    
    # locators of NavBar:
    toolListLink = "//a[@href='/tool_list/']"
    TUBerlinImage = "//a/img[@alt='logo']"
    navStartButton = "//li/a[contains(text(), 'Start')]"
    navData = "//a[contains(text(), 'Daten')]"
    digitalApps = "//li/a[contains(text(), 'Digitale Anwendungen')]"
    weatherDataItem = "//li/a[contains(text(), 'Wetterdaten')]"
    lastProfileItem = "//li/a[contains(text(), 'Lastprofile')]"
    # locators in Home

    
    # locators in tool-list
    toolListSearchInput = "//input[@id='search-input-tools']"
    toolItemsIdentifer = "//div[@class='col-sm-6 col-lg-4 col-xl-3']"
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

    # locators for stromlastapproximation
    selectTypeOfAppr = "//div[@class='Select-value']"

