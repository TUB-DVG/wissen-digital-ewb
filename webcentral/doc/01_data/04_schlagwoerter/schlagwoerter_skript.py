import csv
from encodings import utf_8
import re

# -*- coding: utf-8 -*-


def csv2m4db_keywords(path):
    with open(path, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)

    toWriteFkzOver = [
        [
            "Förderkennzeichen (0010)",
            "Schlagwort1",
            "Schlagwort2",
            "Schlagwort3",
            "Schlagwort4",
            "Schlagwort5",
            "Schlagwort6",
            "Schlagwort",
        ],
    ]
    fkz_over_schlagwoerter_liste = {}

    for row in data:
        fkz = row[header.index("Förderkennzeichen (0010)")]
        fkz_over = fkz
        if fkz[-1].isalpha():
            fkz_over = fkz[:-1]
        if not fkz_over in fkz_over_schlagwoerter_liste:
            fkz_over_schlagwoerter_liste[fkz_over] = {
                "Schlagwort1": row[header.index("Schlagwort1")],
                "Schlagwort2": row[header.index("Schlagwort2")],
                "Schlagwort3": row[header.index("Schlagwort3")],
                "Schlagwort4": row[header.index("Schlagwort4")],
                "Schlagwort5": row[header.index("Schlagwort5")],
                "Schlagwort6": row[header.index("Schlagwort6")],
                "Schlagwort": row[header.index("Schlagwort")],
            }
        toWriteFkzOver.append(
            [
                row[header.index("Förderkennzeichen (0010)")],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort1"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort2"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort3"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort4"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort5"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort6"],
                fkz_over_schlagwoerter_liste[fkz_over]["Schlagwort"],
            ]
        )

    schlagwoerter_csv_fkz_over = open(
        "schlagwoerter_csv_fkz_over.csv", "w+", encoding="utf-8"
    )

    with schlagwoerter_csv_fkz_over:
        writer = csv.writer(schlagwoerter_csv_fkz_over, delimiter=";")
        for row in toWriteFkzOver:
            writer.writerow(row)

    return header, data


## Example schlagwoerter Path "/WenDE/12_Daten/03_Gesamt_BF_Daten/Leistungsplansystematik/"
path_csv_schlagwoerter = "ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.csv"
header, data = csv2m4db_keywords(path_csv_schlagwoerter)
