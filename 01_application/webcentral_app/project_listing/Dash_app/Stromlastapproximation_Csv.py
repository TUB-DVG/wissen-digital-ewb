
"""
#Stromlastapproximation über Standardlastprofile (NRW)


Anwendung=3
Strombedarf = 700000 

# YOU MUST PUT sheet_name=None TO READ ALL CSV FILES IN YOUR XLSM FILE




# prints all sheets
#print(df.keys())
#print(df)
#print(df['Strom_Standardlastprofil'].iloc[:,2])


try:    
    Summe=float(df['Summe'][Anwendung+1])
except:
    Summe =0

#print(Summe)
#print(df['Strom_Standardlastprofil']['Summe'])
lastgang=[]
#print(df.iloc[:,Anwendung])
for i in range(3,8763):
    try:
        lastgang.append(float(df.iloc[:,Anwendung][i]) *(Strombedarf/Summe))
    except:
        lastgang.append(0)
sum=math.fsum(lastgang)
#print(sum)
#print(lastgang[0:5])
lastgang2=[]
for i in range (0, len(lastgang)):
    lastgang2.append( lastgang[i]*(Strombedarf/sum))


#print(lastgang2[0:5])
print(lastgang2)

"""

def Stromapproximation(Anwendung,Strombedarf):
    import pandas as pd
    import math


    df = pd.read_csv('Strom_Approximation.csv')
    try:    
        Summe=float(df['Summe'][Anwendung+1])
    except:
        Summe =0

    #print(Summe)
    #print(df['Strom_Standardlastprofil']['Summe'])
    lastgang=[]
    #print(df.iloc[:,Anwendung])
    for i in range(3,8763):
        try:
            lastgang.append(float(df.iloc[:,Anwendung][i]) *(Strombedarf/Summe))
            
        except:
            lastgang.append(0)
    sum=math.fsum(lastgang)
    lastgang2=[]
    for i in range (0, len(lastgang)):
        lastgang2.append( lastgang[i]*(Strombedarf/sum))

    return lastgang2


