#!/usr/bin/env python3
print ("Importing...")

import alpaca_trade_api as tradeapi
import time
from Basics import ConvertJson, stockCalc
from config import *
import datetime

if input('Override Market Wait?') == 'n':
  print("Waiting for market open...")
  while True:
    now = datetime.datetime.now()
    current_time = int(now.strftime("%H%M"))
    print(current_time)
    if current_time >= 630 or current_time <= 800:
      print('Start time: {}'.format(current_time))
      break
    time.sleep(60)
  print("Market has opened. Beginning program...")

api = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)

account = api.get_account()
buying_power = int(float(account.buying_power))
portfolio = api.list_positions()
orders = api.list_orders(status='open')
print(portfolio)
config = ConvertJson("/Users/oceanhawk/Documents/Python/Stock-Trading-Bots/Version-1/json/Var.json")
date = datetime.datetime.date(datetime.datetime.now()).strftime("%m%d%y")

print("---")
print("Cleaning portfolio...")
api.close_all_positions()
begin_time = datetime.datetime.now()
Stocks = stockCalc(buying_power,date)
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
  orders = []
  for stock in Stocks:
    if stock[-2] > 0:
      try:
        api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'buy', type = 'market')
        print("Bought {} shares of {}".format(stock[-2], stock[0]))
        orders.append(stock)
      except Exception as e:
        print(stock[0] + " cannot be bought short because: {}".format(e))
    else:
      try:
        api.submit_order(symbol = stock[0], qty = abs(stock[-2]), side = 'sell', type = 'market')
        print("Sold {} shares of {}".format(stock[-2], stock[0]))
        orders.append(stock)
      except Exception as e:
        print(stock[0] + " cannot be sold because: {}".format(e))
  #print("Waiting for API...")
  #time.sleep(5)
  #print(orders)
  #for stock in orders:
    #stopPercent = stock[4]*0.6
    #if stopPercent < 0.1:
      #stopPercent =  0.1
    #if stock[8] > 0:
      #api.submit_order(symbol = stock[0], qty = abs(stock[8]), side = 'sell', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = (stopPercent)) 
      #print("Stoploss set for {} shares of {}".format(stock[8], stock[0]))
    #else:
      #api.submit_order(symbol = stock[0], qty = abs(stock[8]), side = 'buy', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = (stopPercent))
      #print("Stoploss set for {} shares of {}".format(stock[8], stock[0]))
BuyAllStock()


