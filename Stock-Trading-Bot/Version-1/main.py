print ("Importing...")

import alpaca_trade_api as tradeapi
import time
from config import *
from Basics import *
import datetime

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

if config['Date'] != date:
  Override = False
  begin_time = datetime.datetime.now()
  Stocks = stockCalc(buying_power,date)
  print("It took this long to scan Stocks: {}".format(datetime.datetime.now() - begin_time))
else:
  if input("Stocks already scanned today. Override? (y/n)") == "n":
    print("Quitting program...")
    quit()
  else:
    Override = True
    begin_time = datetime.datetime.now()
    Stocks = stockCalc(buying_power,date)
    print("It took this long to scan Stocks: {}".format(datetime.datetime.now() - begin_time))
print("---")
print("Stock picks:")
print(Stocks)

if Override:
  if input("Do you still want to buy today? (y/n)") == "n":
    quit()

print("---")
print("Buying Stocks...")
def BuyAllStock():
  orders = []
  for stock in Stocks:
    if stock[6] > 0:
      try:
        api.submit_order(symbol = stock[0], qty = abs(stock[6]), side = 'buy', type = 'market')
        print("Bought {} shares of {}".format(stock[6], stock[0]))
        orders.append(stock)
      except Exception as e:
        print(stock[0] + " cannot be bought short because: {}".format(e))
    else:
      try:
        api.submit_order(symbol = stock[0], qty = abs(stock[6]), side = 'sell', type = 'market')
        print("Sold {} shares of {}".format(stock[6], stock[0]))
        orders.append(stock)
      except Exception as e:
        print(stock[0] + " cannot be sold because: {}".format(e))
  print("Waiting for API...")
  time.sleep(5)
  print(orders)
  for stock in orders:
    stopPercent = stock[4]*0.1
    if stopPercent < 0.1:
      stopPercent =  0.1
    if stock[6] > 0:
      api.submit_order(symbol = stock[0], qty = abs(stock[6]), side = 'sell', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = (stopPercent)) 
      print("Stoploss set for {} shares of {}".format(stock[6], stock[0]))
    else:
      api.submit_order(symbol = stock[0], qty = abs(stock[6]), side = 'buy', type = 'trailing_stop', time_in_force = 'gtc', trail_percent = (stopPercent))
      print("Stoploss set for {} shares of {}".format(stock[6], stock[0]))
BuyAllStock()


