import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates
from stockValFunc import *


def findTrend(thickness, df, price):
  daylen = len(df['Date'].tolist())
  go = True
  for i in range(df.shape[0]-thickness-1,df.shape[0]-daylen,-1):
    if isSupport(df,i,thickness,'Close'):
      l = round(df['Close'][i],3)
      point = (i,l)
      break
    elif isResistance(df,i,thickness,'Close'):
      h = round(df['Close'][i],3)
      point = (i,h)
      break
    if isSupport(df,i,thickness,'Low'):
      l = round(df['Low'][i],3)
      point = (i,l)
      break
    elif isResistance(df,i,thickness,'High'):
      h = round(df['High'][i],3)
      point = (i,h)
      break
  rise = ((price/point[1])-1)*100
  run = df.shape[0]-thickness-point[0]
  return rise/run

def fetchData(tickerName):
  ticker = yfinance.Ticker(tickerName)
  df = ticker.history(interval="1d",period="6mo")
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  return df

def findStockValuation(name): #name = stock ticker
  lines = []
  buystrength = 0
  df = fetchData(name)
  daylen = len(df['Date'].tolist())
  s = np.mean(df['High'] - df['Low'])*2

  def isFarFromLevel(l,typ):
    lst = []
    level = 0
    least = 100000
    for x in levels:
      diff = abs(l-x[1])
      result = diff < s
      if result:
        if diff < least:
          least = diff
          level = x
        lst.append(result)
    if level != 0:
      index = levels.index(level)
      if levels[index][3] != typ:
        return False
      levels[index][2] += (abs(s-l)/price) + ((i*i)/(df.shape[0]-thickness-2))
    return np.sum(lst) == 0

  try:
    price = float(get_current_price(name))
  except:
    return None

  levels = []
  point = None
  average = 0
  oc_average = 0
  l_average = 0
  h_average = 0
  thickness = 4

  #i = current iteration
  #h/l = high or low of current iteration
  for i in range(df.shape[0]-thickness-1,df.shape[0]-daylen,-1):
    if df['Close'][i-1] != float("nan"):
      average += (abs((df['Close'][i]/df['Close'][i-1])-1)) #average daily volatility (per)
      oc_average += (abs((df['Open'][i]/df['Close'][i])-1)) #average distance between day open and close (per)
      l_average += (((df['Low'][i]/df['Open'][i])-1)) #average distance between day open and low (per)
      h_average += (((df['High'][i]/df['Open'][i])-1)) #average distance between day open and close (per)
    if isSupport(df,i,thickness,'Low'):
      l = df['Low'][i]
      if isFarFromLevel(l,'s'):
        levels.append([i,l,1,'s'])
    elif isResistance(df,i,thickness,'High'):
      h = df['High'][i]
      if isFarFromLevel(h,'r'):
        levels.append([i,h,1,'r'])
            
  #price > points[0] can return True or False
  t_daylen = daylen/2 #true daylen
  for a in (average, oc_average, l_average, h_average):
      a = (a/t_daylen)*100
  if len(levels) > 1:
    while len(levels) > 2:
      levels.remove(min([(l[2],l) for l in levels])[1])
    resistance = [(level[1]) for level in levels if level[1] > price]
    support = [(level[1]) for level in levels if level[1] < price]
    if len(resistance) < 1 or len(support) < 1:
      print("{} eliminated: not within support and resistance".format(name,levels))
      return None
    else:
      res = resistance[0]
      sup = support[0]
    trend = findTrend(thickness, df, price)
    if trend > 0:
      potp = ((res/price)-1)*100
    else:
      potp = ((price/sup)-1)*100
    #print("trend: {}, stock: {}".format(trend,name)) #trend debugging
    buyStrength = potp * trend
    print("{} stock accepted. Buystrength: {}".format(name,buyStrength,average))
    return buyStrength, res, sup, average, trend, potp, l_average, h_average, oc_average

  print("{} eliminated: not enough S&L points".format(name))
  return None

def get_current_price(ticker):
  symbol = yfinance.Ticker(ticker)
  todays_data = symbol.history(period='1d')
  return round(todays_data['Close'][0],3)
