class Locator(object):
    
    # locators on start-page:
    linkToImpressum = "//a[@id='impressumLink']"
    inputSearchField = "//*[@id='search-input-general']"
    resultElements = "//tr"
    firstColumnToRow = "//td"
    linkToBuisnessApp = "//a[contains(text(), 'Geschäfts­modell­anwendungen')]"
    linkToTechnicalStandarts = "//a[@id='linkToTechnicalStandarts']"
    paginationNextLink = "//a[@id='paginationNextLink']"
    paginationPreviousLink = "//a[@id='paginationPreviousLink']"
    paginationFirstLink = "//a[@id='paginationFirstSite']"
    paginationLastLink = "//a[@id='paginationLastSite']"
    paginationCurrentSite = "//span[@class='current']"
    linkToTechnicalPublications = "//a[@id='linkToTechnicalPublications']"
    linkToOperationalPublications = "//a[@id='linkToOperationalPublications']"
    linkToLegalPublications = "//a[@id='linkToLegalPublications']"
    linkToEcologicalPublications = "//a[@id='linkToEcologicalPublications']"
    linkToNegativeEnviormentalImpact = "/pages/environmentalIntegrityNegativ"

    # locators for all search-pages:
    cardLocator = "//div[@class='card-body pb-0']"
    xFromSearchFilter = "//i[@class='bi bi-x fa-lg close-icon']"
    usageDropdownElement = "//select[@id='kategorie-input-tools']/option"
    accessabilityDropdownElement = "//select[@id='lizenz-input-tools']/option"
    lifeCyclePhaseDropdownElement = "//select[@id='lzp-input-tools']/option"
    searchSubmitButton = "//button[@id='search-submit-tools']"
    usageOnDetailPage = "//li[@class='list-inline-item h6 mb-0']"
    accessabilityParagraphTag = "//h5[contains(text(), 'Zugänglichkeit')]/p"
    

    # locators on TechnicalStandards:
    linkToNormsOnTS = "//a[@id='linkToNorms']"
    linkToProtocolsOnTS = "//a[@id='linkToProtocols']"
    
    # locators on NormsPage:
    searchInputNorms = "//input[@id='search-input-norms']"

    # locators on ProtocolsPage:
    searchInputProtocols = "//input[@id='search-input-protocols']"

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
    #paginationNextLink = "//a[@id='paginationNextLink']"
    #paginationNextLink = "//a[@id='paginationNextLink']"
    #paginationPreviousLink = "//a[@id='paginationPreviousLink']"
    #paginationFirstLink = "//a[@id='paginationFirstLink']"
    #paginationLastLink = "//a[@id='paginationLastLink']"

    # locators in Business Apps:
    businessSearchField = "//input[@id='search-input-tools']"
    businessDetailsFurtherInfo = "//a[@id='furtherInfoLink']" 
    businessDetailsTags = "//ul[@id='tagsUlElement']/li"

    # locators in loginPage
    loginButtonElement = "//input[@class='btn login_btn']"

    # locators of lastprofile:
    stromlastApprLink = "//a[@href='/LastProfile/stromlast']"
    heatApproximationLink = "/LastProfile/warmelast"
    weatherServiceLink = "//a[contains(text(), 'Wetterdienst')]"
    linkToStandardLoadProdile = "//a[contains(text(), 'Standard-Lastprofile beim BDEW')]"

    # locators inside stromlast-app
    selectPlaceholderCurrentApp = "//div[@class='Select-placeholder']"
    iframePlotlyApp = "//iframe"
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
    bottomParagraph = "//p[@id='containerParagraphAtBottom']"

    # locators of about page:
    aboutPageTopHeading = "//h2"
    aboutPageSubHeading = "//h3"
    aboutPageEWBImage = "//img[@id='ewbImage']"
    aboutPageEinsteinCenterLink = "//a[@href='https://ewb.innoecos.com/Group/Einstein.Center.Digital.Future']"
    aboutPageUDKLink = "//a[@href='https://ewb.innoecos.com/Group/Berlin.Career.College.Zentralinstitut.fuer.Weiterbildung.ZIW']"
    aboutPageLinkToIOeW = "//a[@href='https://ewb.innoecos.com/Group/IOeW/']"
    aboutPageImgOfEinsteinCenter = "//img[@id='ecdfImage']"
    aboutPageImgOfTUBerlin = "/html/body/section[2]/div/div[2]/div/a[2]/img"
    aboutPageImgOfUDK ="//img[@id='udkImage']"
    aboutPageImgOfIOEW = "//img[@id='ioewImage']"

    # Admin Page locators
    adminPageUsernameInput = "//input[@id='id_username']"
    adminPagePasswordInput = "//input[@type='password']"
    adminPageSubmit = "//input[@type='submit']"

    # publicationPage locators
    publicationContainer = "//div[@id='publicationsContainer']"
    publicationSearchBoxForm = "//form[@id='searchBox']"
    publicationSearchBoxInput = "//input[@id='search-input-publication']"
    publicationSearchBoxSelect = "//select[@id='name-input-publication']"
    publicationSearchBoxSubmit = "//button[@id='search-submit-publication']"
    publicationSearchBoxReset = "//h6[@id='allButton']"
    publicationCloseButton = "//a/i"
    paginatorObjects = "card"
    paginatorObjectTitle = ".//h3"
    paginatorObjectAuthorsAndType = ".//p"

    publicationDetailsPageTitle = "//h2"
    publicationDetailsPageAuthorsHeading = "//h5[contains(text(), 'Autoren')]"
    publicationDetailsPageAuthorsValues = "following-sibling::p"

    publicationDetailsPageType = "list-inline-item"

    # CriteriaCatalog locators
    criteriaCatalogOverviewCard1 = "//div[@title='Planung, Betrieb und Betriebsoptimierung']"
    criteriaCatalogOverviewCard2 = "//div[@title='Planung, Betrieb und Betriebsoptimierung']"
    criteriaCatalogDetailsContentContainer = "//div[@id='hi']"
    allHorizontalLineElements = "//hr"
    fullTextSearchField = "//input[@id='searchInputCriteriaCatalog']"
    collpaseEveryThingButton = "//button[@id='collapseEverythingButton']"

    # locators for negative-environmental-impacts
    contentDiv = "//div[contains(@class, 'content')]"
    descriptionHeadingDiv = "//div[@class='description-heading']"
    descriptionContentDiv = "//div[@class='description-content']"
    boxesDiv = "//div[@class='boxes']"
    box1 = "//div[@id='box1']"
    box2 = "//div[@id='box2']"
    boxHeading = "//h6[@class='boxHeading']"
    boxDescription = "//p[@class='boxDescription']"
    boxImage = "//div[@class='boxImage']"
    imageInDiv = "//img"
    linkToComponentsListPage = "/component_list/components"
    linkToDataProcessingPage = "/component_list/dataProcessing"

    # locators for components_list
    secondaryNavBar = "secondaryNavbar"
    descriptionBox  = "descriptionBox"
    descriptionHeading = "descriptionHeading"
    descriptionText = "descriptionText"
    descriptionDownloadLink = "descriptionDownloadLink"
    descriptionImage = "descriptionImage"

    # locators for Footer
    languageSelectionField = "//select[@name='language']"