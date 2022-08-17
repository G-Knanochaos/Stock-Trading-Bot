from flask import request
import pandas as pd
import numpy as np
import math

monthdict = {'January': 1,
             'February': 2,
             'March': 3,
             'April': 4,
             'May': 5,
             'June': 6,
             'July': 7,
             'August': 8,
             'September': 9,
             'October': 10,
             'November': 11,
             'December': 12}


def input_request(ques):
    if request.form.get(ques) and request.form.get != '':
        try:
            return int(request.form.get(ques))
        except:
            return request.form.get(ques)
    return None


def conversion(val, conversion):
    if not val or val == '':
        return False
    return val * conversion


def KwH(BTU, watts, type, size):
    AC_csv = pd.read_csv('website/static/AC_Data/AC_Cost_Data.csv')
    if conversion(BTU, 1 / 12000):
        return [conversion(BTU, 1 / 12000), None]
    if conversion(watts, 1 / 1000):
        return [conversion(watts, 1 / 1000), None]
    return AC_csv.loc[(AC_csv['Type'] == type) & (AC_csv['Size'] == size), ['KwhPH', 'GOT']].values.flatten()


def csv_loc(csv, month, city, err=None):
    res = csv.loc[(csv['Station.City'] == city) & (csv['Date.Month'] == monthdict[month]), ['Data.Temperature.Avg Temp',
                                                                                            'Data.Temperature.Max Temp']]
    if res.empty:
        return csv_loc(csv, monthdict[month], city,
                       err="Make sure the city you entered is 1) a city (not a county/state) and 2) "
                           "doesn't contain spelling errors")
    return res


def Price(kwh, EER, hours, temp, state, city, month, avg_, high, save):
    with open('website/static/AC_Data/AC_Cost_Data.csv', 'rb') as ACV:
        with open('website/static/AC_Data/WBC.csv', 'rb') as WV:
            AC_csv = pd.read_csv(ACV)
            W_csv = pd.read_csv(WV)
            W_csv['Station.City'] = W_csv['Station.City'].str.lower()
            avgs = [avg_, high]
            avg = ((avgs[0] + (avgs[1] * 5))) / 6
            AC_csv['State'] = AC_csv['State'].str.lower()
            res = float(hours) * float(
                AC_csv.loc[AC_csv['Dchange'] == int(avg - temp), 'Dmult'].values.flatten()[0]) * float(
                AC_csv.loc[AC_csv['State'].str.lower() == state.lower(), 'CostKwh'].values.flatten()[0]) * float(
                AC_csv.loc[AC_csv["EER"] == float(EER), "Emult"].values.flatten()[0]) * float(kwh) / 100
    return [round(res, 2), hours, temp, avg]


def sugg_temp(cost, hours, Dchange, avg, target, priority):
    with open('website/static/AC_Data/AC_Cost_Data.csv', 'rb') as ACV:
        AC_csv = pd.read_csv(ACV)
        goal = (target / (cost * 30))
        return [hours, 0, avg] if goal > 1 else [math.floor((goal * hours) * 100) / 100, 0,
                                                     avg] if priority == 'Hours' else [hours, abs((np.log(
            AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * goal) / np.log(
            1.04)) + 7), avg] if priority == 'Temperature' else [
            math.floor((round(math.sqrt(goal), 5) * hours) * 100) / 100, abs((np.log(
                AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * round(
                    math.sqrt(goal),
                    5)) / np.log(
                1.04)) + 7), avg] if priority == 'Both' else ['Error', 'Error', avg]
