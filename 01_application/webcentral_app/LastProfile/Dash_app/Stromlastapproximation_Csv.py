#Stromlastapproximation über Standardlastprofile (NRW)
import os 
import math
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Strom_Approximation.csv') 

def currentApproximation(application:int,powerRequirement:int):

    df = pd.read_csv(DATA_PATH)
    try:    
        sum = float(df['Summe'][application+1])
    except:
        sum = 0
    loadGear = []
    for i in range(3,8763):
        try:
            loadGear.append(float(df.iloc[:,application][i])*(powerRequirement/sum))        
        except:
            loadGear.append(0)
    sum = math.fsum(loadGear)
    loadGear2 = []
    for i in range (0, len(loadGear)):
        loadGear2.append( loadGear[i]*(powerRequirement/sum))
    return loadGear2


