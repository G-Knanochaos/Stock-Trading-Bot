import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import datetime
from GraphFuncs import *
plt.rcParams['figure.figsize'] = [8,5]
plt.rc('font', size=14)

lines = []
buystrength = 0

name = input("What stock would you like to scan?")
begin_time = datetime.datetime.now()
try:
  ticker = yfinance.Ticker(name)
except: 
  print("This ticker does not exist")
df = ticker.history(interval="1d",period="3mo")
df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
daylen = len(df['Date'].tolist())
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

def get_current_price(symbol):
  todays_data = symbol.history(period='1d')
  return todays_data['Close'][0]
price = float(get_current_price(ticker))

def plot_all():
  fig, ax = plt.subplots()

  candlestick_ohlc(ax,df.values,width=0.6, \
                   colorup='green', colordown='red', alpha=0.8)


  fig.tight_layout()

  for level in levels:
    plt.hlines(level[1],xmin=df['Date'][0],\
               xmax=max(df['Date']),colors='blue')
    plt.text(df['Date'][0],level[1]+0.05,s=str(level[2])+level[3])

  fig.show()

s = np.mean(df['High'] - df['Low']) * 2

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

levels = []
boolean = 0
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

print(levels)
def stockVal():
  global buyStrength
  if len(levels) > 1:
    while len(levels) > 2:
      levels.remove(min([(l[2],l) for l in levels])[1])
    resistance = [(level[1]) for level in levels if level[1] > price]
    support = [(level[1]) for level in levels if level[1] < price]
    if len(resistance) > 0 and len(support) > 0:
      res = resistance[0]
      sup = support[0]
    else:
      return 0
    if price < res and price > sup:
      mid = (res+sup)/2 
      buyStrength = (-(((price/mid)-1)*100))
stockVal()
  
run = True
showSwings = True
print("The stock you chose is: " + name + ". The stock's current price is " + str(round(price,2)))
print("The stock's current resistance prices are:")
print([level for level in levels if level[1] > price])
print("The stock's current support prices are:")
print([level for level in levels if level[1] < price])
print("--")
try:
  print("The stock has a BUY STRENGTH of: ", buyStrength)
except:
  print("Not ideal to buy")
print("This script took: {}".format(datetime.datetime.now() - begin_time))
if input("Plot? (y/n)") == "n":
  quit()
plot_all()

