#Stromlastapproximation über Standardlastprofile (NRW)

import pathlib
import os.path 
import pandas as pd
import math

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Strom_Approximation.csv') 

def currentApproximation(application:int,powerRequirement:int):

    df = pd.read_csv(DATA_PATH)
    try:    
        Summe = float(df['Summe'][application+1])
    except:
        Summe = 0
    lastgang = []
    for i in range(3,8763):
        try:
            lastgang.append(float(df.iloc[:,application][i])*(powerRequirement/Summe))
            
        except:
            lastgang.append(0)
    sum = math.fsum(lastgang)
    lastgang2 = []
    for i in range (0, len(lastgang)):
        lastgang2.append( lastgang[i]*(powerRequirement/sum))
    return lastgang2


