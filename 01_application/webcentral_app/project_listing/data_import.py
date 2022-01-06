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

def get_or_create_enargus(row, header):
    """
    add entry into table enargus or/and return entry key
    """
    # content = row[number of the columns of the row]

    # fill table forschung or/and get the forschung_id
    obj, created = get_or_create_forschung(row, header)
    forschung_id = obj.forschung_id

    laufzeitbeginn = row[header.index('Laufzeitbeginn')]
    laufzeitende = row[header.index('Laufzeitende')]
    thema = row[header.index('Thema')]
    obj, created = Enargus.objects.get_or_create(
        laufzeitbeginn=laufzeitbeginn,
        laufzeitende=laufzeitende,
        thema=thema,
        forschung_id = forschung_id
    )
    return obj, created

def add_or_update_row_teilprojekt(row, header):
    """add or update one row of the database, but without foreign key connections

    """
    # fill table enargus or/and get the enargus_id
    obj, created = get_or_create_enargus(row, header)
    enargus_id = obj.enargus_id
    try:
        Teilprojekt.objects.create(fkz=row[header.index('FKZ')],
                                    enargus_daten_id= enargus_id)
    except IntegrityError:
        answ = input("FKZ ist vorhanden. Sollen die alten Elemente mit \
        den neuen Werten ueberschrieben werden (y/n): ")
        if answ == 'y':
            Teilprojekt.objects.filter(pk=row[header.index('FKZ')]).update(
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
path_csv='../../02_work_doc/BF_M4_DB_60rows.csv'
header, data = csv2m4db(path_csv)
# data_2 = data[2]
