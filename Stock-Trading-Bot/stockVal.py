import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates

lines = []
buystrength = 0

def findStockValuation(tickerName):
  global name,ticker,df,s,price
  name = tickerName
  ticker = yfinance.Ticker(name)
  df = ticker.history(interval="1d",period="3mo")
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  daylen = len(df['Date'].tolist())
  s =  np.mean(df['High'] - df['Low'])
  try:
    price = float(get_current_price(ticker))
  except:
    return 0, 0 ,0

  global levels
  levels = []
  for i in range(df.shape[0]-4,df.shape[0]-daylen,-1):
    if isSupport(df,i):
      l = round(df['Low'][i],3)
      if isFarFromLevel(l):
        levels.append([i,l,1])
    elif isResistance(df,i):
      l = round(df['High'][i],3)
      if isFarFromLevel(l):
        levels.append([i,l,1])
        
  if len(levels) > 1:
    while len(levels) > 2:
      levels.remove(min(levels))
    resistance = [(level[1]) for level in levels if level[1] > price]
    support = [(level[1]) for level in levels if level[1] < price]
    try:
      res = resistance[0]
      sup = support[0]
    except:
      return 0, 0, 0
    if price < res and price > sup:
      rDis = res/price - 1
      sDis = sup/price - 1
      potProfit = res/sup
      buyStrength = (rDis+sDis) * potProfit * 100
      print(buyStrength)
      return -buyStrength, res, sup
  return 0, 0, 0
  

def get_current_price(symbol):
  todays_data = symbol.history(period='1d')
  return round(todays_data['Close'][0],3)

def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2] and df['Low'][i+2] < df['Low'][i+3] and df['Low'][i-2] < df['Low'][i-3]
  return support
def isResistance(df,i):
  resistance = df['Low'][i] > df['Low'][i-1]  and df['Low'][i] > df['Low'][i+1] and df['Low'][i+1] > df['Low'][i+2] and df['Low'][i-1] > df['Low'][i-2] and df['Low'][i+2] > df['Low'][i+3] and df['Low'][i-2] > df['Low'][i-3]
  return resistance

def average(lst):
  total = 0
  for l in lst:
    total += l
  return total/len(lst)

def isFarFromLevel(l):
  lst = []
  for x in levels:
    result = abs(l-x[1]) < s
    if result:
      lst.append(result)
    else:
      x[2] += 1
  return np.sum(lst) == 0
