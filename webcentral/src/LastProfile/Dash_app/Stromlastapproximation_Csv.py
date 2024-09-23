# Stromlastapproximation über Standardlastprofile (NRW)
import os
import math
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = os.path.join(PATH, "Strom_Approximation.csv")


def currentApproximation(application: int, powerRequirement: int):
    df = pd.read_csv(DATA_PATH)
    try:
        sum_value = float(df["Summe"][application + 1])
    except (KeyError, IndexError, ValueError):
        sum_value = 0


    loadGear = []
    for i in range(3, 8763):
        try:
            loadGear.append(
                float(df.iloc[i, application]) * (powerRequirement / sum_value)
            )
        except (KeyError, IndexError, ValueError):
            loadGear.append(0)


    sum_loadGear = math.fsum(loadGear)
    loadGear2 = []
    for value in loadGear:
        loadGear2.append(value * (powerRequirement / sum_loadGear))


    return loadGear2
