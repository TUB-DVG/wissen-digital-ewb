#Stromlastapproximation über Standardlastprofile (NRW)

import pathlib
import os.path 


PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Strom_Approximation.csv') 

def Stromapproximation(application:int,power_requirement:int):
    import pandas as pd
    import math
    df = pd.read_csv(DATA_PATH)
    try:    
        Summe=float(df['Summe'][application+1])
    except:
        Summe =0

    #print(Summe)
    #print(df['Strom_Standardlastprofil']['Summe'])
    lastgang=[]
    #print(df.iloc[:,Anwendung])
    for i in range(3,8763):
        try:
            lastgang.append(float(df.iloc[:,application][i]) *(power_requirement/Summe))
            
        except:
            lastgang.append(0)
    sum=math.fsum(lastgang)
    lastgang2=[]
    for i in range (0, len(lastgang)):
        lastgang2.append( lastgang[i]*(power_requirement/sum))

    return lastgang2


