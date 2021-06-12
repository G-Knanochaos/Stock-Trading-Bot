import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates

lines = []
buystrength = 0

def findStockValuation(tickerName):
  global name,ticker,df,s,price
  count = 0
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
    return 0, 0 ,0, 0

  global levels
  levels = []
  points = []
  for i in range(df.shape[0]-4,df.shape[0]-daylen,-1):
    count += ((df['High'][i]-df['Low'][i])/price)*100
    if isSupport(df,i,1):
      l = round(df['Low'][i],3)
      points.append(l)
      if isSupport(df,i,2):
        if isSupport(df,i,3):
          if isFarFromLevel(l):
            levels.append([i,l,1])
    elif isResistance(df,i,1):
      l = round(df['High'][i],3)
      points.append(l)
      if isResistance(df,i,2):
        if isResistance(df,i,3):
          if isFarFromLevel(l):
            levels.append([i,l,1])

  #price > points[0] can return True or False
  isUptrend = price > points[0]
  avgDailyVol = round(count/daylen,2)
  if len(levels) > 1:
    while len(levels) > 2:
      levels.remove(min(levels))
    resistance = [(level[1]) for level in levels if level[1] > price]
    support = [(level[1]) for level in levels if level[1] < price]
    try:
      res = resistance[0]
      sup = support[0]
    except:
      return 0, 0, 0, 0
    if price < res and price > sup:
      buyStrength = (((res+sup)/price)-2) * 100
      if isUptrend and buyStrength < 0:
        print("{} eliminated because stock is in up trend".format(name))
        return 0, 0, 0, 0
      elif not isUptrend and buyStrength > 0:
        print("{} eliminated because stock is in down trend".format(name))
        return 0, 0, 0, 0
      print(buyStrength)
      return buyStrength, res, sup, avgDailyVol
  return 0, 0, 0, 0
  

def get_current_price(symbol):
  todays_data = symbol.history(period='1d')
  return round(todays_data['Close'][0],3)

def isSupport(df,i,layers):
  lst = []
  for x in range(1,layers+1):
    lst.append(df['Low'][i-(x-1)] < df['Low'][i-x])
    lst.append(df['Low'][i+(x-1)] < df['Low'][i+x])
  return sum(lst) == layers*2
def isResistance(df,i,layers):
  lst = []
  for x in range(1,layers+1):
    lst.append(df['Low'][i-(x-1)] > df['Low'][i-x])
    lst.append(df['Low'][i+(x-1)] > df['Low'][i+x])
  return sum(lst) == layers*2

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
