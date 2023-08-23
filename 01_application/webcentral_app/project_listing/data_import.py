import csv
from encodings import utf_8
from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from keywords.models import *
#from norms_over.models import *
from TechnicalStandards.models import *
# -*- coding: utf-8 -*-

def getOrCreateFurtherFundingInformation(row, header):
    """
    add entry into table FurtherFundingInformation or/and return entry key
    """
    # content = row[number of the columns of the row]
    fundedBy = row[header.index('Bundesministerium')]
    projectManagementAgency = row[header.index('Projekttraeger')]
    researchProgram = row[header.index('Foerderprogramm')]
    fundingProgram = row[header.index('Forschungsprogramm')]
    obj, created = FurtherFundingInformation.objects.get_or_create(
        fundedBy=fundedBy,
        projectManagementAgency=projectManagementAgency,
        researchProgram=researchProgram,
        fundingProgram=fundingProgram
    )
    return obj, created

def getOrCreateAddress(row, header, who):
    """
    add entry into table anschrift or/and return entry key

    who options:
    - 'GrantRecipient' : zuwendungsempfaenger
    - 'ExecutingEntity' : ausfehrende Stelle
    """
    # content = row[number of the columns of the row]
    # decision kind of persion, where should the data read from, maybe later needed
    if who == 'GrantRecipient':
        plz = row[header.index('PLZ_ZWE')]
        location = row[header.index('Ort_ZWE')]
        state = row[header.index('Land_ZWE')]
        address = row[header.index('Adress_ZWE')]
    elif who == 'ExecutingEntity':
        plz = row[header.index('PLZ_AS')]
        location = row[header.index('Ort_AS')]
        state = row[header.index('Land_AS')]
        address = row[header.index('Adress_AS')]

    obj, created = Address.objects.get_or_create(
        plz = plz,
        location = location,
        state = state,
        address = address
    )
    return obj, created

def getOrCreatePerson(row, header):
    """
    add entry into table person or/and return entry key
    """
    # content = row[number of the columns of the row]
    # decision kind of persion, where should the data read from, maybe later needed
    surname = row[header.index('Name_pl')]
    firstName = row[header.index('Vorname_pl')]
    title = row[header.index('Titel_pl')]
    email = row[header.index('Email_pl')]
    obj, created = Person.objects.get_or_create(
        surname = surname,
        firstName = firstName,
        title = title,
        email = email
    )
    return obj, created

def getOrCreateRAndDPlanningCategory(row, header):
    """
    add entry into table RAndDPlanningCategory (leistungsplansystematik) or/and return entry key
    """
    # content = row[number of the columns of the row]
    rAndDPlanningCategoryText = row[header.index('Leistungsplan_Sys_Text')]
    rAndDPlanningCategoryNumber = row[header.index('Leistungsplan_Sys_Nr')]

    obj, created = RAndDPlanningCategory.objects.get_or_create(
        rAndDPlanningCategoryNumber =  rAndDPlanningCategoryNumber,
        rAndDPlanningCategoryText = rAndDPlanningCategoryText
    )
    return obj, created

def getOrCreateGrantRecipient(row, header):
    """
    add entry into table GrantRecipient (zuwendungsempfaenger) or/and return entry key
    """
   # fill table address in case of zuwendungsempfaenger
    # or/and get the address_id
    objAddressGrantRecipient, createdGrantRecipient = getOrCreateAddress(row, header, 'GrantRecipient')
    grantRecipientAddress_id = objAddressGrantRecipient.address_id

    # content = row[number of the columns of the row]
    name = row[header.index('Name_ZWE')]
    obj, created = GrantRecipient.objects.get_or_create(
        name = name,
        address_id = grantRecipientAddress_id
    )
    return obj, created

def getOrCreateExecutingEntity(row, header):
    """
    add entry into table ausfuehrende_stelle or/and return entry key
    """
   # fill table address in case of ausfuehrende_stelle
    # or/and get the address_id
    objAddressExecutingEntity, createdAddressExecutingEntity = getOrCreateAddress(row, header, 'ExecutingEntity') ### what does ans mean here?
    executingEntityAddress_id = objAddressExecutingEntity.address_id

    # content = row[number of the columns of the row]
    name = row[header.index('Name_AS')]
    obj, created = ExecutingEntity.objects.get_or_create(
        name = name,
        address_id = executingEntityAddress_id
    )
    return obj, created

def getOrCreateEnargus(row, header):
    """
    add entry into table enargus or/and return entry key
    """
    # content = row[number of the columns of the row]
    # print(forschung_id)

    # fill table zuwendungsempfaenger or/and get the zuwendungsempfaenger_id
    objGrantRecipient, createdGrantRecipient = getOrCreateGrantRecipient(row, header)
    grantRecipient_id = objGrantRecipient.grantRecipient_id

    # fill table ausfuehrende_stelle or/and get the ausfuehrende_stelle_id
    objExecutingEntity, createdExecutingEntity = getOrCreateExecutingEntity(row, header)
    executingEntity_id = objExecutingEntity.executingEntity_id

    # fill table leistung_sys or/and get the leistungsplansystematik_nr
    objRAndDPlanningCategory, createdRAndDPlanningCategory = getOrCreateRAndDPlanningCategory(row, header)
    rAndDPlanningCategoryNumber = objRAndDPlanningCategory.rAndDPlanningCategoryNumber

    # fill table person or/and get the person_id
    objPerson, createdPerson = getOrCreatePerson(row, header)
    person_id = objPerson.person_id

    # fill table forschung or/and get the forschung_id
    objFurtherFundingInformation, createdFurtherFundingInformation = getOrCreateFurtherFundingInformation(row, header)
    furtherFundingInformation_id = objFurtherFundingInformation.furtherFundingInformation_id

    startDate = row[header.index('Laufzeitbeginn')]
    endDate = row[header.index('Laufzeitende')]
    topics = row[header.index('Thema')]
    collaborativeProject = row[header.index('Verbundbezeichung')]
    appropriatedBudget = float(row[header.index('Foerdersumme_EUR')])
    shortDescriptionDe = row[header.index('Kurzbeschreibung_de')]
    shortDescriptionEn = row[header.index('Kurzbeschreibung_en')]
    database = row[header.index('Datenbank')]
    obj, created = Enargus.objects.get_or_create(
        startDate=startDate,
        endDate=endDate,
        topics=topics,
        # instead of using only the name of the feature in case
        # of foreigne keys use the name+_id, I dont know why
        projectLead_id = person_id,
        furtherFundingInformation_id = furtherFundingInformation_id,
        rAndDPlanningCategory_id = rAndDPlanningCategoryNumber,
        grantRecipient_id = grantRecipient_id,
        executingEntity_id = executingEntity_id,
        collaborativeProject = collaborativeProject,
        appropriatedBudget = appropriatedBudget,
        shortDescriptionDe = shortDescriptionDe,
        shortDescriptionEn = shortDescriptionEn,
        database = database
    )
    return obj, created

def getOrCreateModuleAssignment(row, header):
    """
    add entry into table modulen_zuordnung_ptj or/and return entry key
    """
    # content = row[number of the columns of the row]

    priority1 = row[header.index('modulzuordnung_ptj_1')]
    priority2 = row[header.index('modulzuordnung_ptj_2')]
    priority3 = row[header.index('modulzuordnung_ptj_3')]
    priority4 = row[header.index('modulzuordnung_ptj_4')]
    obj, created = ModuleAssignment.objects.get_or_create(
        priority1 = priority1,
        priority2 = priority2,
        priority3 = priority3,
        priority4 = priority4
    )
    return obj, created

def getOrCreateTools(row, header, image_path):
    """
    add entry into table Tools or/and return entry key
    """
    # content = row[number of the columns of the row]
    name = row[header.index('Tool')]
    shortDescription = row[header.index('Kurzbeschreibung')]
    applicationArea = row[header.index('Anwendungsbereich')]
    usage = row[header.index('Kategorie')]
    lifeCyclePhase = row[header.index('Lebenszyklusphase')]
    userInterface = row[header.index('Nutzerschnittstelle')]
    targetGroup = row[header.index('Zielgruppe')]
    lastUpdate= row[header.index('letztes Update')]
    licence = row[header.index('Lizenz')]
    furtherInformation = row[header.index('weitere Informationen')]
    alternatives = row[header.index('Alternativen')]
    specificApplication = row[header.index('konkrete Anwendung in EWB Projekten')]
    # userEvaluation = row[header.index('Nutzerbewertungen')]
    if type(image_path) == str:
        image = image_path
    else:
        image = None
    # released
    # releasePlanned
    # yearOfRelease
    # resources
    # developmentState
    # programmingLanguages
    # frameworksLibraries
    # databaseSystem
    # classification
    # scale
    # technicalStandards

    obj, created = Tools.objects.get_or_create(
        name = name,
        shortDescription = shortDescription,
        applicationArea = applicationArea,
        usage = usage,
        lifeCyclePhase = lifeCyclePhase,
        userInterface = userInterface,
        targetGroup = targetGroup,
        lastUpdate = lastUpdate,
        licence = licence,
        furtherInformation = furtherInformation,
        alternatives = alternatives,
        specificApplication = specificApplication,
        image = image
        # nutzerbewertungen = nutzerbewertung
    )
    return obj, created

def getOrCreateWeatherData(row, header):
    """
    add entry into table Weatherdata or/and return entry key
    """
    # content = row[number of the columns of the row]

    data_service = row[header.index('data_service')]
    short_description = row[header.index('short_description')]
    provider = row[header.index('provider')]
    further_infos = row[header.index('further_information')]
    data_url = row[header.index('data_url')]
    logo_url = row[header.index('logo_url')]
    applications = row[header.index('applications')]
    last_update= row[header.index('last_update')]
    license = row[header.index('license')]
    category = row[header.index('category')]
    long_description = row[header.index('long_description')]
    image = row[header.index('image')]
    
    obj, created = Weatherdata.objects.get_or_create(
        data_service = data_service,
        short_description = short_description,
        provider = provider,
        further_information = further_infos,
        data_url = data_url,
        logo_url = logo_url,
        applications = applications,
        last_update = last_update,
        license = license,
        category = category,
        long_description = long_description,
        image = image
    )
    return obj, created

def getOrCreateKeyword(row, header, keywordKey):
    """
    add entry into table forschung or/and return entry key
    """
    # content = row[number of the columns of the row]
    keyword = row[header.index(keywordKey)]
    obj, created = Keyword.objects.get_or_create(
        keyword = keyword
    )
    return obj, created

def getOrCreateKeywordRegister(row, header):
    """
    add entry into table Weatherdata or/and return entry key
    """
    objKeyword1, createdKeyword1 = getOrCreateKeyword(row, header, 'Schlagwort1')
    keyword1_id = objKeyword1.keyword_id

    objKeyword2, createdKeyword2 = getOrCreateKeyword(row, header, 'Schlagwort2')
    keyword2_id = objKeyword2.keyword_id

    objKeyword3, createdKeyword3 = getOrCreateKeyword(row, header, 'Schlagwort3')
    keyword3_id = objKeyword3.keyword_id

    objKeyword4, createdKeyword4 = getOrCreateKeyword(row, header, 'Schlagwort4')
    keyword4_id = objKeyword4.keyword_id

    objKeyword5, createdKeyword5 = getOrCreateKeyword(row, header, 'Schlagwort5')
    keyword5_id = objKeyword5.keyword_id

    objKeyword6, createdKeyword6 = getOrCreateKeyword(row, header, 'Schlagwort6')
    keyword6_id = objKeyword6.keyword_id

    objKeyword7, createdKeyword7 = getOrCreateKeyword(row, header, 'Schlagwort')
    keyword7_id = objKeyword7.keyword_id

    obj, created = KeywordRegisterFirstReview.objects.get_or_create(
        keyword1_id = keyword1_id,
        keyword2_id = keyword2_id,
        keyword3_id = keyword3_id,
        keyword4_id = keyword4_id,
        keyword5_id = keyword5_id,
        keyword6_id = keyword6_id,
        keyword7_id = keyword7_id
    )
    return obj, created

def addOrUpdateRowSubproject(row, header, source):
    """add or update one row of the database, but without foreign key connections

    source cases:
    - 'enargus' : read data from enargus xml via csv file (here csv will loaded)
    - 'module' : read data from 'verteiler xlsx' via csv file (here csv will loaded)

    """
    # fill table enargus or/and get the enargus_id
    if source == 'enargus':
        obj, created = getOrCreateEnargus(row, header)
        enargus_id = obj.enargus_id
        referenceNumber = row[header.index('FKZ')]

    # breakpoint()
        try:
            Subproject.objects.create(referenceNumber_id=referenceNumber,
                                    enargusData_id= enargus_id)
            print('added: %s' %referenceNumber)
        except IntegrityError:
            #answ = input("%s found in db. Update this part project? (y/n): "
            #         %referenceNumber)
            #if answ == 'y':
            Subproject.objects.filter(pk=referenceNumber).update(
                    enargusData_id= enargus_id)
    elif source == 'module':
        obj, created = getOrCreateModuleAssignment(row, header)
        moduleAssignment_id = obj.moduleAssignment_id
        referenceNumber = row[header.index('FKZ')]
        try:
            Subproject.objects.create(pk=referenceNumber,
                                    moduleAssignment_id= moduleAssignment_id)
            print('added: %s' %referenceNumber)
        except IntegrityError:
            Subproject.objects.filter(referenceNumber_id=referenceNumber).update(
                    moduleAssignment_id= moduleAssignment_id)
            print('updated: %s' %referenceNumber)
    elif source == 'keywordRegister':
        obj, created = getOrCreateKeywordRegister(row, header)
        keywordRegister_id = obj.keywordRegisterFirstReview_id
        referenceNumber = row[header.index('Förderkennzeichen (0010)')]
        try:
            keywordsFirstReview = KeywordRegisterFirstReview.objects.get(keywordRegisterFirstReview_id=keywordRegister_id)
            #print('checking keywords', keywordsFirstReview)
            Subproject.objects.create(referenceNumber_id=referenceNumber,
                                    keywordsFirstReview = keywordsFirstReview)
            print('added: %s' %referenceNumber)
        except IntegrityError:
            #answ = input("%s found in db. Update this part project? (Y/n): "
            #         %referenceNumber) or 'y'
            #if answ == 'y':
            keywordsFirstReview = KeywordRegisterFirstReview.objects.get(keywordRegisterFirstReview_id=keywordRegister_id)
            print('checking keywords', keywordsFirstReview)
            Subproject.objects.filter(pk=referenceNumber).update(
                keywordsFirstReview = keywordsFirstReview)
            print('updated: %s' %referenceNumber)

def getOrCreateNorms(row, header):
    """
    add entry (Norms) into table or/and return entry key
    """
    # content = row[number of the columns of the row]
    isNorm = True
    name = row[header.index('Name')]
    shortDescription = row[header.index('ShortDescription')]
    title = row[header.index('Title')]
    source  = row[header.index('Source')]
    link  = row[header.index('Link')]

    obj, created = Norm.objects.get_or_create(
        isNorm = isNorm,
        name = name,
        shortDescription = shortDescription,
        title = title, 
        source  = source,
        link = link 
    )
    return obj, created

def getOrCreateProtocols(row, header):
    """
    add entry (Protocols) into table or/and return entry key
    """
    # content = row[number of the columns of the row]
    isNorm = False 
    name = row[header.index('name')]
    communicationMediumCategory = row[header.index('communicationMediumCategory')]
    supportedTransmissionMediuems = row[header.index('supportedTransmissionMediuems')]
    associatedStandards  = row[header.index('associatedStandards')]
    openSourceStatus  = row[header.index('openSourceStatus')]
    licensingFeeRequirement = row[header.index('licensingFeeRequirement')]
    networkTopology  = row[header.index('networkTopology')]
    security  = row[header.index('security')]
    bandwidth  = row[header.index('bandwith')]
    frequency  = row[header.index('frequency')]
    range = row[header.index('range')]
    numberOfConnectedDevices  = row[header.index('numberOfConnectedDevices')]
    dataModelArchitecture = row[header.index('dataModelArchitecture')]
    discovery  = row[header.index('discovery')]
    multiMaster  = row[header.index('multiMaster')]
    packetSize  = row[header.index('packetSize')]
    priorities  = row[header.index('priorities')]
    price = row[header.index('price')]
    osiLayers  = row[header.index('osiLayers')]
    buildingAutomationLayer  = row[header.index('buildingAutomationLayer')]
    exampleProject = row[header.index('exampleProject')]
    link  = row[header.index('link')]
    image  = row[header.index('image')]
    obj, created = Protocol.objects.get_or_create(
        isNorm = isNorm,
        name = name,
        communicationMediumCategory = communicationMediumCategory,
        supportedTransmissionMediuems = supportedTransmissionMediuems,
        associatedStandards  = associatedStandards,
        openSourceStatus  = openSourceStatus,
        licensingFeeRequirement = licensingFeeRequirement,
        networkTopology  = networkTopology,
        security  = security,
        bandwidth  = bandwidth,
        frequency  = frequency,
        range = range,
        numberOfConnectedDevices  = numberOfConnectedDevices,
        dataModelArchitecture = dataModelArchitecture,
        discovery  = discovery,
        multiMaster = multiMaster,
        packetSize = packetSize,
        priorities  = priorities,
        price = price,
        osiLayers  = osiLayers,
        buildingAutomationLayer  = buildingAutomationLayer,
        exampleProject = exampleProject,
        link = link,
        image = image
    )
    return obj, created

def csv2m4dbEnargus(path):
    """EnArgus csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
            addOrUpdateRowSubproject(row, header, 'enargus')
    return header, data

def csv2m4dbModule(path):
    """Modul csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            # print(row[header.index('FKZ')])
            data.append(row)
            addOrUpdateRowSubproject(row, header, 'module')
    return header, data

def readPrintCsv(path):
    """Test function EnArgus csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
            # print(row[header.index('FKZ')])
    return header, data

def csv2m4dbTools(path, toolsImages):
    """tool overview csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter=';')
        header = next(reader)
        data = []
        for ii, row in enumerate(reader):
            print(row[header.index('Tool')])
            image = toolsImages.loc[row[header.index('Tool')]]['image']
            print(image)
            getOrCreateTools(row, header, image)
    return header, data   

def csv2m4dbWeatherData(path):
    """Weatherdata csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            print(row[header.index('data_service')])
            data.append(row)
            # breakpoint()
            getOrCreateWeatherData(row, header)
    return header, data

def csv2m4dbKeywordRegisterFirstReview(path):
    """KeywordRegisterFirstReview csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            print(row[header.index('Förderkennzeichen (0010)')])
            data.append(row)
            # breakpoint()
            # get_or_create_schlagwortregister(row, header)
            addOrUpdateRowSubproject(row, header, 'keywordRegister')
    return header, data

def csv2m4dbNorms(path):
    """Normen csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter='|')
        header = next(reader)
        data = []
        for row in reader:
            try:
                print(row[header.index('Name')])
                data.append(row)
                # breakpoint()
                getOrCreateNorms(row, header)
            except:
                print('NOT WORKING FOR ROW ', row)
    return header, data

def csv2m4dbProtocols(path):
    """Normen csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter='|')
        header = next(reader)
        data = []
        for row in reader:
            try:
                print(row[header.index('name')])
                data.append(row)
                # breakpoint()
                getOrCreateProtocols(row, header)
            except:
                print('NOT WORKING FOR ROW ', row)
    return header, data

def removeFromDatabase(modelName):
    try:
        records = modelName.objects.all()
        records.delete()
    except:
        print('Removal of records <', modelName,'> from database failed...')
    return

def retrieveImageFromDatabase():
    # retrieve image path and tool names from the database <- to be executed BEFORE Tools in database are modified!
    import psycopg2
    import pandas as pd
    from sqlalchemy import create_engine
    # Create an engine instance
    #conn_string = 'postgresql://dbadmint:abc123@localhost:5432/m4_data3'
    ## remote access after config the server see [[remote_postgresql.org]
    conn_string = 'postgresql://adm_webcentral:abc123@database/m4_db_serv_22070'
    alchemeyEngine = create_engine(conn_string)
    conn = alchemeyEngine.connect() 
    # Read data from PostgreSQL database table and load into a DataFrame instance
    ## test the sql code and find the specific name of the tables, use pgadmin
    df = pd.read_sql_query(
        """
        SELECT tools_over_tools.Bezeichnung, tools_over_tools.Image
        FROM tools_over_tools
        """
    , conn) 
    conn.close()
    alchemeyEngine.dispose()
    df.to_csv('/src/02_work_doc/01_daten/02_toolUebersicht/image_list.csv')
    return df 

def loadClassificationAndFocus(filename):
    """Loads Classifcation and Focus for the Tools
    
    """    
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        header = next(reader)
        data = []
        for ii, row in enumerate(reader):
            print(row[header.index('Tool')])
            tool = row[header.index('Tool')]
            classificationStr = row[header.index('classification')]
            classificationDjangoQuery = Classification.objects.filter(classification=classificationStr)
            focusStr = row[header.index('focus')]
            focusDjangoQuery = Focus.objects.filter(focus=focusStr)
            # pdb.set_trace()
            if len(classificationDjangoQuery) == 1 and len(focusDjangoQuery) == 1:
                querySet = Tools.objects.filter(name=tool)
                
                if len(querySet) == 1:
                    # pdb.set_trace()
                    querySet[0].focus.set(focusDjangoQuery)
                    querySet[0].classification.set(classificationDjangoQuery)
            
    return header, data 

def loadDigitalApplication(filename):
    """loads digital application into the database

    """
    with open(filename, encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        header = next(reader)
        data = []
        for ii, row in enumerate(reader):
            getOrCreateDigitalApplication(row, header)
    return header, data  

def getOrCreateDigitalApplication(row, header):
    """
    add entry into table Tools or/and return entry key
    """
    # content = row[number of the columns of the row]
    name = row[header.index('Name')]
    provider = row[header.index('Anbieter')]
    shortDescription = row[header.index('Kurzbeschreibung (Was ist XY?)')]
    classification = Classification.objects.filter(classification="Digitale Anwendung")
    focus = Focus.objects.filter(focus="Betrieblich")
    lifeCyclePhase = row[header.index('Lebenszyklusphase')]
    userInterface = row[header.index('Nutzerschnittstelle')]
    targetGroup = row[header.index('Zielgruppe')]
    licence = row[header.index('Lizenz')]
    image_path = row[header.index('Bild / Icon')]
    furtherInformation = row[header.index('Weitere Informationen')]
    if type(image_path) == str:
        image = image_path
    else:
        image = None
    # released
    # releasePlanned
    # yearOfRelease
    # resources
    # developmentState
    # programmingLanguages
    # frameworksLibraries
    # databaseSystem
    # classification
    # scale
    # technicalStandards
    # pdb.set_trace()
    obj, created = Tools.objects.get_or_create(
        name=name,
        provider=provider,
        shortDescription=shortDescription,
        lifeCyclePhase=lifeCyclePhase,
        userInterface=userInterface,
        targetGroup=targetGroup,
        licence = licence,
        furtherInformation = furtherInformation,
        image=image,
    )
    obj.classification.set(classification)
    obj.focus.set(focus)
    return obj, created

# Script area (here you find examples to use the functions ahead)
# retrieved BEFORE Tools are modified in database! 
#retrieveImageFromDatabase()
#removeFromDatabase(Tools)
#re-import tools into database
    
#pathCsvTools='/src/02_work_doc/01_daten/02_toolUebersicht/2022_02_22_EWB_Tools_Uebersicht.csv'
#pathCsvToolsImages = '/src/02_work_doc/01_daten/02_toolUebersicht/image_list.csv'
import pandas as pd
#toolsImages = pd.read_csv(pathCsvToolsImages,index_col=['bezeichnung'])
#header, data = csv2m4dbTools(pathCsvTools, toolsImages)

## add/update norm data
removeFromDatabase(Norm)
pathCsvNorms='/src/02_work_doc/01_daten/05_technicalStandards/2023_04_17_Normen.csv'
header, data = csv2m4dbNorms(pathCsvNorms)

pathCsvProtocols = '/src/02_work_doc/01_daten/05_technicalStandards/2023_08_21_Protokolle.csv'
header, data =  csv2m4dbProtocols(pathCsvProtocols)

## Example add/update Weatherdata table
#pathCsvWeatherData='/src/02_work_doc/01_daten/03_weatherdata/2023_06_07_weatherdata.csv'
#header, data = csv2m4dbWeatherData(pathCsvWeatherData)

## Example add/update Schlagwoerter table
# pathCsvKeywords='./02_work_doc/01_daten/04_schlagwoerter/schlagwoerter_csv_fkz_over_orthography_edit.csv'
# header, data = csv2m4dbKeywordRegisterFirstReview(pathCsvKeywords)

# ## add/update Enargus data
# pathCsvEnargus ='./02_work_doc/01_daten/01_prePro/enargus_csv_20230403.csv'
# header, data = csv2m4dbEnargus(pathCsvEnargus)

# ## add/update ModuleAssignment data
# pathCsvModule='./02_work_doc/01_daten/01_prePro/modulzuordnung_csv_20230403.csv'
# header, data = csv2m4dbModule(pathCsvModule)


pathToToolsClassificationFocusMapping = '/src/02_work_doc/01_daten/02_toolUebersicht/toolClassificationFocus.csv'
header, data = loadClassificationAndFocus(pathToToolsClassificationFocusMapping)

pathToDigitalApplicationCSV = '/src/02_work_doc/01_daten/06_digitaleAnwendungen/Tools-Digitale-Geschäftsmodelle.csv'
header, data = loadDigitalApplication(pathToDigitalApplicationCSV)

#pathToToolsClassificationFocusMapping = '/src/02_work_doc/01_daten/02_toolUebersicht/toolClassificationFocus.csv'
#header, data = loadClassificationAndFocus(pathToToolsClassificationFocusMapping)

#pathToDigitalApplicationCSV = '/src/02_work_doc/01_daten/06_digitaleAnwendungen/Tools-Digitale-Geschäftsmodelle.csv'
#header, data = loadDigitalApplication(pathToDigitalApplicationCSV)

