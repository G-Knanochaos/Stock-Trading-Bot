print ("Importing...")

import alpaca_trade_api as tradeapi
from config import *
from Basics import *
from datetime import datetime

api = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)
account = api.get_account()
buying_power = int(float(account.buying_power))
portfolio = api.list_positions()
print(portfolio)
config = ConvertJson("/Users/oceanhawk/Documents/Python/Stock-Trading-Bot/json/Var.json")
date = datetime.date(datetime.now()).strftime("%m%d%y")

if config['Date'] != date:
  Override = False
  Stocks = stockCalc(buying_power,date)
else:
  if input("Stocks already scanned today. Override? (y/n)") == "n":
    print("Quitting program...")
    quit()
  else:
    Override = True
    Stocks = stockCalc(buying_power,date)
print("---")
print("Stock picks:")
print(Stocks)
if Override:
  if input("Do you want to clean your portfolio? (y/n)") == "n":
    quit()

print("---")
print("Cleaning portfolio")
for stock in StockCleaning(portfolio):
  print(stock)
  if stock[2] == "long":
    api.submit_order(symbol = stock[0], qty = stock[1], side = "sell")
    print("Liquidated {} shares of {}".format(stock[1], stock[0]))
  else:
    api.submit_order(symbol = stock[0], qty = abs(stock[1]), side = "buy")
    print("Liquidated {} shares of {}".format(stock[1], stock[0]))

if Override:
  if input("Do you still want to buy today? (y/n)") == "n":
    quit()

print("---")
print("Buying Stocks...")
for stock in Stocks:
  if stock[5] > 0:
    try:
      api.submit_order(symbol = stock[0], qty = stock[5], side = 'buy', type = 'market')
      print("Bought {} shares of {}".format(stock[5], stock[0]))
    except Exception as e:
      print(stock[0] + " cannot be bought because: {}".format(e))
  else:
    try:
      api.submit_order(symbol = stock[0], qty = abs(stock[5]), side = 'sell', type = 'market') 
      print("Sold {} shares of {}".format(stock[5], stock[0]))
    except Exception as e:
      print(stock[0] + " cannot be sold short because: {}".format(e))

