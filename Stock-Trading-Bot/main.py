print ("Importing...")

from stockVal import findStockValuation
from stockVal import get_current_price
import alpaca_trade_api as tradeapi
from config import *
from Basics import *
from datetime import datetime

API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)
account = api.get_account()
buying_power = int(account.buying_power)
jsonFile = ConvertJson("json/Var.json")
date = datetime.date(datetime.now()).strftime("%m%d%y")
#api.submit_order(symbol = 'AAPL', qty=1, side='buy', type='market')

def findStockList():
  Stocks = []
  Stocks = [[x] for x in FindTopStocks()]

  print("Analyzing Stocks...")
  for stock in Stocks:
    stock.append(findStockValuation(stock[0]))

  print("Filtering Stocks...")
  Stocks = list(filter(lambda x: x[1] != 0, Stocks))
  Stocks.sort(key = SortSystem, reverse = True)
  return Stocks

if jsonFile['Date'] != date:
  FullStocks = findStockList()
  Stocks = FullStocks[:10]
  TotalRating = 0
  stockp = 0
  for stock in Stocks:
    stock.append(get_current_price(yfinance.Ticker(stock[0])))
    TotalRating += abs(stock[1])
  for stock in Stocks:
    stockp = float(stock[1]*(100/TotalRating)/100)
    print(stockp)
    total = stockp*buying_power
    totalspending = total/stock[2]
    stock.append(math.floor(totalspending))
  UpdateJson(ConvertStockList(Stocks))
  ChangeKey("Date","json/Var.json",date)
else:
  print("Stocks already scanned today.")
  Stocks = list(ConvertJson("json/StockStorage.json"))
print(Stocks)


  


