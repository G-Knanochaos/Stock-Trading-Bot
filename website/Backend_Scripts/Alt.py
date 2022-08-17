import pandas as pd
from .AC_Calc import input_request as inp


def fan_price(state, type, watts, hours):
    AC_csv = pd.read_csv('website/static/AC_Data/AC_Cost_Data.csv')
    filt = (AC_csv['Ftype'].str.lower() == type.lower())
    if not watts:
        watts = AC_csv.loc[filt, 'Fwatts'].values.flatten()
    return round(float(watts) * float(
        AC_csv.loc[AC_csv['State'].str.lower() == state.lower(), 'CostKwh'].values.flatten()[0]) / 1000, 2) * hours
