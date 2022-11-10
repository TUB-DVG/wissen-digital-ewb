from tracemalloc import start
import pandas as pd
import wetterdienst
from wetterdienst.provider.dwd.observation import DwdObservationRequest
import plotly.express as px
import math
import plotly.graph_objects as go
def Warmelast(Anwendung,Warmebedarf,Station,start_date,end_date):


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


    data= stations.filter_by_station_id(station_id=Station)

    #station_data = data.values.all().df.tail(8760).reset_index()
    station_data = data.values.all().df
    print(station_data)




    #Eingaben vom Server sind Im Kelvin wurden auf celsius umgeformt
    station_data['value']=station_data['value'].apply(lambda x: x - 273.15)


    Fehlende_werte=station_data['value'].isna().sum()

    #station_data=station_data.dropna().reset_index(drop=True)
    station_data['fehlend'] = 'False'
    for i in range (0,len(station_data.index)):
        if math.isnan(station_data['value'][i]):
            #print(station_data['date'][i])
            station_data['value'][i]=station_data['value'][i-24]
            station_data['fehlend'][i]='True'

    df_warme = pd.read_csv('Warme_Strom.csv')


    #Regressionskoeffizienten laden 
    A=float(df_warme.iloc[:,9][Anwendung+4])
    #print(A)
    #print(A)
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
    #print(W_Tag)

    #
    # print(W_Tag)

    #Berechnung von h
    h=[]
    for i in range(0,8760):
        T_average=0
        LaufV = i 
        j=0
   
        while j<24 and LaufV <8760:

            T_moment=float(station_data['value'][LaufV])
            T_average=T_average+T_moment/24
            LaufV=LaufV+1
            j+=1

        
        h.append(round( A / (1 + (B / (T_average - 40)) ** C) + D,14))
    #print(h)
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

    #print (F_Samstag)


    # Berechnung des stündlichen Wärmebedarfs
    Q_average=Warmebedarf
    Q=[]
    #LaufV = 0
    LaufV_Stunden = 0

    #   #Berechnung mittleres h
    h_average = 0
    for i in range(0,8760):
        h_average=h_average+h[i]

    h_average = h_average / (8760)

    for k in range (1,54): #52 Wochen
        for l in range(0,7):  #7 Tage
            #Auswahl des richtigen Wochentagsfaktor mit l
                #Sicherheitsabfrage: Abbruch der For Schleife nach einem Jahr

            for i in range(0,24): #24 Stunden
                if LaufV_Stunden==8760:
                    break
            
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
                while j<24 and LaufV<8760:
                    h_sum=h_sum + h[LaufV]
                    LaufV=LaufV+1
                    j+=1
                #Auswahl des richtigen Stundenfaktors
                if station_data['date'][LaufV_Stunden].weekday() ==0 :
                    F=F_Montag[Zeile] [i]
                elif station_data['date'][LaufV_Stunden].weekday() == 1 :
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

                #print(h_average)
                try:
                   
                    Q.append( h_sum * (Q_average / h_average) * F * W_Tag[l])
                except ZeroDivisionError:
                    z = 0
            
                LaufV_Stunden = LaufV_Stunden + 1
                
    #Berechnung des approximierten Jahreswärmebedarfs
    Q_sum=0
    #print(Q)
    #print(len(Q))
    for i in range (0,8760):
        Q_sum=Q_sum+Q[i]
        
        #print(Q_sum)

    #print(Q_sum)
    # Korrektur des Wärmebedarfs, Berechnung des WW-Anteils 
    Q_WW=[]
    Q_input=Warmebedarf
    for i in range(0,8760):
    
        Q[i]=Q[i]*(Q_input/Q_sum)
        #print( Q[i])
        Q_WW.append(D*(Q[i]/h[i]))

    start=station_data.index[station_data.date == pd.Timestamp(start_date+" 00:00:00+00:00")].tolist()[0]
    end=station_data.index[station_data.date == pd.Timestamp(end_date+" 23:00:00+00:00")].tolist()[0] +1
    d = {'Last':Q[start:end],'Time':station_data['date'][start:end],'fehlend':station_data['fehlend'][start:end]}
    d=pd.DataFrame(d)

    return Fehlende_werte,d

#   print(Warmelast(2,150000,78,"2021-10-04","2022-10-03"))



