
#Stromlastapproximation über Standardlastprofile (NRW)



def Stromapproximation(application:int,power_requirement:int):
    import pandas as pd
    import math
    df = pd.read_csv('Strom_Approximation.csv')
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


