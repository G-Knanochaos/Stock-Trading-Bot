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
  s = (np.mean(df['High']/df['Low'])-1)*0.75

  try:
    price = float(get_current_price(name))
  except:
    print("Price of {} cannot be fetched. Eliminated.".format(name))
    return None

  def isFarFromLevel(l,typ,i,score):
    lst = []
    level = 0
    least = 100000
    for x in levels:
      diff = abs((x[1]/l)-1)
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
      levels[index][2] *= (s-least)*10 * score 
    return np.sum(lst) == 0

  levels = []
  point = None
  average = 0
  oc_average = 0
  l_average = 0
  h_average = 0
  trend = 0
  potp = 0
  thickness = 4
  start, end = df.shape[0]-1, df.shape[0]-daylen

  #i = current iteration
  #h/l = high or low of current iteration
  for i in range(start,end,-1):
    s_info = isSupport(df,i,'Low')
    if s_info[0] >= thickness: #if amount of iterations >= thickness
      l = df['Low'][i]
      if isFarFromLevel(l,'s',i,s_info[1]):
        levels.append([i,l,s_info[1],'s'])
      continue

    r_info = isResistance(df,i,'High')
    if r_info[0] >= thickness:
      h = df['High'][i]
      if isFarFromLevel(h,'r',i,r_info[1]):
        levels.append([i,h,r_info[1],'r'])
      continue
 
  #price > points[0] can return True or False
  k = lambda x : x[2]
  resistances = [level for level in levels if level[3] == 'r']
  supports = [level for level in levels if level[3] == 's']
  resistances.sort(reverse=True,key = k)
  supports.sort(reverse = True, key = k)
  res = resistances[0]
  sup = supports[0]
  if price < sup[1] or price > res[1]:
    print("{} eliminated: not within support and resistance".format(name,levels))
    return None
  #print("trend: {}, stock: {}".format(trend,name)) #trend debugging
  buyStrength = res[2]+sup[2]
  print("{} stock accepted. Resistance: {}, {}. Support: {}, {}".format(name,res[1],res[2],sup[1],sup[2]))
  return buyStrength, res, sup, average, trend, potp, l_average, h_average, oc_average

def get_current_price(ticker):
  symbol = yfinance.Ticker(ticker)
  todays_data = symbol.history(period='1d')
  return round(todays_data['Close'][0],3)
