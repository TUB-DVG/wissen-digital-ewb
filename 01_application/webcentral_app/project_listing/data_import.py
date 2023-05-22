import csv
from encodings import utf_8
from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from schlagwoerter.models import *
from norms_over.models import *

# -*- coding: utf-8 -*-

def get_or_create_forschung(row, header):
    """
    add entry into table forschung or/and return entry key
    """
    # content = row[number of the columns of the row]
    bundesministerium = row[header.index('Bundesministerium')]
    projekttraeger = row[header.index('Projekttraeger')]
    foerderprogramm = row[header.index('Foerderprogramm')]
    forschungsprogramm = row[header.index('Forschungsprogramm')]
    obj, created = Forschung.objects.get_or_create(
        bundesministerium=bundesministerium,
        projekttraeger=projekttraeger,
        forschungsprogramm=forschungsprogramm,
        foerderprogramm=foerderprogramm
    )
    return obj, created

def get_or_create_anschrift(row, header, who):
    """
    add entry into table anschrift or/and return entry key

    who options:
    - 'zwe' : zuwendungsempfaenger
    - 'as' : ausfehrende Stelle
    """
    # content = row[number of the columns of the row]
    # decision kind of persion, where should the data read from, maybe later needed
    if who == 'zwe':
        plz = row[header.index('PLZ_ZWE')]
        ort = row[header.index('Ort_ZWE')]
        land = row[header.index('Land_ZWE')]
        adresse = row[header.index('Adress_ZWE')]
    elif who == 'as':
        plz = row[header.index('PLZ_AS')]
        ort = row[header.index('Ort_AS')]
        land = row[header.index('Land_AS')]
        adresse = row[header.index('Adress_AS')]

    obj, created = Anschrift.objects.get_or_create(
        plz = plz,
        ort = ort,
        land = land,
        adresse = adresse
    )
    return obj, created

def get_or_create_person(row, header):
    """
    add entry into table person or/and return entry key
    """
    # content = row[number of the columns of the row]
    # decision kind of persion, where should the data read from, maybe later needed
    name = row[header.index('Name_pl')]
    vorname = row[header.index('Vorname_pl')]
    titel = row[header.index('Titel_pl')]
    email = row[header.index('Email_pl')]
    obj, created = Person.objects.get_or_create(
        name = name,
        vorname = vorname,
        titel = titel,
        email = email
    )
    return obj, created

def get_or_create_leistung_sys(row, header):
    """
    add entry into table leistung_sys or/and return entry key
    """
    # content = row[number of the columns of the row]
    leistungsplansystematik_text = row[header.index('Leistungsplan_Sys_Text')]
    leistungsplansystematik_nr = row[header.index('Leistungsplan_Sys_Nr')]

    obj, created = Leistung_sys.objects.get_or_create(
        leistungsplansystematik_nr =  leistungsplansystematik_nr,
        leistungsplansystematik_text = leistungsplansystematik_text
    )
    return obj, created

def get_or_create_zuwendungsempfaenger(row, header):
    """
    add entry into table zuwendungsempfaenger or/and return entry key
    """
   # fill table anschrift in case of zuwendungsempfaenger
    # or/and get the anschrift_id
    obj_ans_zwe, created_ans_zwe = get_or_create_anschrift(row, header, 'zwe')
    zwe_ans_id = obj_ans_zwe.anschrift_id

    # content = row[number of the columns of the row]
    name = row[header.index('Name_ZWE')]
    obj, created = Zuwendungsempfaenger.objects.get_or_create(
        name = name,
        anschrift_id = zwe_ans_id
    )
    return obj, created

def get_or_create_ausfuehrende_stelle(row, header):
    """
    add entry into table ausfuehrende_stelle or/and return entry key
    """
   # fill table anschrift in case of ausfuehrende_stelle
    # or/and get the anschrift_id
    obj_ans_as, created_ans_as = get_or_create_anschrift(row, header, 'as')
    as_ans_id = obj_ans_as.anschrift_id

    # content = row[number of the columns of the row]
    name = row[header.index('Name_AS')]
    obj, created = Ausfuehrende_stelle.objects.get_or_create(
        name = name,
        anschrift_id = as_ans_id
    )
    return obj, created

def get_or_create_enargus(row, header):
    """
    add entry into table enargus or/and return entry key
    """
    # content = row[number of the columns of the row]
    # print(forschung_id)

    # fill table zuwendungsempfaenger or/and get the zuwendungsempfaenger_id
    obj_zwe, created_zwe = get_or_create_zuwendungsempfaenger(row, header)
    zwe_id = obj_zwe.zuwendungsempfaenger_id

    # fill table ausfuehrende_stelle or/and get the ausfuehrende_stelle_id
    obj_as, created_as = get_or_create_ausfuehrende_stelle(row, header)
    as_id = obj_as.ausfuehrende_stelle_id

    # fill table leistung_sys or/and get the leistungsplansystematik_nr
    obj_lps, created_lps = get_or_create_leistung_sys(row, header)
    lps_nr = obj_lps.leistungsplansystematik_nr

    # fill table person or/and get the person_id
    obj_per, created_per = get_or_create_person(row, header)
    person_id = obj_per.person_id

    # fill table forschung or/and get the forschung_id
    obj_for, created_for = get_or_create_forschung(row, header)
    forschung_id = obj_for.forschung_id

    laufzeitbeginn = row[header.index('Laufzeitbeginn')]
    laufzeitende = row[header.index('Laufzeitende')]
    thema = row[header.index('Thema')]
    verbundbezeichnung = row[header.index('Verbundbezeichung')]
    foerdersumme = float(row[header.index('Foerdersumme_EUR')])
    kurzbeschreibung_de = row[header.index('Kurzbeschreibung_de')]
    kurzbeschreibung_en = row[header.index('Kurzbeschreibung_en')]
    datenbank = row[header.index('Datenbank')]
    obj, created = Enargus.objects.get_or_create(
        laufzeitbeginn=laufzeitbeginn,
        laufzeitende=laufzeitende,
        thema=thema,
        # instead of using only the name of the feature in case
        # of foreigne keys use the name+_id, I dont know why
        projektleiter_id = person_id,
        forschung_id = forschung_id,
        leistungsplan_systematik_id = lps_nr,
        zuwendsempfanger_id = zwe_id,
        ausfuehrende_stelle_id = as_id,
        verbundbezeichnung = verbundbezeichnung,
        foerdersumme = foerdersumme,
        kurzbeschreibung_de = kurzbeschreibung_de,
        kurzbeschreibung_en = kurzbeschreibung_en,
        datenbank = datenbank
    )
    return obj, created

def get_or_create_modulen_zuordnung(row, header):
    """
    add entry into table modulen_zuordnung_ptj or/and return entry key
    """
    # content = row[number of the columns of the row]

    priority_1 = row[header.index('modulzuordnung_ptj_1')]
    priority_2 = row[header.index('modulzuordnung_ptj_2')]
    priority_3 = row[header.index('modulzuordnung_ptj_3')]
    priority_4 = row[header.index('modulzuordnung_ptj_4')]
    obj, created = Modulen_zuordnung_ptj.objects.get_or_create(
        priority_1 = priority_1,
        priority_2 = priority_2,
        priority_3 = priority_3,
        priority_4 = priority_4
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

def get_or_create_weatherdata(row, header):
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
        long_description = long_description
    )
    return obj, created

def get_or_create_schlagwort(row, header, schlagwort_key):
    """
    add entry into table forschung or/and return entry key
    """
    # content = row[number of the columns of the row]
    schlagwort = row[header.index(schlagwort_key)]
    obj, created = Schlagwort.objects.get_or_create(
        schlagwort = schlagwort
    )
    return obj, created

def get_or_create_schlagwortregister(row, header):
    """
    add entry into table Weatherdata or/and return entry key
    """
    obj_schlagwort_1, created_schlagwort_1 = get_or_create_schlagwort(row, header, 'Schlagwort1')
    schlagwort_1_id = obj_schlagwort_1.schlagwort_id

    obj_schlagwort_2, created_schlagwort_2 = get_or_create_schlagwort(row, header, 'Schlagwort2')
    schlagwort_2_id = obj_schlagwort_2.schlagwort_id

    obj_schlagwort_3, created_schlagwort_3 = get_or_create_schlagwort(row, header, 'Schlagwort3')
    schlagwort_3_id = obj_schlagwort_3.schlagwort_id

    obj_schlagwort_4, created_schlagwort_4 = get_or_create_schlagwort(row, header, 'Schlagwort4')
    schlagwort_4_id = obj_schlagwort_4.schlagwort_id
    
    obj_schlagwort_5, created_schlagwort_5 = get_or_create_schlagwort(row, header, 'Schlagwort5')
    schlagwort_5_id = obj_schlagwort_5.schlagwort_id
    
    obj_schlagwort_6, created_schlagwort_6 = get_or_create_schlagwort(row, header, 'Schlagwort6')
    schlagwort_6_id = obj_schlagwort_6.schlagwort_id
    
    obj_schlagwort_7, created_schlagwort_7 = get_or_create_schlagwort(row, header, 'Schlagwort')
    schlagwort_7_id = obj_schlagwort_7.schlagwort_id
    

    obj, created = Schlagwortregister_erstsichtung.objects.get_or_create(
        schlagwort_1_id = schlagwort_1_id,
        schlagwort_2_id = schlagwort_2_id,
        schlagwort_3_id = schlagwort_3_id,
        schlagwort_4_id = schlagwort_4_id,
        schlagwort_5_id = schlagwort_5_id,
        schlagwort_6_id = schlagwort_6_id,
        schlagwort_7_id = schlagwort_7_id
    )
    return obj, created

def add_or_update_row_teilprojekt(row, header, source):
    """add or update one row of the database, but without foreign key connections

    source cases:
    - 'enargus' : read data from enargus xml via csv file (here csv will loaded)
    - 'modul' : read data from 'verteiler xlsx' via csv file (here csv will loaded)

    """
    # fill table enargus or/and get the enargus_id
    if source == 'enargus':
        obj, created = get_or_create_enargus(row, header)
        enargus_id = obj.enargus_id
        fkz = row[header.index('FKZ')]

    # breakpoint()
        try:
            Teilprojekt.objects.create(fkz=fkz,
                                    enargus_daten_id= enargus_id)
            print('added: %s' %fkz)
        except IntegrityError:
            answ = input("%s found in db. Update this part project? (y/n): "
                     %fkz)
            if answ == 'y':
                Teilprojekt.objects.filter(pk=fkz).update(
                    enargus_daten_id= enargus_id)
    elif source == 'modul':
        obj, created = get_or_create_modulen_zuordnung(row, header)
        mod_id = obj.mod_id
        fkz = row[header.index('FKZ')]
        try:
            Teilprojekt.objects.create(fkz=fkz,
                                    zuordnung_id= mod_id)
            print('added: %s' %fkz)
        except IntegrityError:
            answ = input("%s found in db. Update this part project? (Y/n): "
                     %fkz) or 'y'
            if answ == 'y':
                Teilprojekt.objects.filter(pk=fkz).update(
                    zuordnung_id= mod_id)
                print('updated: %s' %fkz)
    elif source == 'schlagwortregister':
        obj, created = get_or_create_schlagwortregister(row, header)
        schlagwortregister_id = obj.schlagwortregister_id
        fkz = row[header.index('Förderkennzeichen (0010)')]
        try:
            Teilprojekt.objects.create(fkz=fkz,
                                    schlagwortregister_erstsichtung_id = schlagwortregister_id)
            print('added: %s' %fkz)
        except IntegrityError:
            answ = input("%s found in db. Update this part project? (Y/n): "
                     %fkz) or 'y'
            if answ == 'y':
                Teilprojekt.objects.filter(pk=fkz).update(
                    schlagwortregister_erstsichtung_id= schlagwortregister_id)
                print('updated: %s' %fkz)

def getOrCreateNorms(row, header):
    """
    add entry into table Norms or/and return entry key
    """
    # content = row[number of the columns of the row]
    isNorm = True
    name = row[header.index('Name')]
    shortDescription = row[header.index('ShortDescription')]
    title = row[header.index('Title')]
    source  = row[header.index('Source')]
    link  = row[header.index('Link')]

    obj, created = TechnicalStandards.objects.get_or_create(
        isNorm = isNorm,
        name = name,
        shortDescription = shortDescription,
        title = title, 
        source  = source ,
        link = link 
    )
    return obj, created

def csv2m4db_enargus(path):
    """EnArgus csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
            add_or_update_row_teilprojekt(row, header, 'enargus')
    return header, data

def csv2m4db_modul(path):
    """Modul csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            # print(row[header.index('FKZ')])
            data.append(row)
            add_or_update_row_teilprojekt(row, header, 'modul')
    return header, data

def read_print_csv(path):
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
    """tools Uebersicht csv-file into BF M4 Django database, hard coded"""
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
def csv2m4db_weatherdata(path):
    """Weatherdata csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            print(row[header.index('data_service')])
            data.append(row)
            # breakpoint()
            get_or_create_weatherdata(row, header)
    return header, data


def csv2m4db_schlagwortregister_erstsichtung(path):
    """Weatherdata csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            print(row[header.index('Förderkennzeichen (0010)')])
            data.append(row)
            # breakpoint()
            # get_or_create_schlagwortregister(row, header)
            add_or_update_row_teilprojekt(row, header, 'schlagwortregister')
    return header, data

def csv2m4dbNorms(path):
    """Normen Uebersicht csv-file into BF M4 Django database, hard coded"""
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

def removeFromDatabase(modelName):
    try:
        records = modelName.objects.all()
        records.delete()
    except:
        print('Removal of records <', modelName,'> from database failed...')
    return

# Script area (here you find examples to use the functions ahead)

## Example add/update Enargus data
# path_csv_enargus='../../02_work_doc/01_daten/01_prePro/enargus_csv_20220216.csv'
# header, data = csv2m4db_enargus(path_csv_enargus)

## Example add/update Modul-Zuordnung data
# path_csv_modul='../../02_work_doc/01_daten/01_prePro/modulzuordnung_csv_20220225.csv'
# header, data = csv2m4db_modul(path_csv_modul)

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

# retrieved BEFORE Tools are modified in database! 
#retrieveImageFromDatabase()
#removeFromDatabase(Tools)
#re-import tools into database
pathCsvTools='./02_work_doc/01_daten/02_toolUebersicht/2022_02_22_EWB_Tools_Uebersicht.csv'
pathCsvToolsImages = './02_work_doc/01_daten/02_toolUebersicht/image_list.csv'
import pandas as pd
toolsImages = pd.read_csv(pathCsvToolsImages,index_col=['bezeichnung'])
header, data = csv2m4dbTools(pathCsvTools, toolsImages)

## Example add/update Weatherdata table
# path_csv_weatherdata='../../02_work_doc/01_daten/03_weatherdata/2022_03_31_weatherdata.csv'
# header, data = csv2m4db_weatherdata(path_csv_weatherdata)

## Example add/update Schlagwoerter table
#path_csv_schlagwoerter='../../02_work_doc/01_daten/04_schlagwoerter/schlagwoerter_csv_fkz_over_orthography_edit.csv'
#header, data = csv2m4db_schlagwortregister_erstsichtung(path_csv_schlagwoerter)

#pathCsvNorms='/src/02_work_doc/01_daten/05_normen/2023_04_17_Normen.csv'
#header, data = csv2m4dbNorms(pathCsvNorms)
