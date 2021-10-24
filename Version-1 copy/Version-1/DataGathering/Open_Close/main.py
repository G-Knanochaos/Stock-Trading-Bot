import pandas as pd
import json
import numpy as np
import yfinance as yf
import datetime
import time

BLACKLIST = ['IBTB','FDM']

if input('Override Close Wait?') == 'n':
  print("Waiting for market close...")
  while True:
    now = datetime.datetime.now()
    current_time = int(now.strftime("%H%M"))
    print(current_time)
    if current_time >= 1300 and current_time <= 1500:
      print('Start time: {}'.format(current_time))
      break
    time.sleep(60)
  print("Market has closed. Beginning program...")

f = open('/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/json/stocks.json')
data = json.load(f)
lst = []
for obj in data:
    lst.append([obj['Ticker'],
                obj['Strength'],
                obj['Trend'][0],
                obj['Open Close Average']])
for obj in lst:
    ticker = yf.Ticker(obj[0])
    df = ticker.history(period='1d', interval = '1d')
    Open = df['Open'][0]
    Close = df['Close'][0]
    pDiff = (Close/Open)-1
    obj.append(pDiff)
    print("Percent difference: {}, Ticker: {}".format(pDiff,obj[0]))
_columns = ['Ticker', 'Strength','Trend', 'OC_Average', 'Actual_Increase']

df = pd.DataFrame(data=lst,columns = _columns)

file = "/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Open_Close/Trainers/data.csv"
p_df = pd.read_csv(file)
frames = pd.concat([df,p_df], ignore_index = True)
#if input("Update file? (y/n)") == 'n':
    #quit()
frames.to_csv(file, mode='w',sep=';')

