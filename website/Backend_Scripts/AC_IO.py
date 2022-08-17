from flask import redirect, request, jsonify
import pandas as pd
import numpy as np
import math

AC_csv = pd.read_csv('website/static/AC_Data//AC_Cost_Data.csv')


def rep_input(inp, ans=None, int_only=False, rep=False, nns=False):
    if rep and ans and nns:
        print(f'Please input one of the valid answers : {ans}')
    elif rep and ans and not nns:
        print(f'Please input one of the valid answers : {ans + ["not sure"]}')
    elif rep and int_only:
        print(f'Please input an integer.')
    res = input(inp).lower()
    if int_only:
        try:
            return float(res)
        except ValueError:
            return res if res == 'not sure' and nns == False else rep_input(inp, int_only=True, rep=True)
    return res if not ans and not int_only else res if res in [x.lower() for x in ans if isinstance(x, str)] + [
        'not sure'] and not nns else res if res in [x.lower() for x in ans if isinstance(x, str)] else rep_input(inp,
                                                                                                                 ans=ans,
                                                                                                                 rep=True,
                                                                                                                 nns=nns)


def inp_conversion(val, conversion, l_bound=None, u_bound=None):
    if val == 'not sure':
        return False
    if l_bound and u_bound:
        if val > u_bound or val < l_bound:
            i = rep_input(
                'Your value was deemed unreasonablyt high or low by the system. This failsafe was put in place '
                'to minimize the risk of entering a mistaken value and skewing the results. Input "y" to move'
                'on to the next question, input "n" to use this value anyway: ', ans=['y', 'n'], nns=True)
            return val * conversion if i == 'n' else False
    return val * conversion


def KwH_Ques():
    BTU = rep_input("Enter the BTU of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if inp_conversion(BTU, 1 / 12000, 1000, 80000):
        return [inp_conversion(BTU, 1 / 12000), None]
    watts = rep_input("Enter the wattage of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if inp_conversion(watts, 1 / 1000, 83, 6667):
        return [inp_conversion(watts, 1 / 1000), None]
    est_df = pd.DataFrame(AC_csv.loc[(AC_csv['Type'] == rep_input(
        "Enter the type (central, window unit, mini split) of air conditioner you have (not skippable): ",
        ans=['central', 'window unit', 'mini_split'], nns=True)) & (AC_csv['Size'] == rep_input(
        "Enter the size (small, medium, large) of your air conditioner (not skippable): ",
        ans=['small', 'medium', 'large'], nns=True)), ['KwhPH', 'GOT']])
    return est_df.values.flatten()


def inp_csv_loc(csv, date, rep=False):
    if rep:
        print("Make sure the city you entered is 1) a city (not a county/state) and 2) doesn't contain spelling errors")
    city = rep_input("What is the nearest major city to you (preferably >100 miles): ", nns=True)
    filt = (csv['Station.City'] == city) & (csv['Date.Month'] == int(date))
    res = csv.loc[filt, ['Data.Temperature.Avg Temp', 'Data.Temperature.Max Temp']]
    if res.empty:
        return inp_csv_loc(csv, date, rep=True)
    return res


def Price_Ques(kwh, tense, rdeg=False):
    tense_dict = {'present': ['was', 'today', 'did'], 'past': ['is', 'most days', 'do']}
    t1, t2, t3 = tense_dict[tense]
    EER = rep_input(
        "What is the EER (energy efficiency ratio) of your air conditioner : format w/ 1 decminal point ('not sure' "
        "if you don't know): ", ans=[str(n / 2) for n in range(12, 25)])
    if EER == 'not sure':
        EER = '8.5'
    hours = rep_input(f'How many hours {t1} your air conditioner on {t2}? ', int_only=True, nns=True)
    temp = rep_input(f'What temperature {t3} you set your air conditioner to (F)? ', int_only=True, nns=True)
    state = rep_input(f'What state do you live in? ', ans=list(AC_csv['State'].values.flatten()), nns=True)
    use_csv = rep_input("Would you like to use average temperature data for your area (recommended unless there is "
                        "abnormally high or low weather conditions at the moment in your area) (y/n): ", ans=['y', 'n'],
                        nns=True)
    W_csv = pd.read_csv('AC data/WBC.csv')
    W_csv['Station.City'] = W_csv['Station.City'].str.lower()
    if use_csv == 'y':
        date = rep_input("What month of the year is it (enter a number)? ", ans=[str(n + 1) for n in range(12)],
                         nns=True)
        avg_max = inp_csv_loc(W_csv, date)
        avgs = [avg_max['Data.Temperature.Avg Temp'].mean(), avg_max['Data.Temperature.Max Temp'].mean()]
        avg = (avgs[0] + (avgs[1] * 5)) / 6
    elif use_csv == 'n':
        avgs = [rep_input('What was the average temperature today? ', int_only=True, nns=True),
                rep_input('What was the high temperature today? ', int_only=True, nns=True)]
        avg = ((avgs[0] + (avgs[1] * 5))) / 6
    AC_csv['State'] = AC_csv['State'].str.lower()
    res = hours * float(AC_csv.loc[AC_csv['Dchange'] == int(avg - temp), 'Dmult']) * float(
        AC_csv.loc[AC_csv['State'] == state, 'CostKwh']) * float(
        AC_csv.loc[AC_csv['EER'] == float(EER), 'Emult']) * float(kwh) / 100
    if rdeg:
        return [res, hours, avg - temp, avg]
    return res


def inp_sugg_temp(cost, hours, Dchange, avg):
    goal = (round(float(rep_input('What is your AC budget (monthly)? ', int_only=True, nns=True)), 2) / (cost * 30))
    priority = rep_input(
        'What would you NOT like to change ("hours" of AC, AC "temp", or "both" are of equal importance)? ',
        ans=['hours', 'temp', 'both'], nns=True)

    return [False, False, avg] if goal > 1 else [math.floor((goal * hours) * 100) / 100, Dchange,
                                                 avg] if priority == 'temp' else [hours, abs((np.log(
        AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * goal) / np.log(1.04)) + 7),
                                                                                  avg] if priority == 'hours' else [
        math.floor((round(math.sqrt(goal), 5) * hours) * 100) / 100, abs((np.log(
            AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * round(math.sqrt(goal),
                                                                                                      5)) / np.log(
            1.04)) + 7), avg] if priority == 'both' else ['Error', 'Error', avg]


# ---[SEND TO SERVER]---


def send(ques, val_ans, int_only, ns, err_msg, mc):
    request()


def Qreq(ques, val_ans=None, int_only=False, ns=False, err_msg=None, mc=False):
    if not ns:
        val_ans = val_ans + ['not sure']
    res = send(ques, val_ans, int_only, err_msg, ns, mc)
    if int_only:
        try:
            return float(res)
        except ValueError:
            return res if res == 'not sure' and ns == False else Qreq(ques, int_only=True,
                                                                      err_msg='Please input an number.')
    return res if mc else res if not val_ans and not int_only else res if res in [x.lower() for x in
                                                                                  val_ans if isinstance(x, str)] + [
                                                                              'not sure'] and not ns else res if res in [
        x.lower() for x in val_ans if isinstance(x, str)] else Qreq(ques, val_ans, ns=ns,
                                                                    err_msg=f'Please input a valid answer : {val_ans}')


def conversion(val, conversion, l_bound=None, u_bound=None):
    if val == 'not sure':
        return False
    if l_bound and u_bound:
        if val > u_bound or val < l_bound:
            i = Qreq(
                f'Your value of {val} was deemed unreasonably high or low by the system. This failsafe was put in place '
                'to minimize the risk of entering a mistaken value and skewing the results.',
                val_ans=['Yes, use this value', 'No, give the next question'], ns=True, mc=True)
            return val * conversion if i == 'n' else False
    return val * conversion


def KwH():
    BTU = Qreq("Enter the BTU of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if conversion(BTU, 1 / 12000, 1000, 80000):
        return [conversion(BTU, 1 / 12000), None]
    watts = Qreq("Enter the wattage of your air conditioner ('not sure' if you don't know): ", int_only=True)
    if conversion(watts, 1 / 1000, 83, 6667):
        return [conversion(watts, 1 / 1000), None]
    est_df = pd.DataFrame(AC_csv.loc[(AC_csv['Type'] == Qreq(
        "Enter the type (central, window unit, mini split) of air conditioner you have (not skippable): ",
        ans=['central', 'window unit', 'mini_split'], ns=True, mc=True)) & (AC_csv['Size'] == Qreq(
        "Enter the size (small, medium, large) of your air conditioner (not skippable): ",
        ans=['small', 'medium', 'large'], ns=True, mc=True)), ['KwhPH', 'GOT']])
    return est_df.values.flatten()


def csv_loc(csv, date, err=None):
    city = Qreq("What is the nearest major city to you (preferably >100 miles): ", ns=True, err_msg=err)
    filt = (csv['Station.City'] == city) & (csv['Date.Month'] == int(date))
    res = csv.loc[filt, ['Data.Temperature.Avg Temp', 'Data.Temperature.Max Temp']]
    if res.empty:
        return csv_loc(csv, date, err="Make sure the city you entered is 1) a city (not a county/state) and 2) "
                                      "doesn't contain spelling errors")
    return res


def Price(kwh, tense, rdeg=False):
    tense_dict = {'present': ['was', 'today', 'did'], 'past': ['is', 'most days', 'do']}
    t1, t2, t3 = tense_dict[tense]
    EER = Qreq(
        "What is the EER (energy efficiency ratio) of your air conditioner : format w/ 1 decminal point ('not sure' "
        "if you don't know): ", val_ans=[str(n / 2) for n in range(12, 25)], mc=True)
    if EER == 'not sure':
        EER = '8.5'
    hours = Qreq(f'How many hours {t1} your air conditioner on {t2}? ', int_only=True, ns=True)
    temp = Qreq(f'What temperature {t3} you set your air conditioner to (F)? ', int_only=True, ns=True)
    state = Qreq(f'What state do you live in? ', ans=list(AC_csv['State'].values.flatten()), ns=True, mc=True)
    use_csv = Qreq("Would you like to use average temperature data for your area (recommended unless there is "
                   "abnormally high or low weather conditions at the moment in your area) (y/n): ", ans=['yes', 'no'],
                   ns=True, mc=True)
    W_csv = pd.read_csv('AC data/WBC.csv')
    W_csv['Station.City'] = W_csv['Station.City'].str.lower()
    if use_csv == 'y':
        date = Qreq("What month of the year is it (enter a number)? ", val_ans=[str(n + 1) for n in range(12)],
                    ns=True, mc=True)
        avg_max = csv_loc(W_csv, date)
        avgs = [avg_max['Data.Temperature.Avg Temp'].mean(), avg_max['Data.Temperature.Max Temp'].mean()]
        avg = (avgs[0] + (avgs[1] * 5)) / 6
    elif use_csv == 'n':
        avgs = [Qreq('What was the average temperature today? ', int_only=True, ns=True),
                Qreq('What was the high temperature today? ', int_only=True, ns=True)]
        avg = ((avgs[0] + (avgs[1] * 5))) / 6
    AC_csv['State'] = AC_csv['State'].str.lower()
    res = hours * float(AC_csv.loc[AC_csv['Dchange'] == int(avg - temp), 'Dmult']) * float(
        AC_csv.loc[AC_csv['State'] == state, 'CostKwh']) * float(
        AC_csv.loc[AC_csv['EER'] == float(EER), 'Emult']) * float(kwh) / 100
    if rdeg:
        return [res, hours, temp, avg]
    return res


def sugg_temp(cost, hours, Dchange, avg):
    goal = (round(float(Qreq('What is your AC budget (monthly)? ', int_only=True, ns=True)), 2) / (cost * 30))
    priority = Qreq(
        'What would you NOT like to change ("hours" of AC, AC "temp", or "both" are of equal importance)? ',
        val_ans=['hours', 'temp', 'both'], ns=True, mc=True)

    return [False, False, avg] if goal > 1 else [math.floor((goal * hours) * 100) / 100, Dchange,
                                                 avg] if priority == 'temp' else [hours, abs((np.log(
        AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * goal) / np.log(1.04)) + 7),
                                                                                  avg] if priority == 'hours' else [
        math.floor((round(math.sqrt(goal), 5) * hours) * 100) / 100, abs((np.log(
            AC_csv.loc[AC_csv['Dchange'] == math.floor(Dchange), 'Dmult'].values.flatten()[0] * round(math.sqrt(goal),
                                                                                                      5)) / np.log(
            1.04)) + 7), avg] if priority == 'both' else ['Error', 'Error', avg]


# ---[MAIN]---


if __name__ == '__main__':
    kwhph = KwH_Ques()
    if kwhph[1]:
        print(f'Your air conditioner spends {kwhph[0]} kWh hourly, give or take {kwhph[1]} kWh.')
    if not kwhph[1]:
        print(f'Your air conditioner spends aproximatley {kwhph[0]} kWh hourly.')
    p = Price_Ques(kwhph[0], 'present', rdeg=True)
    print(f"You spent aproximatley \n${round(p[0], 2)}\n today on air conditioning.")
    sugg = inp_sugg_temp(p[0], p[1], p[2], p[3])
    print(f"You should put your thermostat at {math.floor(sugg[2] - sugg[1])} degrees for {round(sugg[0], 2)} hours.")
