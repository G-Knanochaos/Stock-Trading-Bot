#!/usr/bin/env python3
print ("Importing...")

import time
import Basics
from stockVal import get_current_price, findTrend, fetchData
from config import api
import datetime

def find_time():
  now = datetime.datetime.now()
  current_time = int(now.strftime("%H%M"))
  print(now.strftime("%H:%M:%S"))
  return current_time 

print('"" = default option')
clear_p = input('Clear portfolio? (y/"n")') == 'y'
if input('Wait for market open? ("y"/n)') != 'n':
  print("Waiting for market open...")
  while True:
    t = find_time()
    if t >= 625 and t <= 800:
      break
    time.sleep(60)
  while True:
    t = find_time()
    if t == 630:
     print('Start time: {}'.format(t))
     break
    time.sleep(5)
  print("Market has opened. Beginning program...")

c_positions = api.list_positions()
print("---")
print("Scanning Open Positions...")
p_data = Basics.stockAnal([[p.symbol] for p in c_positions])
print("---")
p_num = 5-len(c_positions)
print('{} open slots available'.format(p_num))#number of stocks that need replacing (open slots)
orders = api.list_orders()
b = [p.symbol for p in c_positions]

def get_order_id(ticker):
  for order in orders:
    if order.symbol == ticker:
      return order.id
def close_position(ticker, order_id, shares):
  try:
    api.cancel_order(order_id)
  except:
    print('No open trailing order for {}'.format(ticker))
  time.sleep(5)
  try:
    api.close_position(ticker, qty = abs(shares))
  except:
    print('No open position for {}.'.format(ticker))

print("Filtering open positions")
for stock in tuple(zip(c_positions,p_data)):
  print('-')
  ticker, value, shares = stock[0].symbol, float(stock[0].market_value), int(stock[0].qty)
  try:
    price = get_current_price(ticker)
  except:
    print('Info not received for {}. Closing position...'.format(ticker))
    close_position(ticker, order_id, stock[1][11])
  order_id = get_order_id(ticker)
  trend = findTrend(8, fetchData(ticker), price)
  if value > 0:
    line = stock[1][2]-((stock[1][6]*stock[1][3])*0.001)
    if trend < 0:
      print('{} trend reversed. Closing position...'.format(ticker))
      close_position(ticker, order_id, shares)
      continue
    elif price >= line:
      print('{} near resistance line. Closing position...'.format(ticker))
      close_position(ticker, order_id, shares)
      continue
  elif value < 0:
    line = stock[1][3]+((stock[1][6]*stock[1][2])*0.001)
    if trend > 0:
      print('{} trend reversed. Closing position...'.format(ticker))
      close_position(ticker, order_id, shares)
      continue
    elif price <= line:
      print('{} near support line. Closing position...'.format(ticker))
      close_position(ticker, order_id, shares)
      continue
  print("Holding {}".format(ticker))


#Scans if stocks have reached support or resistence or reversed, and sells if they have ^^
print("---")

if clear_p:
  p_num = 5
  print("---")
  print("Cleaning portfolio...")
  api.cancel_all_orders()
  api.close_all_positions()
else:
  if p_num == 0:
    print("No stocks need replacing. Quitting program...")
    quit()

account = api.get_account()
buying_power = int(float(account.cash)) #set to 1000 during actual trading
print("Buying power: {}".format(buying_power))
config = Basics.ConvertJson(Basics.directory + "json/Var.json")
date = datetime.datetime.date(datetime.datetime.now()).strftime("%m%d%y")

begin_time = datetime.datetime.now()
finviz_stocks = [[x] for x in Basics.FindTopStocks(b)]
Stocks = Basics.stockCalc(finviz_stocks,buying_power,date)[:p_num]
print("It took this long to scan Stocks: {}".format(datetime.datetime.now() - begin_time))
print("---")
print("Stock picks:")
print(Stocks)

if config['Date'] == date:
  if input("Do you still want to buy today? (y/n)") == "n":
    quit()

print("---")
print("Buying Stocks...")
def BuyAllStock():
  for stock in Stocks:
    if stock[-2] > 0:
      api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'buy', type = 'market')
      t = datetime.datetime.now().strftime("%H:%M:%S")
      print("Bought {} shares of {}. Time: {};         ".format(stock[-2], stock[0], t))
    else:
      api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'sell', type = 'market')
      t = datetime.datetime.now().strftime("%H:%M:%S")
      print("Sold {} shares of {}. Time: {};        ".format(stock[-2], stock[0], t))
  print("Waiting for API")
  time.sleep(120)
  for stock in Stocks:
    if stock[-2] > 0:
      api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'sell', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = round(stock[6]*(1/2),2)) 
      print("Trailing order set for {} shares of {};         ".format(stock[-2], stock[0]))
    else:
      api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'buy', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = round(stock[6]*(1/3),2)) 
      print("Trailing order set for {} shares of {};         ".format(stock[-2], stock[0]))
BuyAllStock()

