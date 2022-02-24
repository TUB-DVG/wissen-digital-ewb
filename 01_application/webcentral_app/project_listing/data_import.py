import csv
from project_listing.models import *

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

def get_or_create_enargus(row, header):
    """
    add entry into table enargus or/and return entry key
    """
    # content = row[number of the columns of the row]
    # print(forschung_id)
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
    obj, created = Enargus.objects.get_or_create(
        laufzeitbeginn=laufzeitbeginn,
        laufzeitende=laufzeitende,
        thema=thema,
        # instead of using only the name of the feature in case
        # of foreigne keys use the name+_id, I dont know why
        projektleiter_id = person_id,
        forschung_id = forschung_id,
        verbundbezeichnung = verbundbezeichnung,
        foerdersumme = foerdersumme
    )
    return obj, created

def add_or_update_row_teilprojekt(row, header):
    """add or update one row of the database, but without foreign key connections

    """
    # fill table enargus or/and get the enargus_id
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

def csv2m4db(path):
    """EnArgus csv-file into BF M4 Django database, hard coded"""
    with open(path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
            add_or_update_row_teilprojekt(row, header)
            # print(row[header.index('FKZ')])
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


# Script area (here you find examples to use the functions ahead)

# print('jupp')
path_csv='../../02_work_doc/01_daten/01_prePro/enargus_csv_20220216.csv'
header, data = csv2m4db(path_csv)
# data_2 = data[2]
