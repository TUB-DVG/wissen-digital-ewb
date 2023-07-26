import pandas as pd
import csv

df = pd.read_csv('2022_02_22_EWB_Tools_Uebersicht.csv', sep=';', header=0)

toolsList = df.Tool.tolist()
# classificationList = []
# focusList = []
csvList = []
for tool in toolsList:
    csvList.append((tool, "Digitales Werkzeug", "Technisch"))
    # classificationList.append("Werkzeug")
    # focusList.append("Technisch")

cols = ["Tool", "classification", "focus"]

with open('toolClassificationFocus.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(cols)
    for row in csvList:
        csv_out.writerow(row)