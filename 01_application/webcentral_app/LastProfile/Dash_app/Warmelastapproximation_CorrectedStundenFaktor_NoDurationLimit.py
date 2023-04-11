from turtle import color
import pandas as pd
import math
#Importing the wetterDienst library and the plotly library for graphing
import wetterdienst
from wetterdienst.provider.dwd.observation import DwdObservationRequest
import plotly.express as px
import plotly.graph_objects as go

Anwendung=2

Warmebedarf=1500000


#Setting up the resolution for data filtering
Resolution='HOURLY'

#Selecting the dataset

Dataset='AIR_TEMPERATURE'
# Parameter variable selection

Parameter='TEMPERATURE_AIR_MEAN_200'
#Setting up the Period

Period='RECENT'
# Acquiring all the stations that provide data according to selected filters
stations = DwdObservationRequest(
      parameter=Parameter,
      resolution=Resolution,
      period=Period
       )


station_id=44

data= stations.filter_by_station_id(station_id=station_id)

station_data = data.values.all().df
#print(len(station_data))

#Eingaben vom Server sind Im Kelvin wurden auf celsius umgeformt
station_data['value']=station_data['value'].apply(lambda x: x - 273.15)


Fehlende_werte=station_data['value'].isna().sum()

#station_data=station_data.dropna().reset_index(drop=True)
station_data['fehlend'] = 'False'
for i in range (0,len(station_data.index)):
    if math.isnan(station_data['value'][i]):
        station_data['value'][i]=station_data['value'][i-24]
        station_data['fehlend'][i]='True'






df_warme = pd.read_csv('Wärme_Strom.csv')



#Regressionskoeffizienten laden 
A=float(df_warme.iloc[:,9][Anwendung+4])


B=float(df_warme.iloc[:,10][Anwendung+4])
C=float(df_warme.iloc[:,11][Anwendung+4])
D=float(df_warme.iloc[:,12][Anwendung+4])

#Wochentagsfaktoren laden
W_Tag=[]
##Montag
W_Tag.append(float(df_warme.iloc[:,9][Anwendung+23]))
##Dienstag
W_Tag.append(float(df_warme.iloc[:,10][Anwendung+23]))
## Mittwoch
W_Tag.append(float(df_warme.iloc[:,11][Anwendung+23]))
##Donnerstag
W_Tag.append(float(df_warme.iloc[:,12][Anwendung+23]))
##Freitag
W_Tag.append(float(df_warme.iloc[:,13][Anwendung+23]))
##Samstag
W_Tag.append(float(df_warme.iloc[:,14][Anwendung+23]))
##Sonntag
W_Tag.append(float(df_warme.iloc[:,15][Anwendung+23]))



#Berechnung von h
h=[]

for i in range(0,station_data.shape[0]):
    T_average=0
    LaufV = i 
    j=0
    while j<24 and LaufV<station_data.shape[0]:

        T_moment=float(station_data['value'][LaufV])
        
        T_average=T_average+T_moment/24
        LaufV=LaufV+1
        j+=1


    h.append(round( A / (1 + (B / (T_average - 40)) ** C) + D,14))


#Stundenfaktoren
Zeile_Anfang=Anwendung*13 -24

#Stundenfaktoren für Montag einlesen
Splate=18
F_Montag = [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Montag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]

#print(F_Montag)
#Stundenfaktoren für Dienstag einlesen
Splate=44
F_Dienstag = [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Dienstag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]

#Stundenfaktoren für Mittwoch einlesen

Splate=70
F_Mittwoch = [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Mittwoch[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]

#Stundenfaktoren für Donnerstag einlesen
Splate=96
F_Donnerstag = [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Donnerstag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]

#Stundenfaktoren für Freitag einlesen
Splate=122
F_Freitag= [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Freitag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]


#Stundenfaktoren für Samstage einlesen
Splate=148
F_Samstag= [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Samstag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]

#Stundenfaktoren für Sonntage einlesen
Splate=174
F_Sonntag= [[0 for x in range(24)] for y in range(10)] 
for i in range(0,24):
    for j in range(0,10):
        F_Sonntag[j][i]=df_warme.iloc[:,Splate+i][Zeile_Anfang+j]



# Berechnung des stündlichen Wärmebedarfs
Q_average=Warmebedarf
Q=[]
#LaufV = 0
LaufV_Stunden = 0

#Berechnung mittleres h

h_average = 0
for i in range(0,station_data.shape[0]):
    h_average=h_average+h[i]

h_average = h_average / (station_data.shape[0])

i=0
for k in range (0,station_data.shape[0]):

            if i == 24 :
                i=0
          
            #Auswahl der Zeile in Abhängigkeit zur Außentemperatur
            if station_data['value'][LaufV_Stunden] <=-15:
                Zeile=0
            elif station_data['value'][LaufV_Stunden] <=-10 and station_data['value'][LaufV_Stunden] >-15:
                Zeile=1
            elif station_data['value'][LaufV_Stunden] <=-5 and station_data['value'][LaufV_Stunden] >-10:
                Zeile=2
            elif station_data['value'][LaufV_Stunden] <=0 and station_data['value'][LaufV_Stunden] >-5:
                Zeile=3
            elif station_data['value'][LaufV_Stunden] <=5 and station_data['value'][LaufV_Stunden] >0:
                Zeile=4
            elif station_data['value'][LaufV_Stunden] <=10 and station_data['value'][LaufV_Stunden] >5:
                Zeile=5
            elif station_data['value'][LaufV_Stunden] <=15 and station_data['value'][LaufV_Stunden] >10:
                Zeile=6
            elif station_data['value'][LaufV_Stunden] <=20 and station_data['value'][LaufV_Stunden] >15:
                Zeile=7
                #Here is a difference
            elif station_data['value'][LaufV_Stunden] <=25 and station_data['value'][LaufV_Stunden] >20:
                Zeile=8
            else:
                Zeile=9


            #Tagessumme h
                #If LaufV < 8760 - 24 Then
            h_sum=0
            LaufV= LaufV_Stunden 
            j=0
            while j<24 and LaufV<station_data.shape[0]:
                h_sum=h_sum + h[LaufV]
                LaufV=LaufV+1
                j+=1
            #print(h_sum)
            #Auswahl des richtigen Stundenfaktors

            #print()
            if station_data['date'][LaufV_Stunden].weekday()==0 :
                F=F_Montag[Zeile] [i]
            elif station_data['date'][LaufV_Stunden].weekday()== 1 :
                    F = F_Dienstag[Zeile] [i]
            elif station_data['date'][LaufV_Stunden].weekday() == 2 :
                    F = F_Mittwoch[Zeile] [i]
            elif station_data['date'][LaufV_Stunden].weekday() == 3:
                    F = F_Donnerstag[Zeile] [i]
            elif station_data['date'][LaufV_Stunden].weekday() == 4:
                    F = F_Freitag[Zeile] [i]
            elif station_data['date'][LaufV_Stunden].weekday() == 5 :
                    F = F_Samstag[Zeile] [i]
            else:
                F = F_Sonntag[Zeile] [i]

            try:
                #print(h_average)
                Q.append( h_sum * (Q_average / h_average) * F * W_Tag[station_data['date'][LaufV_Stunden].weekday()])
            except ZeroDivisionError:
                z = 0

           
            LaufV_Stunden = LaufV_Stunden + 1
            i=i+1
        
#Berechnung des approximierten Jahreswärmebedarfs
Q_sum=0

for i in range (0,station_data.shape[0]):
    Q_sum=Q_sum+Q[i]
    

# Korrektur des Wärmebedarfs, Berechnung des WW-Anteils 
Q_WW=[]
Q_input=Warmebedarf
for i in range(0,station_data.shape[0]):

   
    Q[i]=Q[i]*(Q_input/Q_sum)
    #print( Q[i])
    Q_WW.append(D*(Q[i]/h[i]))

print(Q)
#print(len(Q))