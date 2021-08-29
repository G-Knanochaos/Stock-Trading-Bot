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
                obj['Average High to Previous Close'],
                obj['Average Low to Previous Close'],
                obj['Average Daily Volatility'],
                obj['Trend'][0]])
for obj in lst:
    ticker = yf.Ticker(obj[0])
    df = ticker.history(period='5d', interval = '1d')
    Close = df['Close'][3]
    max_index = len(df['High'])-1
    try:
      High, Low = ((df['High'][max_index]/Close)-1)*100, ((df['Low'][max_index]/Close)-1)*100
    except:
      print(ticker)
    obj.extend([High,Low,Close])
    print("High: {}, Low: {}, Close: {}, Ticker: {}".format(High,Low,Close,obj[0]))
_columns = ['Ticker', 'Strength','Average_High', 'Average_Low', 'Average_Volatility', 'Trend', 'Actual_High', 'Actual_Low', 'Previous_Close']

df = pd.DataFrame(data=lst,columns = _columns)

file = "/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/DataGathering/Trainers/data.csv"
#if input("Update file? (y/n)") == 'n':
    #quit()
df.to_csv(file, mode='a',sep=';')

