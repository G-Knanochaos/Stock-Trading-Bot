print ("Importing...")

from stockVal import findStockValuation
from stockVal import get_current_price
import alpaca_trade_api as tradeapi
from config import *
import Basics

#API_BASE_URL = 'https://paper-api.alpaca.markets'
#api = tradeapi.REST(API_KEY, API_SECRET, API_BASE_URL)
#api.submit_order(symbol = 'AAPL', qty=1, side='buy', type='market')

def findStockList():
  Stocks = []
  Stocks = [[x] for x in Basics.FindTopStocks()]

  print("Analyzing Stocks...")
  for stock in Stocks:
    stock.append(findStockValuation(stock[0]))

  print("Filtering Stocks...")
  Stocks = list(filter(lambda x: x[1] != 0, Stocks))
  Stocks.sort(key = Basics.SortSystem, reverse = True)
  return Stocks

FullStocks = findStockList()
Stocks = FullStocks[:10]
for stock in Stocks:
  stock.append(get_current_price(stock[0]))



  
  


