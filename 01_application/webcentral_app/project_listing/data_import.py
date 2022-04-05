import csv
from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *

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

def get_or_create_tools(row, header):
    """
    add entry into table tools or/and return entry key
    """
    # content = row[number of the columns of the row]

    bezeichung = row[header.index('Tool')]
    kurzbe = row[header.index('Kurzbeschreibung')]
    anwend_bereich = row[header.index('Anwendungsbereich')]
    kategorie = row[header.index('Kategorie')]
    lebenszy = row[header.index('Lebenszyklusphase')]
    nutzersch = row[header.index('Nutzerschnittstelle')]
    zielgruppe = row[header.index('Zielgruppe')]
    letztes_update= row[header.index('letztes Update')]
    lizenz = row[header.index('Lizenz')]
    weitere_infos = row[header.index('weitere Informationen')]
    alternativen = row[header.index('Alternativen')]
    konk_anw_ewb = row[header.index('konkrete Anwendung in EWB Projekten')]
    nutzerbewertung = row[header.index('Nutzerbewertungen')]


    obj, created = Tools.objects.get_or_create(
        bezeichnung = bezeichung,
        kurzbeschreibung = kurzbe,
        anwendungsbereich = anwend_bereich,
        kategorie = kategorie,
        lebenszyklusphase = lebenszy,
        nutzerschnittstelle = nutzersch,
        zielgruppe = zielgruppe,
        letztes_update = letztes_update,
        lizenz = lizenz,
        weitere_informationen = weitere_infos,
        alternativen = alternativen,
        konk_anwendung = konk_anw_ewb,
        # nutzerbewertungen = nutzerbewertung
    )
    return obj, created

def get_or_create_weatherdata(row, header):
    """
    add entry into table tools or/and return entry key
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

def csv2m4db_tools(path):
    """tools Uebersicht csv-file into BF M4 Django database, hard coded"""
    with open(path, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            print(row[header.index('Tool')])
            data.append(row)
            # breakpoint()
            get_or_create_tools(row, header)
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


# Script area (here you find examples to use the functions ahead)

## Example add/update Enargus data
# path_csv_enargus='../../02_work_doc/01_daten/01_prePro/enargus_csv_20220216.csv'
# header, data = csv2m4db_enargus(path_csv_enargus)

## Example add/update Modul-Zuordnung data
# path_csv_modul='../../02_work_doc/01_daten/01_prePro/modulzuordnung_csv_20220225.csv'
# header, data = csv2m4db_modul(path_csv_modul)

## Example add/update Tool Uebersichts table
# path_csv_tools='../../02_work_doc/01_daten/02_toolUebersicht/2022_02_22_EWB_Tools_Uebersicht.csv'
# header, data = csv2m4db_tools(path_csv_tools)

## Example add/update Weatherdata table
path_csv_weatherdata='../../02_work_doc/01_daten/03_weatherdata/2022_03_31_weatherdata.csv'
header, data = csv2m4db_weatherdata(path_csv_weatherdata)
 #
 #
