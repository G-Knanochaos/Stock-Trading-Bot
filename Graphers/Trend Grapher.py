import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
df = ticker.history(interval="1d",period="6mo")
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

  if showSwings:
    for point in points:
      plt.scatter(point[0],point[1],s=100.0,c='black')
    for i in range(0,len(points)-1):
      plt.plot((points[i][0],points[i+1][0]),(points[i][1],points[i+1][1]),'k-')

  fig.show()

s =  np.mean(df['High'] - df['Low']) * 2

points = [(max(df['Date']),price)]
boolean = 0
a = 0
t_daylen = daylen-2
for i in range(df.shape[0]-3,df.shape[0]-daylen,-1):
  a += (abs(df['Close'][i]-df['Close'][i-1])/price)
  if isSupport(df,i,2,'Close'):
    l = df['Close'][i]
    points.append((df['Date'][i],l))
  elif isResistance(df,i,2,'Close'):
    h = df['Close'][i]
    points.append((df['Date'][i],h))

a = (a/t_daylen)*100
def stockVal():
  global isUptrend
  isUptrend = price > points[1][1]
  trend = (((price/points[1][1])-1)*100)/a
stockVal()

showSwings = True
print("The stock you chose is: " + name + ". The stock's current price is " + str(round(price,2)))
if isUptrend:
  print("The stock is currently in an uptrend.")
else:
  print("The stock is currently in a downtrend.")
print("--")
print("This script took: {}".format(datetime.datetime.now() - begin_time))
if input("Show Swings? (y/n)") == "n":
  showSwings = False
plot_all()

