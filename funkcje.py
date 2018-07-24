import pandas as pd
import numpy as np


def columns(df):

    # New lap column

    x = [1]
    for i in range(1, len(df)):
        if df['lapTime'][i] <= df['lapTime'][i - 1]:
            x.append(1)
        else:
            x.append(0)
    df['newLap'] = pd.Series(x)

    # Rotate change

    g = 7
    x = [0.] * g
    for i in range(g, len(df)):
        x.append(abs(df['m_xr'][i] - df['m_xr'][i - g]))
    df['rotateChange'] = pd.Series(x)

    # Speed change with break sum

    g = 10
    x = [0.] * g
    y = []
    suma = 0
    for i in range(g):
        suma += df['brake'][i]
        y.append(suma)
    for i in range(g, len(df)):
        suma += df['brake'][i]
        suma -= df['brake'][i - g]
        x.append(df['speed'][i] - df['speed'][i - g])
        y.append(suma)
    df['speedChange'] = pd.Series(x)
    df['brakeSum'] = pd.Series(y)

    # Backward

    x = []
    for i in range(len(df) - 1):
        if df['totalDistance'][i + 1] < df['totalDistance'][i]:
            x.append(1)
        else:
            x.append(0)
    x.append(0)
    df['back'] = pd.Series(x)

    # Wheels position differences

    df['frontDifference'] = abs(df['m_susp_pos_fl'] - df['m_susp_pos_fr'])
    df['rearDifference'] = abs(df['m_susp_pos_rl'] - df['m_susp_pos_rr'])

    return df
