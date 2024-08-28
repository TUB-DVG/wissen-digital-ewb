import math
import pathlib
import os.path
import pandas as pd
from typing import Tuple
import datetime
from wetterdienst.provider.dwd.observation import DwdObservationRequest

PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = os.path.join(PATH, "Wärme_Strom.csv")
TRY_PATH = os.path.join(PATH, "TRY2015_524124130664_Jahr.csv")


def heatLoad(
    application: int,
    heatDemand: int,
    station: int,
    startDate: str,
    endDate: str,
    referenceYear: str,
) -> Tuple[int, pd.DataFrame, pd.DataFrame]:
    if referenceYear == "off":
        # ToDo check with Firas why this parameter is "on", when
        # Setting up the resolution for data filtering
        RESOLUTION = "HOURLY"
        # Parameter variable selection
        PARAMETER = "TEMPERATURE_AIR_MEAN_200"
        # Setting up the Period
        PERIOD = "RECENT"
        # Acquiring all the stations that provide data according to selected filters
        stations = DwdObservationRequest(
            parameter=PARAMETER, resolution=RESOLUTION, period=PERIOD
        )
        data = stations.filter_by_station_id(station_id=station)
        stationData = data.values.all().df

        # Input from the server is Im Kelvin converted to celsius
        stationData["value"] = stationData["value"].apply(lambda x: x - 273.15)
    else:
        stationData = pd.read_csv(TRY_PATH)
        stationData["date"] = pd.to_datetime(
            stationData[["YEAR", "MONTH", "DAY", "HOUR"]],
            format="%Y-%m-%d %H",
            utc=True,
        )
    # Fill in the missing entries in the wetterdient data and mark them
    missingValues = 0
    stationData["fehlend"] = "False"
    for i in range(0, len(stationData.index)):
        if math.isnan(stationData["value"][i]):
            missingValues += 1
            stationData["value"][i] = stationData["value"][i - 24]
            stationData["fehlend"][i] = "True"
    # Prepare csv file to read factors
    dfHeat = pd.read_csv(DATA_PATH)

    # Load regression coefficients
    A = float(dfHeat.iloc[:, 9][application + 4])
    B = float(dfHeat.iloc[:, 10][application + 4])
    C = float(dfHeat.iloc[:, 11][application + 4])
    D = float(dfHeat.iloc[:, 12][application + 4])

    # Load weekday factors
    weekDay = []
    ##Montag
    weekDay.append(float(dfHeat.iloc[:, 9][application + 23]))
    ##Dienstag
    weekDay.append(float(dfHeat.iloc[:, 10][application + 23]))
    ## Mittwoch
    weekDay.append(float(dfHeat.iloc[:, 11][application + 23]))
    ##Donnerstag
    weekDay.append(float(dfHeat.iloc[:, 12][application + 23]))
    ##Freitag
    weekDay.append(float(dfHeat.iloc[:, 13][application + 23]))
    ##Samstag
    weekDay.append(float(dfHeat.iloc[:, 14][application + 23]))
    ##Sonntag
    weekDay.append(float(dfHeat.iloc[:, 15][application + 23]))

    # Calculation of h
    h = []
    for i in range(0, stationData.shape[0]):
        tAverage = 0
        runV = i
        j = 0

        while j < 24 and runV < stationData.shape[0]:
            tMoment = float(stationData["value"][runV])
            tAverage = tAverage + tMoment / 24
            runV = runV + 1
            j += 1

        h.append(round(A / (1 + (B / (tAverage - 40)) ** C) + D, 14))

    # Load hour factors
    lineStart = application * 13 - 24

    # Load hour factors for Mondays
    column = 18
    factorMonday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorMonday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Tuesdays
    column = 44
    factorTuesday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorTuesday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Wednesdays
    column = 70
    factorWednesday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorWednesday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Thursdays
    column = 96
    factorThursday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorThursday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Fridays
    column = 122
    factorFriday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorFriday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Saturdays
    column = 148
    factorSaturday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorSaturday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Sundays
    column = 174
    factorSunday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorSunday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Calculation of the hourly heat demand
    Q_average = heatDemand
    Q = []

    # Calculate mean h
    h_average = 0
    for i in range(0, stationData.shape[0]):
        h_average = h_average + h[i]

    h_average = h_average / (stationData.shape[0])

    i = 0
    for k in range(0, stationData.shape[0]):
        # Reset hours after 24 hours
        if i == 24:
            i = 0
        # Selection of the line depending on the outside temperature
        if stationData["value"][k] <= -15:
            line = 0
        elif stationData["value"][k] <= -10 and stationData["value"][k] > -15:
            line = 1
        elif stationData["value"][k] <= -5 and stationData["value"][k] > -10:
            line = 2
        elif stationData["value"][k] <= 0 and stationData["value"][k] > -5:
            line = 3
        elif stationData["value"][k] <= 5 and stationData["value"][k] > 0:
            line = 4
        elif stationData["value"][k] <= 10 and stationData["value"][k] > 5:
            line = 5
        elif stationData["value"][k] <= 15 and stationData["value"][k] > 10:
            line = 6
        elif stationData["value"][k] <= 20 and stationData["value"][k] > 15:
            line = 7
            # Here is a difference
        elif stationData["value"][k] <= 25 and stationData["value"][k] > 20:
            line = 8
        else:
            line = 9
        # Tagessumme h
        h_sum = 0
        runV = k
        j = 0
        while j < 24 and runV < stationData.shape[0]:
            h_sum = h_sum + h[runV]
            runV = runV + 1
            j += 1
        # Selecting the right hour factor
        if stationData["date"][k].weekday() == 0:
            F = factorMonday[line][i]
        elif stationData["date"][k].weekday() == 1:
            F = factorTuesday[line][i]
        elif stationData["date"][k].weekday() == 2:
            F = factorWednesday[line][i]
        elif stationData["date"][k].weekday() == 3:
            F = factorThursday[line][i]
        elif stationData["date"][k].weekday() == 4:
            F = factorFriday[line][i]
        elif stationData["date"][k].weekday() == 5:
            F = factorSaturday[line][i]
        else:
            F = factorSunday[line][i]
        try:

            Q.append(
                h_sum
                * (Q_average / h_average)
                * F
                * weekDay[stationData["date"][k].weekday()]
            )
        except ZeroDivisionError:
            pass
        # Increment hours
        i = i + 1

    # Calculation of the approximate annual heat requirement
    qSum = 0
    for i in range(0, stationData.shape[0]):
        qSum = qSum + Q[i]

    # Correction of the heat requirement, calculation of the WW_share
    qWW = []
    Q_INPUT = heatDemand
    for i in range(0, stationData.shape[0]):
        Q[i] = Q[i] * (Q_INPUT / qSum)
        qWW.append(D * (Q[i] / h[i]))

    # start = pd.Timestamp(startDate + " 01:00:00+00:00")
    # end = pd.Timestamp(endDate + " 23:00:00+00:00")
    # # print(stationData.index[stationData.date == pd.Timestamp(startDate+" 01:00:00+00:00")].tolist())
    # start=stationData.index[stationData.date == pd.Timestamp(startDate+" 01:00:00+00:00")].tolist()[0]
    # end=stationData.index[stationData.date == pd.Timestamp(endDate+" 23:00:00+00:00")].tolist()[0] +1

    print("This ist the end 2", startDate, endDate)
    start = stationData[
        stationData.date == pd.Timestamp(startDate + " 01:00:00+00:00")
    ].index.tolist()[0]
    end = stationData[
        stationData.date == pd.Timestamp(endDate + " 23:00:00+00:00")
    ].index.tolist()[
        0
    ]  # +1
    heatApproximationDf = pd.DataFrame(
        {
            "Time": stationData["date"][start:end],
            "Last": Q[start:end],
            "WW_Last": qWW[start:end],
            "fehlend": stationData["fehlend"][start:end],
        }
    )
    return missingValues, heatApproximationDf


def heatLoadreferenceYear(
    application: int,
    heatDemand: int,
    startDate: str,
    endDate: str,
):
    stationData = pd.read_csv(TRY_PATH)
    stationData["date"] = pd.to_datetime(
        stationData[["YEAR", "MONTH", "DAY", "HOUR"]],
        format="%Y-%m-%d %H",
        utc=True,
    )
    # Fill in the missing entries in the wetterdient data and mark them
    missingValues = 0
    stationData["fehlend"] = "False"
    for i in range(0, len(stationData.index)):
        if math.isnan(stationData["value"][i]):
            missingValues += 1
            stationData["value"][i] = stationData["value"][i - 24]
            stationData["fehlend"][i] = "True"
    # Prepare csv file to read factors
    dfHeat = pd.read_csv(DATA_PATH)

    # Load regression coefficients
    A = float(dfHeat.iloc[:, 9][application + 4])
    B = float(dfHeat.iloc[:, 10][application + 4])
    C = float(dfHeat.iloc[:, 11][application + 4])
    D = float(dfHeat.iloc[:, 12][application + 4])

    # Load weekday factors
    weekDay = []
    ##Montag
    weekDay.append(float(dfHeat.iloc[:, 9][application + 23]))
    ##Dienstag
    weekDay.append(float(dfHeat.iloc[:, 10][application + 23]))
    ## Mittwoch
    weekDay.append(float(dfHeat.iloc[:, 11][application + 23]))
    ##Donnerstag
    weekDay.append(float(dfHeat.iloc[:, 12][application + 23]))
    ##Freitag
    weekDay.append(float(dfHeat.iloc[:, 13][application + 23]))
    ##Samstag
    weekDay.append(float(dfHeat.iloc[:, 14][application + 23]))
    ##Sonntag
    weekDay.append(float(dfHeat.iloc[:, 15][application + 23]))

    # Calculation of h
    h = []
    for i in range(0, stationData.shape[0]):
        tAverage = 0
        runV = i
        j = 0

        while j < 24 and runV < stationData.shape[0]:
            tMoment = float(stationData["value"][runV])
            tAverage = tAverage + tMoment / 24
            runV = runV + 1
            j += 1

        h.append(round(A / (1 + (B / (tAverage - 40)) ** C) + D, 14))

    # Load hour factors
    lineStart = application * 13 - 24

    # Load hour factors for Mondays
    column = 18
    factorMonday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorMonday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Tuesdays
    column = 44
    factorTuesday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorTuesday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Wednesdays
    column = 70
    factorWednesday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorWednesday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Thursdays
    column = 96
    factorThursday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorThursday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Fridays
    column = 122
    factorFriday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorFriday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Saturdays
    column = 148
    factorSaturday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorSaturday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Load hour factors for Sundays
    column = 174
    factorSunday = [[0 for x in range(24)] for y in range(10)]
    for i in range(0, 24):
        for j in range(0, 10):
            factorSunday[j][i] = dfHeat.iloc[:, column + i][lineStart + j]

    # Calculation of the hourly heat demand
    Q_average = heatDemand
    Q = []

    # Calculate mean h
    h_average = 0
    for i in range(0, stationData.shape[0]):
        h_average = h_average + h[i]

    h_average = h_average / (stationData.shape[0])

    i = 0
    for k in range(0, stationData.shape[0]):
        # Reset hours after 24 hours
        if i == 24:
            i = 0
        # Selection of the line depending on the outside temperature
        if stationData["value"][k] <= -15:
            line = 0
        elif stationData["value"][k] <= -10 and stationData["value"][k] > -15:
            line = 1
        elif stationData["value"][k] <= -5 and stationData["value"][k] > -10:
            line = 2
        elif stationData["value"][k] <= 0 and stationData["value"][k] > -5:
            line = 3
        elif stationData["value"][k] <= 5 and stationData["value"][k] > 0:
            line = 4
        elif stationData["value"][k] <= 10 and stationData["value"][k] > 5:
            line = 5
        elif stationData["value"][k] <= 15 and stationData["value"][k] > 10:
            line = 6
        elif stationData["value"][k] <= 20 and stationData["value"][k] > 15:
            line = 7
            # Here is a difference
        elif stationData["value"][k] <= 25 and stationData["value"][k] > 20:
            line = 8
        else:
            line = 9
        # Tagessumme h
        h_sum = 0
        runV = k
        j = 0
        while j < 24 and runV < stationData.shape[0]:
            h_sum = h_sum + h[runV]
            runV = runV + 1
            j += 1
        # Selecting the right hour factor
        if stationData["date"][k].weekday() == 0:
            F = factorMonday[line][i]
        elif stationData["date"][k].weekday() == 1:
            F = factorTuesday[line][i]
        elif stationData["date"][k].weekday() == 2:
            F = factorWednesday[line][i]
        elif stationData["date"][k].weekday() == 3:
            F = factorThursday[line][i]
        elif stationData["date"][k].weekday() == 4:
            F = factorFriday[line][i]
        elif stationData["date"][k].weekday() == 5:
            F = factorSaturday[line][i]
        else:
            F = factorSunday[line][i]
        try:

            Q.append(
                h_sum
                * (Q_average / h_average)
                * F
                * weekDay[stationData["date"][k].weekday()]
            )
        except ZeroDivisionError:
            pass
        # Increment hours
        i = i + 1

    # Calculation of the approximate annual heat requirement
    qSum = 0
    for i in range(0, stationData.shape[0]):
        qSum = qSum + Q[i]

    # Correction of the heat requirement, calculation of the WW_share
    qWW = []
    Q_INPUT = heatDemand
    for i in range(0, stationData.shape[0]):

        Q[i] = Q[i] * (Q_INPUT / qSum)

        qWW.append(D * (Q[i] / h[i]))

    # start = datetime.datetime.strptime("01/01/2021", "%m/%d/%Y")
    # end = datetime.datetime.strptime("12/31/2021", "%m/%d/%Y")

    # start = datetime.datetime(startDate, 0, 0, 1)
    # end = datetime.datetime(endDate + 0, 0, 23)

    start = stationData.index[
        stationData.date == pd.Timestamp(startDate + " 01:00:00+00:00")
    ].tolist()[0]
    end = (
        stationData.index[
            stationData.date == pd.Timestamp(endDate + " 23:00:00+00:00")
        ].tolist()[0]
        + 1
    )

    heatApproximationDf = pd.DataFrame(
        {
            "Time": stationData["date"][start:end],
            "Last": Q[start:end],
            "WW_Last": qWW[start:end],
            "fehlend": stationData["fehlend"][start:end],
        }
    )

    return missingValues, heatApproximationDf
