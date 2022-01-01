import pandas as pd
import numpy as np
import yfinance
import matplotlib.dates as mpl_dates
from stockValFunc import *

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
  s = np.mean(df['High'] - df['Low'])*2
  stct = True

  try:
    price = float(get_current_price(ticker))
  except:
    return 0, 0 ,0, 0

  global levels
  levels = []
  point = None
  go = True
  average = 0
  oc_average = 0
  l_average = 0
  h_average = 0
  for i in range(df.shape[0]-2,df.shape[0]-daylen,-1):
    average += (abs(df['Close'][i]-df['Close'][i-1])/price)
    oc_average += (abs((df['Open'][i]/df['Close'][i])-1))
    l_average += ((df['Low'][i]-df['Close'][i-1])/price)
    h_average += ((df['High'][i]-df['Close'][i-1])/price)
    if go:
      if isSupport(df,i,1,'Close'):
        l = round(df['Close'][i],3)
        point = l
        go = False
      elif isResistance(df,i,1,'Close'):
        h = round(df['Close'][i],3)
        point = h
        go = False

  for i in range(df.shape[0]-4,df.shape[0]-daylen,-1):
    if isSupport(df,i,1,'Low'):
      if isSupport(df,i,2,'Low'):
        if isSupport(df,i,3,'Low'):
          l = df['Low'][i]
          if isFarFromLevel(l,'s'):
            levels.append([i,l,1,'s'])
    elif isResistance(df,i,1,'High'):
      if isResistance(df,i,2,'High'):
        if isResistance(df,i,3,'High'):
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
      return 0, 0, 0, 0
    else:
      res = resistance[0]
      sup = support[0]
    if price < res and price > sup:
      mid = (res+sup)/2
      strength = (-(((price/mid)-1)*100))
      trend = (((price/point)-1)*100)/average #time difference stuffs
      #print("trend: {}, stock: {}".format(trend,name)) #trend debugging
      if trend > 1 and strength < 0:
        print("{} eliminated: in up trend".format(name))
        stct = False
      elif trend < -1 and strength > 0:
        print("{} eliminated: in down trend".format(name))
        stct = False
      elif not trend > 1 and not trend < -1:
        print("{} eliminated: stock not active".format(name))
        stct = False
      buyStrength = (strength * abs(trend))
      print("{} stock accepted. Buystrength: {}".format(name,buyStrength,average))
      return buyStrength, res, sup, average, (trend,point), strength, l_average, h_average, stct, oc_average
      print("{} eliminated: not enough S&L points".format(name))
  return 0, 0, 0, 0
  
def get_current_price(symbol):
    todays_data = symbol.history(period='1d')
    return round(todays_data['Close'][0],3)

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
    levels[index][2] += (abs(s-l)/price)
  return np.sum(lst) == 0
