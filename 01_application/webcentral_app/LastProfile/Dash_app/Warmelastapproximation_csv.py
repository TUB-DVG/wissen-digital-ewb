import pathlib
import os.path 
from tracemalloc import start
import pandas as pd
from wetterdienst.provider.dwd.observation import DwdObservationRequest
import math
import plotly.graph_objects as go


from typing import Tuple

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Wärme_Strom.csv') 

# That type of type check only works with python 3.9+ 
def warmelast(Application:int,heat_demand:int,Station:int,start_date:str,end_date:str)-> Tuple[int, pd.DataFrame,pd.DataFrame]:


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
    station_data = data.values.all().df



    #Input from the server is Im Kelvin converted to celsius
    station_data['value']=station_data['value'].apply(lambda x: x - 273.15)


    
    # Fill in the missing entries in the wetterdient data and mark them
    Fehlende_werte=0
    station_data['fehlend'] = 'False'
    for i in range (0,len(station_data.index)):
        if math.isnan(station_data['value'][i]):
            Fehlende_werte+=1
            station_data['value'][i]=station_data['value'][i-24]
            station_data['fehlend'][i]='True'

    # Prepare csv file to read factors
    df_warme = pd.read_csv(DATA_PATH)

    #Load regression coefficients
    A=float(df_warme.iloc[:,9][Application+4])
    B=float(df_warme.iloc[:,10][Application+4])
    C=float(df_warme.iloc[:,11][Application+4])
    D=float(df_warme.iloc[:,12][Application+4])

    #Load weekday factors
    W_Tag=[]
    ##Montag
    W_Tag.append(float(df_warme.iloc[:,9][Application+23]))
    ##Dienstag
    W_Tag.append(float(df_warme.iloc[:,10][Application+23]))
    ## Mittwoch
    W_Tag.append(float(df_warme.iloc[:,11][Application+23]))
    ##Donnerstag
    W_Tag.append(float(df_warme.iloc[:,12][Application+23]))
    ##Freitag
    W_Tag.append(float(df_warme.iloc[:,13][Application+23]))
    ##Samstag
    W_Tag.append(float(df_warme.iloc[:,14][Application+23]))
    ##Sonntag
    W_Tag.append(float(df_warme.iloc[:,15][Application+23]))
    #print(W_Tag)

    #Calculation of h
    h=[]
    for i in range(0,station_data.shape[0]):
        T_average=0
        LaufV = i 
        j=0
   
        while j<24 and LaufV <station_data.shape[0] :
            T_moment=float(station_data['value'][LaufV])
            T_average=T_average+T_moment/24
            LaufV=LaufV+1
            j+=1

        
        h.append(round( A / (1 + (B / (T_average - 40)) ** C) + D,14))

    #Load hour factors
    Zeile_Anfang=Application*13 -24

    #Load hour factors for Mondays
    Column=18
    F_Montag = [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Montag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]


    #Load hour factors for Tuesdays
    Column=44
    F_Dienstag = [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Dienstag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]

    #Load hour factors for Wednesdays

    Column=70
    F_Mittwoch = [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Mittwoch[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]

    #Load hour factors for Thursdays
    Column=96
    F_Donnerstag = [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Donnerstag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]

    #Load hour factors for Fridays
    Column=122
    F_Freitag= [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Freitag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]


    #Load hour factors for Saturdays
    Column=148
    F_Samstag= [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Samstag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]

    #Load hour factors for Sundays
    Column=174
    F_Sonntag= [[0 for x in range(24)] for y in range(10)] 
    for i in range(0,24):
        for j in range(0,10):
            F_Sonntag[j][i]=df_warme.iloc[:,Column+i][Zeile_Anfang+j]




    # Calculation of the hourly heat demand
    Q_average=heat_demand
    Q=[]
    #LaufV = 0
    #k = 0

    # Calculate mean h
    h_average = 0
    for i in range(0,station_data.shape[0]):
        h_average=h_average+h[i]

    h_average = h_average / (station_data.shape[0])

    i=0
    for k in range (0,station_data.shape[0]):
                # Reset hours after 24 hours
                if i == 24 :
                    i=0
          
                #Selection of the line depending on the outside temperature
                if station_data['value'][k] <=-15:
                    Zeile=0
                elif station_data['value'][k] <=-10 and station_data['value'][k] >-15:
                    Zeile=1
                elif station_data['value'][k] <=-5 and station_data['value'][k] >-10:
                    Zeile=2
                elif station_data['value'][k] <=0 and station_data['value'][k] >-5:
                    Zeile=3
                elif station_data['value'][k] <=5 and station_data['value'][k] >0:
                    Zeile=4
                elif station_data['value'][k] <=10 and station_data['value'][k] >5:
                    Zeile=5
                elif station_data['value'][k] <=15 and station_data['value'][k] >10:
                    Zeile=6
                elif station_data['value'][k] <=20 and station_data['value'][k] >15:
                    Zeile=7
                    #Here is a difference
                elif station_data['value'][k] <=25 and station_data['value'][k] >20:
                    Zeile=8
                else:
                    Zeile=9

                #Tagessumme h
                h_sum=0
                LaufV= k 
                j=0
                while j<24 and LaufV<station_data.shape[0]:
                    h_sum=h_sum + h[LaufV]
                    LaufV=LaufV+1
                    j+=1
                #Selecting the right hour factor
                if station_data['date'][k].weekday() ==0 :
                    F=F_Montag[Zeile] [i]
                elif station_data['date'][k].weekday() == 1 :
                        F = F_Dienstag[Zeile] [i]
                elif station_data['date'][k].weekday() == 2 :
                        F = F_Mittwoch[Zeile] [i]
                elif station_data['date'][k].weekday() == 3:
                        F = F_Donnerstag[Zeile] [i]
                elif station_data['date'][k].weekday() == 4:
                        F = F_Freitag[Zeile] [i]
                elif station_data['date'][k].weekday() == 5 :
                        F = F_Samstag[Zeile] [i]
                else:
                    F = F_Sonntag[Zeile] [i]
                try:
                   
                    Q.append( h_sum * (Q_average / h_average) * F * W_Tag[station_data['date'][k].weekday()])
                except ZeroDivisionError:
                    z = 0
              
                #Increment hours
                i=i+1
                
    #Calculation of the approximate annual heat requirement
    Q_sum=0
    for i in range (0,station_data.shape[0]):
        Q_sum=Q_sum+Q[i]
        

    # Correction of the heat requirement, calculation of the WW_share
    Q_WW=[]
    Q_input=heat_demand
    for i in range(0,station_data.shape[0]):
    
        Q[i]=Q[i]*(Q_input/Q_sum)
     
        Q_WW.append(D*(Q[i]/h[i]))

    start=station_data.index[station_data.date == pd.Timestamp(start_date+" 00:00:00+00:00")].tolist()[0]
    end=station_data.index[station_data.date == pd.Timestamp(end_date+" 23:00:00+00:00")].tolist()[0] +1

    heat_approximation_df = pd.DataFrame({'Last':Q[start:end],'Time':station_data['date'][start:end],'fehlend':station_data['fehlend'][start:end]})
    WW_heat_approximation=pd.DataFrame({'Last':Q_WW[start:end],'Time':station_data['date'][start:end],'fehlend':station_data['fehlend'][start:end]})
    
  

    return Fehlende_werte,heat_approximation_df,WW_heat_approximation



